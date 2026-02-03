# 🖱️ Kali Cursor Master

![Version](https://img.shields.io/badge/version-3.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-555555?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)

> **Stop struggling with manual cursor installation.** > Bridge the gap between Windows and Linux customization. Instantly convert professional Windows cursor packs (`.cur`, `.ani`) into native X11 Linux themes with a single click.

---

## 📸 Screenshots & Gallery

| **Theme Creator** | **Theme Library** |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/462e2808-8c64-43f5-8962-427cdd5faf2c" width="400" alt="Theme Creator Interface"> | <img src="https://github.com/user-attachments/assets/ac3e7838-14d0-4f52-baa4-a6d74bcedf6a" width="400" alt="Library Interface"> |

<details>
<summary><strong>View Full Application Preview</strong></summary>
<br>
<img src="https://github.com/user-attachments/assets/d6db72c1-ef23-480f-bbbc-731d6eec9ddb" width="800" alt="Full App Screenshot">
<br>
<img src="https://github.com/user-attachments/assets/9d72b586-2174-4862-aaea-e520363d2025" width="800" alt="Mobile View">
</details>

---

## 🌟 Why Use This?

Linux uses a completely different cursor architecture (**X11 bitmaps**) than Windows (**cur/ani** binaries).
Traditionally, porting a cursor theme involves:
1.  Using complex CLI tools like `imagemagick` to extract frames.
2.  Manually calculating "hotspots" (the exact pixel coordinate where a click registers).
3.  Writing tedious `.theme` and config files for every single cursor state.

**Kali Cursor Master** automates the entire pipeline. It serves as a GUI wrapper that handles binary conversion, hotspot calculation, permission management, and system integration.

---

## ✨ Key Features

### 🛡️ Self-Healing Engine
The app is built to be unbreakable. On every launch, it runs a diagnostic check:
* **Dependency Check:** Automatically detects if `imagemagick` or `xcursorgen` are missing and installs them via `apt`.
* **Permission Fixer:** If your `~/.icons` folder becomes locked or owned by root, the app automatically repairs ownership so you can save themes.

### 🔄 Universal Conversion
* **Static Cursors:** Converts standard `.cur` files instantly.
* **Animated Cursors:** Explodes `.ani` files into individual frames, preserves frame delays, and recompiles them into X11 animations.

### 🎯 Smart Hotspot Detection
Precision matters. The app reads the binary metadata of the Windows file to find the exact *X,Y* coordinates of the hotspot.
* *Fallback Logic:* If metadata is missing, it intelligently centers the hotspot based on the cursor role (e.g., "Busy" is centered, "Arrow" is top-left).

### 🔗 Deep System Integration
* Installs themes directly to the user space: `~/.icons/`.
* Auto-generates a **Start Menu Shortcut** (Application Entry).
* Updates the GNOME/XFCE registry immediately upon application.

---

## 📦 Installation

### Prerequisites
* Kali Linux (or any Debian/Ubuntu-based distro).
* Python 3.x (Pre-installed on Kali).
* `sudo` access (for installing backend tools).
