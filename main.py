#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import re
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# --- CONFIGURATION ---
HOME = Path.home()
ICON_DIR = HOME / ".icons"
APP_DIR = HOME / ".local/share/applications"
ASSET_DIR = HOME / ".local/share/icons"
THEME_COLOR = "#663399"  # Kali Purple
BG_COLOR = "#1f1f2e"
FG_COLOR = "white"

# --- ROLES ---
ROLES = {
    "Normal": ["left_ptr", "default", "arrow", "top_left_arrow"],
    "Link": ["hand2", "hand", "pointer", "hand1"],
    "Working": ["left_ptr_watch", "progress"],
    "Busy": ["watch", "wait"],
    "Text": ["xterm", "text", "ibeam"],
    "Precision": ["crosshair", "cross"],
    "Unavailable": ["dnd-none", "circle", "not-allowed"],
    "Resize V": ["sb_v_double_arrow", "v_double_arrow", "ns-resize"],
    "Resize H": ["sb_h_double_arrow", "h_double_arrow", "ew-resize"],
    "Move": ["fleur", "move", "all-scroll"],
    "Help": ["question_arrow", "help"]
}

APP_ICON = """<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#d4aaff;stop-opacity:1"/><stop offset="100%" style="stop-color:#4d0099;stop-opacity:1"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="#1a1a20"/><path d="M22 14L22 48L30 40L38 54L44 50L36 36L48 36Z" fill="url(#g)" stroke="white" stroke-width="2"/></svg>"""

class SelfHealer:
    @staticmethod
    def check_system():
        issues = []
        # Check 1: Dependencies
        if not shutil.which("convert") or not shutil.which("xcursorgen"):
            issues.append("MISSING_DEPS")
        
        # Check 2: Permissions
        if ICON_DIR.exists() and not os.access(ICON_DIR, os.W_OK):
            issues.append("PERM_DENIED")
            
        return issues

    @staticmethod
    def fix_issues(root, issues):
        if "MISSING_DEPS" in issues:
            ans = messagebox.askyesno("System Repair", "Missing core tools (ImageMagick). Install them now?")
            if ans:
                cmd = "sudo apt update && sudo apt install -y python3-tk imagemagick x11-apps"
                subprocess.run(["x-terminal-emulator", "-e", f"bash -c '{cmd}; read -p \"Done. Press Enter...\"'"])
                
        if "PERM_DENIED" in issues:
            ans = messagebox.askyesno("Permission Repair", "Your icon folder is locked. Fix permissions?")
            if ans:
                user = os.environ.get('USER')
                cmd = f"sudo chown -R {user}:{user} {HOME}/.icons && chmod -R 755 {HOME}/.icons"
                subprocess.run(["x-terminal-emulator", "-e", f"bash -c '{cmd}; read -p \"Fixed. Press Enter...\"'"])

