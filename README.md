# 🖱️ Kali Cursor Master

![Version](https://img.shields.io/badge/version-3.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-555555?style=for-the-badge&logo=linux&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Stop struggling with manual cursor installation.** > Convert your favorite Windows cursors (`.cur`, `.ani`) to professional Linux themes in seconds.

---

## 🌟 Why Use This?
Linux uses a completely different cursor architecture (X11 bitmaps) than Windows (cur/ani). Manually converting these requires using complex command-line tools, calculating "hotspots" (the pixel where the click happens), and writing config files.

**Kali Cursor Master** automates the entire pipeline. It's a "Self-Healing" application that installs its own dependencies, fixes permission errors, and integrates directly into your desktop environment.

## ✨ Key Features

* **🛡️ Self-Healing Engine:** The app automatically detects missing system tools (`imagemagick`, `xcursorgen`) and installs them. It also auto-repairs folder permissions if they get locked.
* **🔄 Universal Converter:** Supports static `.cur` files AND fully animated `.ani` files.
* **🎯 Smart Hotspot Detection:** Automatically reads file metadata to find the perfect click-point.
* **📂 Theme Library:** Built-in manager to View, Apply, and Delete themes.
* **🔗 Deep Integration:** Installs themes to `~/.icons` and creates a Start Menu shortcut automatically.

---

## 📦 Installation

You don't need complex setup steps. Just download and run.

### Option 1: The One-Liner (Terminal)
```bash
git clone [https://github.com/YOUR_USERNAME/kali-cursor-master.git](https://github.com/YOUR_USERNAME/kali-cursor-master.git)
cd kali-cursor-master
chmod +x install.sh
./install.sh
