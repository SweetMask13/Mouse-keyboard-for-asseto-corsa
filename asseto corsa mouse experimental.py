from ctypes import *

user32 = windll.user32

if starting:
    import mmap
    import struct

    # === НАСТРОЙКИ FORCE FEEDBACK ===
    SHARED_MEMORY_NAME = "Local\\acpmf_physics"
    SHARED_MEMORY_SIZE = 312
    TELEMETRY_STRUCT_FORMAT = 'f' * 78
    FFB_INDEX = 77  
    
    ffb_strength = 50.00

    try:
        shared_memory = mmap.mmap(-1, SHARED_MEMORY_SIZE, SHARED_MEMORY_NAME)
        telemetry_struct = struct.Struct(TELEMETRY_STRUCT_FORMAT)
        ffb_enabled = True
    except:
        ffb_enabled = False
        
    v = vJoy[0]
    
    # === НАСТРОЙКА ГОЛОСА ===
    import clr
    clr.AddReference("System.Speech")
    from System.Speech.Synthesis import SpeechSynthesizer
    spk = SpeechSynthesizer()
    
    for voice in spk.GetInstalledVoices():
        if "Russian" in voice.VoiceInfo.Culture.EnglishName:
            spk.SelectVoice(voice.VoiceInfo.Name)
            russian_found = True
            break
            
    spk.Rate = 4      
    spk.Volume = 100   
    
    # ===== ДИАПАЗОНЫ ОСЕЙ =====
    a_max = v.axisMax
    a_min = -v.axisMax - 1
    a_full_range = a_max - a_min
    
    # ===== НАСТРОЙКИ РУЛЯ =====
    steering = 0.0
    m_sens = 14.0      
    power_curve = 1.6  
    
    # ===== НАСТРОЙКИ УМНЫХ ПЕДАЛЕЙ =====
    gas_current = 0.0     
    brake_current = 0.0   
    pedal_limit = 0.5     
    
    ramp_speed = 0.02    # Набор газа
    brake_speed = 0.02    # Набор тормоза
    limit_speed = 0.02    # Чувствительность A/D
    
    # ===== СОСТОЯНИЯ =====
    shift_mode = 1 
    mouselock = False

# ==========================================
# ===== ОСНОВНОЙ ЦИКЛ =====
# ==========================================

toggle_mouselock = mouse.getPressed(4)
toggle_shiftmode = keyboard.getPressed(Key.CapsLock)
key_center = keyboard.getKeyDown(Key.B)

# Клавиши педалей
key_w = keyboard.getKeyDown(Key.W)
key_s = keyboard.getKeyDown(Key.S)
key_shift = keyboard.getKeyDown(Key.LeftShift) # ТОТ САМЫЙ FORCE
key_lmb = mouse.getButton(0)  # Оставил как "Паник-брейк"
key_clutch = keyboard.getKeyDown(Key.LeftControl)

key_up = keyboard.getKeyDown(Key.F)
key_down = keyboard.getKeyDown(Key.V)

if toggle_mouselock:
    mouselock = not mouselock

if toggle_shiftmode:
    if shift_mode == 1:
        shift_mode = 2
        if russian_found:
            spk.SpeakAsync("Ручная")
        else:
            spk.SpeakAsync("Manual")
    else:
        shift_mode = 1
        if russian_found:
        	spk.SpeakAsync("Ассист")
        else:
        	spk.SpeakAsync("Assist")

if mouselock:
    user32.SetCursorPos(0, 5000)

# ===== 1. РУЛЬ + FFB =====
ffb_round = 0.0
if mouselock:
    if ffb_enabled:
        try:
            shared_memory.seek(0)
            telemetry_values = telemetry_struct.unpack(shared_memory.read(telemetry_struct.size))
            ffb_round = telemetry_values[FFB_INDEX] * ffb_strength 
        except:
            pass 
    steering += ((mouse.deltaX * m_sens) - ffb_round)

if steering > a_max: steering = a_max
if steering < a_min: steering = a_min
if key_center: steering = 0.0

steer_norm = steering / a_max
steer_curved = (abs(steer_norm) ** power_curve) * a_max
if steer_norm < 0: steer_curved = -steer_curved

# ===== 2. ЛОГИКА ПЕДАЛЕЙ (SHIFT = FORCE) =====

target_gas = 0.0
target_brake = 0.0

if mouselock:
    # Авто-сброс лимита до 50%
    if not key_w and not key_s:
        pedal_limit = 0.5
        
    # Регулировка лимита (A/D)
    if keyboard.getKeyDown(Key.D): pedal_limit += limit_speed
    if keyboard.getKeyDown(Key.A): pedal_limit -= limit_speed
    pedal_limit = max(0.05, min(1.0, pedal_limit))

    # Определяем, какой предел использовать сейчас
    current_power = 1.0 if key_shift else pedal_limit

    # ГАЗ
    if key_w:
        target_gas = current_power
    
    # ТОРМОЗ
    if key_lmb:
        target_brake = 1.0     # ЛКМ всегда 100%
        brake_current = 1.0    # Мгновенно
    elif key_s:
        target_brake = current_power

# Сглаживание
if gas_current < target_gas:
    gas_current = min(gas_current + ramp_speed, target_gas)
elif gas_current > target_gas:
    gas_current = max(gas_current - ramp_speed * 2.5, target_gas)

if brake_current < target_brake:
    brake_current = min(brake_current + brake_speed, target_brake)
elif brake_current > target_brake:
    brake_current = max(brake_current - brake_speed * 3.0, target_brake)

th_out = a_min + (gas_current * a_full_range)
br_out = a_min + (brake_current * a_full_range)

# ===== 3. КПП =====
v.setButton(0, key_up)
v.setButton(1, key_down)
if shift_mode == 1:
    if key_up: th_out = a_min 
    if key_down:
        blip = a_min + (a_full_range * 0.45) 
        if th_out < blip: th_out = blip

# ===== 4. ВЫВОД =====
v.x = int(steer_curved)
v.y = int(th_out)
v.z = int(br_out)
v.rz = int(a_max if key_clutch else a_min)