class Converter:
    @staticmethod
    def process(src, out, name):
        tmp = out / f"tmp_{name}"
        try:
            if tmp.exists(): shutil.rmtree(tmp)
            tmp.mkdir(parents=True)
            # Use ImageMagick to explode cursor into frames
            subprocess.run(["convert", src, "-coalesce", str(tmp/"f.png")], check=True, stderr=subprocess.DEVNULL)
            
            # Find Hotspot
            hotspot = None
            try:
                res = subprocess.run(["identify", "-verbose", src], capture_output=True, text=True)
                m = re.search(r"cursor:hotspot:\s*(\d+),(\d+)", res.stdout)
                if m: hotspot = (int(m.group(1)), int(m.group(2)))
            except: pass

            frames = sorted(list(tmp.glob("f*.png")))
            if not frames: return False

            lines = []
            for f in frames:
                if hotspot: x, y = hotspot
                else:
                    d = subprocess.check_output(["identify", "-format", "%w %h", f]).decode().split()
                    w, h = int(d[0]), int(d[1])
                    if any(k in name for k in ["left_ptr", "arrow", "hand"]): x, y = 0, 0
                    else: x, y = w//2, h//2
                lines.append(f"32 {x} {y} {f.name} 50")
            
            with open(tmp/"c.conf", "w") as f: f.write("\n".join(lines))
            subprocess.run(["xcursorgen", str(tmp/"c.conf"), str(out/name)], cwd=tmp, check=True, stderr=subprocess.DEVNULL)
            shutil.rmtree(tmp)
            return True
        except:
            if tmp.exists(): shutil.rmtree(tmp)
            return False

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kali Cursor Master (v3.0)")
        self.geometry("900x700")
        self.configure(bg=BG_COLOR)
        self.map = {}
        
        # --- SELF HEAL ON START ---
        self.ensure_resources()
        issues = SelfHealer.check_system()
        if issues: SelfHealer.fix_issues(self, issues)
        
        self.setup_ui()

    def ensure_resources(self):
        # Auto-create .desktop and icon if missing
        if not ICON_DIR.exists(): ICON_DIR.mkdir()
        if not ASSET_DIR.exists(): ASSET_DIR.mkdir(parents=True)
        if not APP_DIR.exists(): APP_DIR.mkdir(parents=True)
        
        svg_path = ASSET_DIR / "cursor-master.svg"
        if not svg_path.exists():
            with open(svg_path, "w") as f: f.write(APP_ICON)
            
        desk_path = APP_DIR / "cursor-master.desktop"
        if not desk_path.exists():
            with open(desk_path, "w") as f:
                f.write(f"[Desktop Entry]\nName=Cursor Master\nExec={sys.executable} {os.path.abspath(__file__)}\nIcon={svg_path}\nType=Application\nCategories=Settings;")
            desk_path.chmod(0o755)

    def setup_ui(self):
        s = ttk.Style(); s.theme_use('clam')
        s.configure("TFrame", background=BG_COLOR)
        s.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Segoe UI", 10))
        s.configure("TButton", background=THEME_COLOR, foreground="white", borderwidth=0)
        s.configure("TNotebook", background=BG_COLOR, borderwidth=0)
        s.map("TNotebook.Tab", background=[("selected", THEME_COLOR)], foreground=[("selected", "white")])

        nb = ttk.Notebook(self); nb.pack(fill="both", expand=True, padx=10, pady=10)
        
        # TAB 1: BUILD
        f1 = ttk.Frame(nb); nb.add(f1, text="  Create Theme  ")
        cv = tk.Canvas(f1, bg=BG_COLOR, highlightthickness=0)
        sb = ttk.Scrollbar(f1, command=cv.yview)
        sf = ttk.Frame(cv); cv.create_window((0,0), window=sf, anchor="nw")
        sf.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
        cv.configure(yscrollcommand=sb.set)
        cv.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        sb.pack(side="right", fill="y", pady=10)
        
        self.lbls = {}
        for r in ROLES:
            row = ttk.Frame(sf); row.pack(fill="x", pady=4)
            ttk.Label(row, text=r, width=20).pack(side="left")
            ttk.Button(row, text="Browse", width=8, command=lambda x=r: self.pick(x)).pack(side="left")
            l = ttk.Label(row, text="Default", foreground="#666"); l.pack(side="left", padx=10)
            self.lbls[r] = l
            
        bot = ttk.Frame(f1, padding=10); bot.pack(fill="x")
        ttk.Label(bot, text="Name:").pack(side="left")
        self.name = tk.Entry(bot, bg="#333", fg="white"); self.name.pack(side="left", padx=5)
        self.name.insert(0, "My-New-Cursor")
        ttk.Button(bot, text="BUILD & INSTALL", command=self.build).pack(side="right")

        # TAB 2: LIBRARY
        f2 = ttk.Frame(nb, padding=10); nb.add(f2, text="  My Library  ")
        self.lst = tk.Listbox(f2, bg="#2a2a35", fg="white", selectbackground=THEME_COLOR, relief="flat", font=("Segoe UI", 12))
        self.lst.pack(fill="both", expand=True, pady=(0, 10))
        bb = ttk.Frame(f2); bb.pack(fill="x")
        ttk.Button(bb, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(bb, text="DELETE", command=self.delete_theme).pack(side="right", padx=5)
        ttk.Button(bb, text="APPLY", command=self.apply).pack(side="right")
        self.refresh()

    def pick(self, r):
        p = filedialog.askopenfilename(filetypes=[("Cursors", "*.cur *.ani")])
        if p: self.map[r] = p; self.lbls[r].config(text=os.path.basename(p), foreground="#0f0")

    def build(self):
        nm = self.name.get().strip().replace(" ", "-")
        if not nm or not self.map: return messagebox.showerror("Error", "Missing Name or Files")
        
        td = ICON_DIR / nm; cd = td / "cursors"
        try:
            if td.exists(): shutil.rmtree(td)
            cd.mkdir(parents=True)
            
            # Progress Window
            pw = tk.Toplevel(self); pw.geometry("300x100"); pw.title("Working...")
            pl = ttk.Label(pw, text="Converting...", anchor="center"); pl.pack(expand=True)
            self.update()
            
            cnt = 0
            for r, p in self.map.items():
                pl.config(text=f"Processing {r}..."); self.update()
                mn = ROLES[r][0]
                if Converter.process(p, cd, mn):
                    for a in ROLES[r][1:]: shutil.copy(cd/mn, cd/a)
                    cnt += 1
            
            with open(td/"index.theme", "w") as f: f.write(f"[Icon Theme]\nName={nm}\nInherits=core")
            pw.destroy()
            messagebox.showinfo("Success", f"Theme '{nm}' created with {cnt} cursors!"); self.refresh()
            self.map = {}; self.setup_ui() # Reset UI
        except Exception as e: messagebox.showerror("Error", str(e))

    def refresh(self):
        self.lst.delete(0, tk.END)
        if ICON_DIR.exists():
            for x in ICON_DIR.iterdir(): 
                if x.is_dir(): self.lst.insert(tk.END, x.name)

    def apply(self):
        if not self.lst.curselection(): return
        n = self.lst.get(self.lst.curselection()[0])
        # Force update multiple ways
        cmds = [
            ["xfconf-query", "-c", "xsettings", "-p", "/Gtk/CursorThemeName", "-s", n],
            ["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", n]
        ]
        for c in cmds:
            try: subprocess.run(c, stderr=subprocess.DEVNULL)
            except: pass
        messagebox.showinfo("Applied", f"Theme: {n}\n\nNote: If not changed, Log Out & In.")

    def delete_theme(self):
        sel = self.lst.curselection()
        if not sel: return
        n = self.lst.get(sel[0])
        if messagebox.askyesno("Confirm", f"Delete {n}?"): shutil.rmtree(ICON_DIR/n); self.refresh()

if __name__ == "__main__":
    App().mainloop()