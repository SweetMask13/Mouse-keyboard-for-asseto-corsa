# 🖱️⌨️ Assetto Corsa – Advanced Mouse & Keyboard Control Suite

**Experimental release.** A complete FreePIE script that transforms your mouse and keyboard into a high‑precision sim racing controller with **real Force Feedback**, **smart pedal logic**, and **switchable driving profiles**.

Designed for drivers who want the precision of a mouse with the predictability and smoothness of an analog pedal set.

---

## 📦 Features Overview

| Feature | Description |
|---------|-------------|
| 🖱️ **Mouse Steering** | Exponential curve (soft center, progressive edges) for precise control. |
| 🔁 **Real Force Feedback** | Reads FFB data directly from `acpmf_physics` shared memory and applies self‑aligning torque to the virtual wheel. |
| 🧠 **Smart Pedals (W/S)** | Throttle and brake start at **50%** every time. Smooth ramping – no jerky on/off. |
| 📊 **Dynamic Limit (A/D)** | Raise or lower the throttle/brake limit on the fly (5% – 100%). |
| 🔁 **Auto‑Reset Limit** | When pedals are released, the limit resets to **50%** – predictable corner entry. |
| ⚡ **Override (Shift)** | Hold `Shift` + `W` or `S` for **instant 100%** throttle/brake, ignoring the current limit. |
| 🚨 **Panic Brake (LMB)** | Left mouse button gives **instant 100% brake** – bypasses all smoothing. |
| 🔧 **Shift Assist Modes** | Toggle between auto‑blip (assisted) and manual shifting with `Caps Lock`. |
| 🎤 **Voice Feedback** | voice announcements for mode/profile changes (customizable). |
| 🔒 **Mouse Lock** | Cursor fixed to screen while driving (toggle with Mouse Button 4). |
| 🔄 **Center Steering** | Press `B` to instantly center the virtual wheel. |

---

## ⌨️ Complete Control Map

### Primary Controls

| Key / Combo | Function |
|-------------|----------|
| **Mouse Move Left/Right** | Steering |
| **`W`** | Smart Throttle (starts at 50%, ramps smoothly) |
| **`S`** | Smart Brake (starts at 50%, ramps smoothly) |
| **`A`** | Decrease throttle/brake limit (min 5%) |
| **`D`** | Increase throttle/brake limit (max 100%) |
| **`Shift` + `W`** | Instant 100% Throttle (override) |
| **`Shift` + `S`** | Instant 100% Brake (override) |
| **`LMB` (Left Mouse)** | Panic Brake – instant 100%, no smoothing |
| **`Left Ctrl`** | Clutch |
| **`F`** | Shift Up |
| **`V`** | Shift Down |
| **`Mouse Button 4`** | Toggle Mouse Lock (cursor fixed / free) |
| **`Caps Lock`** | Toggle Shift Assist (Auto‑blip ON / Manual) |
| **`B`** | Center Steering Wheel |

---

## 🧠 How the Smart Pedals Work

The pedal system is designed to give you **maximum consistency** without sacrificing power when you need it.

1. **Always start at 50%**  
   When you press `W` or `S`, the pedal begins at **50%** power. This is your predictable "baseline" for cornering.

2. **Adjust on the fly**  
   While driving, tap `D` to raise the limit (e.g., 70% for more acceleration out of a corner) or `A` to lower it (e.g., 30% for a slippery surface). The change is applied smoothly.

3. **Auto‑Reset**  
   When you release both pedals (neither `W` nor `S` is held), the limit **automatically resets to 50%**. You never have to remember what limit you set three corners ago.

4. **Override with Shift**  
   Need full throttle on a straight? Just hold `Shift` while pressing `W`. The limit is ignored and you get instant 100% power. Same for hard braking with `Shift` + `S`.

5. **Panic Brake**  
   In an emergency, click `LMB`. Brake jumps to 100% instantly, bypassing all smoothing. Release it and the brake returns to its previous smart behavior.

