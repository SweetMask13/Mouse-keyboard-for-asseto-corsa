from ctypes import *
user32 = windll.user32

if starting:   
    import mmap
    import struct

    # === НАСТРОЙКИ FORCE FEEDBACK (ИЗ ПАМЯТИ ИГРЫ) ===
    SHARED_MEMORY_NAME = "Local\\acpmf_physics"
    SHARED_MEMORY_SIZE = 312
    TELEMETRY_STRUCT_FORMAT = 'f' * 78
    FFB_INDEX = 77  # Индекс значения FFB в структуре
    
    # Сила отдачи (в скрипте было 500, но ты можешь менять это под себя)
    ffb_strength = 50.00

    # Пытаемся подключиться к памяти (чтобы скрипт не падал, если игра еще не запущена)
    try:
        shared_memory = mmap.mmap(-1, SHARED_MEMORY_SIZE, SHARED_MEMORY_NAME)
        telemetry_struct = struct.Struct(TELEMETRY_STRUCT_FORMAT)
        ffb_enabled = True
    except:
        ffb_enabled = False
        
    v = vJoy[0]
    prev_state = (False, False, False, False, False)
    # Настройка русского голоса
    import clr
    clr.AddReference("System.Speech")
    from System.Speech.Synthesis import SpeechSynthesizer
    spk = SpeechSynthesizer()
    
    # Пытаемся найти русский голос
    found_russian = False
    for voice in spk.GetInstalledVoices():
        if "Russian" in voice.VoiceInfo.Culture.EnglishName:
            spk.SelectVoice(voice.VoiceInfo.Name)
            found_russian = True
            break
            
    spk.Rate = 4      # Скорость (быстро)
    spk.Volume = 100   # Громкость
    
    # ===== ДИАПАЗОНЫ ОСЕЙ =====
    a_max = v.axisMax
    a_min = -v.axisMax - 1
    a_full_range = a_max - a_min
    
    # ===== НАСТРОЙКИ РУЛЯ =====
    steering = 0.0
    m_sens = 14.0      # Общая скорость
    # 1.4 - золотая середина. Мягко в центре, но без "приклеивания"
    power_curve = 1.6  
    
    # ===== НАСТРОЙКИ ПЕДАЛЕЙ =====
    th_axis = a_min
    br_axis = a_min
    # Скорость "доезда" до цели (лимита или 0)
    pedal_inc = 3800   
    pedal_dec = 4800   
    
    # ===== КОЛЕСИКО (ЛОГИКА КАНАТА) =====
    wheel_offset = 0.0 # 0 - центр, плюс - газ, минус - тормоз
    wheel_step = a_full_range * 0.05   # Шаг 5%
    wheel_cap = a_full_range * 0.15    # Макс 15%
    
    # ===== СОСТОЯНИЯ =====
    shift_mode = 1 
    mouselock = False

# ===== КНОПКИ =====
toggle_mouselock = mouse.getPressed(4)
toggle_shiftmode = keyboard.getPressed(Key.CapsLock)
key_center = keyboard.getKeyDown(Key.B)

key_throttle = mouse.getButton(0) # ЛКМ
key_brake = mouse.getButton(1)    # ПКМ
key_clutch = keyboard.getKeyDown(Key.LeftControl)

key_up = keyboard.getKeyDown(Key.F)
key_down = keyboard.getKeyDown(Key.V)

limit_20 = keyboard.getKeyDown(Key.A)
limit_50 = keyboard.getKeyDown(Key.S)
limit_80 = keyboard.getKeyDown(Key.D)

# ===== ЛОГИКА ПЕРЕКЛЮЧАТЕЛЕЙ =====
if toggle_mouselock:
    mouselock = not mouselock

if toggle_shiftmode:
    if shift_mode == 1:
        shift_mode = 2
        spk.SpeakAsync("Ручная") # Быстрый асинхронный ответ
    else:
        shift_mode = 1
        spk.SpeakAsync("Ассист")
        
        
if mouselock:
    user32.SetCursorPos(0, 5000)

# ===== 1. РУЛЬ + FORCE FEEDBACK =====

ffb_round = 0.0


