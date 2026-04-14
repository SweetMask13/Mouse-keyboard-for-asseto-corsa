# ⌨️ Assetto Corsa WASD Smart Pedals with FFB

**Experimental release.** A complete overhaul of the control scheme.  
Throttle and brake are now on `W`/`S` with smart, auto‑resetting limits and instant overrides.  
Ideal for drivers who want consistency and smooth inputs without sacrificing full power when needed.

## 🆕 What's New vs Old Version

| Old (Pre‑release) | New (WASD) |
|-------------------|------------|
| Gas/Brake on mouse buttons | Gas/Brake on **`W`** / **`S`** |
| Static limiters (`Z/X/C`) | Dynamic limit via **`A`** / **`D`** |
| Limit must be held continuously | Limit adjusts and stays until pedals released |
| No auto‑reset | Limit **auto‑resets to 50%** when pedals released |

## ⌨️ Complete Keymap

| Key / Combo | Function |
|-------------|----------|
| **Mouse Move** | Steering (with FFB) |
| **`W`** | Smart Throttle – starts at 50%, smooth ramp |
| **`S`** | Smart Brake – starts at 50%, smooth ramp |
| **`A`** | Decrease throttle/brake limit (min 5%) |
| **`D`** | Increase throttle/brake limit (max 100%) |
| **`Shift` + `W`** | **Override:** instant 100% throttle |
| **`Shift` + `S`** | **Override:** instant 100% brake |
| **`LMB`** | **Panic Brake** – instant 100% (bypasses smoothing) |
| **`F` / `V`** | Shift Up / Down |
| **`Left Ctrl`** | Clutch |
| **`Caps Lock`** | Toggle shift assist (auto‑blip / manual) |
| **`B`** | Center steering wheel |
| **Mouse Button 4** | Toggle mouse lock |

## 🧠 How Smart Pedals Work

1. Press `W` or `S` → pedal **always starts at 50%** power.
2. While driving, tap `D` to raise the limit (e.g., 70% for more acceleration) or `A` to lower it.
3. Release both pedals → limit **automatically resets to 50%**. Every corner entry is predictable.
4. Need full power? Hold `Shift` + `W` for 100% throttle instantly.

## 🔧 Requirements

- [vJoy](https://sourceforge.net/projects/vjoystick/)
- [FreePIE](https://github.com/AndersMalmgren/FreePIE)
- Run FreePIE **as Administrator**

## 📥 Installation

1. Install vJoy and enable X, Y, Z, RX, RY, RZ axes.
2. Copy the script into FreePIE and run.
3. In Content Manager bind axes as in the old version.

---

*This version is experimental but fully playable. Feedback welcome!*