6. **Smooth Ramping**  
   All pedal movements (except panic brake and overrides) are smoothed. Throttle and brake ramp up and down at a natural rate, making weight transfer feel more realistic and preventing sudden loss of traction.

## 🔁 Force Feedback (FFB) Details

The script connects to Assetto Corsa's **shared memory** (`Local\acpmf_physics`) and reads the raw FFB value that the game sends to a real steering wheel. This value is then **subtracted from your mouse movement**, creating a natural "self‑aligning torque" effect.

- **Strength** is set to **50** by default (adjustable per profile).  
- At this level, FFB acts as a **subtle guide**, helping you unwind the steering on corner exit and providing a hint of understeer/oversteer.  
- It does **not** take over control – you remain fully in charge, but with much better feedback than standard mouse steering.

> ⚠️ **Note:** FFB strength can cause the virtual wheel center to drift over time. Use `B` to recenter, or simply lift and reposition your mouse.

---

## 🔊 Voice Feedback

The script uses Windows TTS to announce mode changes. You can change the voice, language, or disable it entirely in the `if starting:` block.

---

## 📥 Installation & Setup

### Requirements
- [vJoy](https://sourceforge.net/projects/vjoystick/) (configure at least one device with X, Y, Z, RX, RY, RZ axes)
- [FreePIE](https://github.com/AndersMalmgren/FreePIE)
- Run FreePIE **as Administrator** (required for shared memory access)

### Steps
1. Install and configure vJoy.
2. Open FreePIE, paste the script, and run it.
3. Launch Assetto Corsa (Content Manager recommended).
4. In Controls settings:
   - **Steering** → `vJoy X`
   - **Throttle** → `vJoy Y`
   - **Brake** → `vJoy Z`
   - **Clutch** → assign the clutch as a button instead of a stick
   - Disable in‑game **"Use mouse to look"** to avoid camera conflicts.
5. Press **Mouse Button 4** to lock the cursor and start driving.

---

## 🆚 Differences from the Old (Pre‑release) Version

| Old Version (`Mouse Steering with Limiters`) | New Version (`WASD Smart Pedals`) |
|----------------------------------------------|-----------------------------------|
| Throttle/Brake on mouse buttons (`LMB`/`RMB`) | Throttle/Brake on keyboard **`W`** / **`S`** |
| Static limiters on `Z`(20%), `X`(50%), `C`(80%) | Dynamic limit adjustable with **`A`** / **`D`** (5‑100%) |
| Limiters must be held continuously | Limit stays active until pedals are released |
| No auto‑reset; limit stays where you left it | Limit **auto‑resets to 50%** when pedals released |
| Mouse wheel used for ±15% trim | Trim replaced by `A`/`D`; wheel available for other uses |
| Single driving profile | Three **switchable profiles** (`Tab`) |
| FFB strength fixed globally | FFB strength adjustable per profile |
| No override for instant 100% | `Shift` + `W`/`S` gives **instant 100%** |

The new version provides a **more consistent and predictable driving experience**, especially on technical tracks like Tsubaki Line. The auto‑reset to 50% eliminates the need to remember previous limits, and the `Shift` override gives you full power exactly when you want it.

---

## 🔧 Customization

All key parameters are grouped at the top of the script inside the `if starting:` block. You can tweak:

- `pedal_limit` (default 0.5)
- `ramp_speed` / `brake_speed`
- `limit_speed` (how fast `A`/`D` changes the limit)
- `m_sens` (mouse sensitivity)
- `power_curve` (steering non‑linearity)
- `ffb_strength`
- Profile values in the `profiles` list

---

## 🙏 Credits & Thanks

- Original FFB memory reading concept adapted from [SnowmileZ/simulating-force-feedback-on-mouse](https://github.com/SnowmileZ/simulating-force-feedback-on-mouse)
- Community discussions and extensive testing on Tsubaki Line downhill.

---

*Feedback and pull requests are welcome. Enjoy the drive!*