if mouselock:
    # Читаем отдачу из игры, если удалось подключиться к памяти
    if ffb_enabled:
        try:
            shared_memory.seek(0)
            telemetry_values = telemetry_struct.unpack(shared_memory.read(telemetry_struct.size))
            ffb_value = telemetry_values[FFB_INDEX]
            # Умножаем сырое значение на нашу силу
            ffb_round = ffb_value * ffb_strength 
        except:
            pass # Если игра закрылась - просто игнорируем

    # ВОТ ОНА МАГИЯ: Мышка управляет, а игра "выбивает" руль
    # В зависимости от настроек инверсии в AC, тут может понадобиться поменять минус на плюс
    steering += ((mouse.deltaX * m_sens) - ffb_round)

# Ограничители (чтобы руль не свернуло за 100%)
if steering > a_max: steering = a_max
if steering < a_min: steering = a_min

if key_center:
    steering = 0.0

# Математика кривой (оставляем твою)
steer_norm = steering / a_max
steer_curved = (abs(steer_norm) ** power_curve) * a_max
if steer_norm < 0: steer_curved = -steer_curved

# ===== 2. КОЛЕСИКО И СЛЕДЖЕНИЕ ЗА КНОПКАМИ =====

# Собираем все важные кнопки в один список, чтобы следить за их изменениями
current_state = (key_throttle, key_brake, limit_20, limit_50, limit_80)

# Если ты нажал или отпустил ЛЮБУЮ из этих кнопок -> сбрасываем колесико в 0
if current_state != prev_state:
    wheel_offset = 0.0
    prev_state = current_state
glide_speed = a_full_range * 0.006
# Крутим колесико
if keyboard.getKeyDown(Key.E):
    wheel_offset += glide_speed
if keyboard.getKeyDown(Key.Q):
    wheel_offset -= glide_speed

# Ограничиваем канат (от -15% до +15%)
if wheel_offset > wheel_cap: wheel_offset = wheel_cap
if wheel_offset < -wheel_cap: wheel_offset = -wheel_cap

# ===== 3. ГАЗ И ТОРМОЗ (УМНАЯ ЛОГИКА) =====

current_limit = a_max
if limit_20: current_limit = a_min + (a_full_range * 0.20)
elif limit_50: current_limit = a_min + (a_full_range * 0.50)
elif limit_80: current_limit = a_min + (a_full_range * 0.80)

# По умолчанию всё в ноль
th_target = a_min
br_target = a_min

# 2. Логика работает ТОЛЬКО при заблокированной мыши
if mouselock:
    if not any(current_state):
        # Состояние покоя: работает только "канат" на Q/E
        if wheel_offset > 0: th_target = a_min + wheel_offset
        if wheel_offset < 0: br_target = a_min + abs(wheel_offset)
    else:
        # Состояние нажатия: лимиты + триммер Q/E
        if key_throttle:
            th_target = current_limit + wheel_offset
        if key_brake:
            br_target = current_limit - wheel_offset
else:
    # Если mouselock ОТКЛЮЧЕН (курсор на экране):
    # Газ и тормоз принудительно идут в 0, чтобы клики в меню не мешали
    th_target = a_min
    br_target = a_min
    # Дополнительно: можно сбросить триммер Q/E
    wheel_offset = 0.0

# 3. Жесткие рамки (защита)
if th_target > a_max: th_target = a_max
if th_target < a_min: th_target = a_min
if br_target > a_max: br_target = a_max
if br_target < a_min: br_target = a_min

# 4. Плавная интерполяция (оставляем снаружи if mouselock, 
# чтобы педали плавно возвращались в 0 при разблокировке)
if th_axis < th_target:
    th_axis = min(th_axis + pedal_inc, th_target)
else:
    th_axis = max(th_axis - pedal_dec, th_target)

if br_axis < br_target:
    br_axis = min(br_axis + pedal_inc, br_target)
else:
    br_axis = max(br_axis - pedal_dec, br_target)

th_out = th_axis
br_out = br_axis

# ===== 4. КОРОБКА ПЕРЕДАЧ =====
v.setButton(0, key_up)
v.setButton(1, key_down)

if shift_mode == 1:
    if key_up: th_out = a_min # Плавная отсечка здесь не нужна, важна скорость
    if key_down:
        blip = a_min + (a_full_range * 0.45)
        if th_out < blip: th_out = blip

# ===== 5. ВЫВОД В VJOY =====
v.x = int(steer_curved)
v.y = int(th_out)
v.z = int(br_out)
v.rz = int(a_max if key_clutch else a_min) # Сцепление перенес на RZ