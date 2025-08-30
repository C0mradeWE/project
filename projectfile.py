"""
یک ابزار ساده برای مرتب‌سازی فایل‌ها بر اساس تاریخ (نسخه گرافیکی)

- انتخاب پوشه ورودی و خروجی با پنجره
- امکان جابجایی (move) یا کپی (copy)
- ساخت پوشه‌های سال/ماه به صورت خودکار
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

# ساخت پوشه در صورت نبود
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

# مرتب‌سازی فایل‌ها
def organize_files(src: Path, dst: Path, strategy: str):
    if not src.exists() or not src.is_dir():
        messagebox.showerror("خطا", f"مسیر {src} معتبر نیست.")
        return 0

    count = 0
    for file in src.rglob("*"):  # شامل زیرپوشه‌ها
        if file.is_file():
            mtime = file.stat().st_mtime
            date = datetime.fromtimestamp(mtime)

            # مسیر خروجی به صورت سال/ماه
            subdir = dst / f"{date.year}" / f"{date.month:02d}"
            ensure_dir(subdir)

            target = subdir / file.name

            # اگر فایل تکراری بود، اسم جدید ساخته می‌شود
            i = 1
            while target.exists():
                target = subdir / f"{file.stem}_{i}{file.suffix}"
                i += 1

            if strategy == "move":
                shutil.move(str(file), str(target))
            else:
                shutil.copy2(str(file), str(target))

            count += 1
    return count

# اجرا شدن عملیات با دکمه
def run_sort():
    src = Path(src_var.get())
    dst = Path(dst_var.get())
    strategy = strategy_var.get()

    if not src or not dst:
        messagebox.showwarning("هشدار", "لطفاً پوشه‌ها را انتخاب کنید.")
        return

    count = organize_files(src, dst, strategy)
    messagebox.showinfo("پایان", f"✅ عملیات تمام شد. {count} فایل پردازش شد.")

# انتخاب پوشه ورودی
def browse_src():
    folder = filedialog.askdirectory()
    if folder:
        src_var.set(folder)

# انتخاب پوشه خروجی
def browse_dst():
    folder = filedialog.askdirectory()
    if folder:
        dst_var.set(folder)

# ساخت رابط گرافیکی
root = tk.Tk()
root.title("مرتب‌سازی فایل‌ها بر اساس تاریخ")
root.geometry("450x200")

src_var = tk.StringVar()
dst_var = tk.StringVar()
strategy_var = tk.StringVar(value="move")

tk.Label(root, text="پوشه ورودی:").pack(anchor="w", padx=10, pady=5)
frame1 = tk.Frame(root)
frame1.pack(fill="x", padx=10)
tk.Entry(frame1, textvariable=src_var, width=40).pack(side="left", fill="x", expand=True)
tk.Button(frame1, text="انتخاب", command=browse_src).pack(side="left", padx=5)

tk.Label(root, text="پوشه خروجی:").pack(anchor="w", padx=10, pady=5)
frame2 = tk.Frame(root)
frame2.pack(fill="x", padx=10)
tk.Entry(frame2, textvariable=dst_var, width=40).pack(side="left", fill="x", expand=True)
tk.Button(frame2, text="انتخاب", command=browse_dst).pack(side="left", padx=5)

tk.Label(root, text="روش: (move یا copy)").pack(anchor="w", padx=10, pady=5)
tk.Entry(root, textvariable=strategy_var, width=20).pack(padx=10, anchor="w")

tk.Button(root, text="شروع مرتب‌سازی", command=run_sort, bg="green", fg="white").pack(pady=20)

root.mainloop()

#ببخشید یکم از کتابی که معرفی کردید کمک گرفتم
# امیدوارم خوشتون بیاد
