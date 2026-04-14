# 🖱️ Assetto Corsa Mouse Steering with FFB and Dynamic Limiters

**Pre-release version.** Advanced FreePIE script that turns your mouse and keyboard into a precise sim racing controller with Force Feedback extracted directly from the game's physics.

## ✨ Features

- **Mouse Steering** with exponential curve (soft center, sharp edges)
- **Real Force Feedback** – reads `acpmf_physics` shared memory and applies self-aligning torque to your virtual wheel
- **Dynamic throttle/brake limiters** – hold `Z`, `X`, or `C` to cap input at 20%, 50%, or 80%
- **Mouse Wheel "Rope"** – fine‑tune throttle/brake by ±15% using the scroll wheel
- **Smooth pedal ramping** – no jerky on/off, weight transfer feels natural
- **Two shift modes** (toggle with `Caps Lock`): assisted (auto‑blip) or manual
- **Russian voice feedback** (optional) for mode changes
- **Mouse lock** – cursor is fixed to center while driving

## ⌨️ Default Controls

| Action | Key / Combo |
|--------|-------------|
| Steering | Move mouse left/right |
| Throttle | `LMB` (Left Mouse Button) |
| Brake | `RMB` (Right Mouse Button) |
| Clutch | `Left Ctrl` |
| Shift Up / Down | `F` / `V` |
| Limit 20% | `Z` (hold) |
| Limit 50% | `X` (hold) |
| Limit 80% | `C` (hold) |
| Throttle Trim + | Scroll Wheel Up |
| Throttle Trim – | Scroll Wheel Down |
| Center Steering | `B` |
| Toggle Mouse Lock | `M` |
| Toggle Shift Assist | `Caps Lock` |

## ⚙️ How Limiters Work

Hold `Z`, `X`, or `C` while pressing throttle/brake to cap input at the selected percentage.  
Example: `LMB` + `X` → throttle never exceeds 50%.  
Release the limiter key to instantly return to 100% capability.

## 🔧 Requirements

- [vJoy](https://sourceforge.net/projects/vjoystick/)
- [FreePIE](https://github.com/AndersMalmgren/FreePIE)
- Run FreePIE **as Administrator** (needed for shared memory access)

## 📥 Installation

1. Install vJoy and configure at least one virtual device with X, Y, Z, RX, RY, RZ axes.
2. Copy the script into FreePIE and run it.
3. In Content Manager, bind:
   - Steering → `vJoy X`
   - Throttle → `vJoy Y`
   - Brake → `vJoy Z`
   - Clutch → `vJoy RZ`

---

*This is the stable pre-release. An experimental WASD‑based version is coming soon.*
