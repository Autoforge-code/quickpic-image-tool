import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image

SUPPORTED_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff")

def resource_path(relative_path):
    """适配 PyInstaller 单文件打包资源提取"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BatchImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Image Resizer & Converter - Quick Pro")
        self.root.geometry("560x520")
        self.root.resizable(False, False)

        # 尝试设置窗口图标
        icon_path = resource_path("app_icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        self.bg_color = "#f8fafc"
        self.root.configure(bg=self.bg_color)
        
        self.is_processing = False
        self.setup_ui()

    def setup_ui(self):
        # 1. 顶部标头
        header = tk.Label(
            self.root, 
            text="Batch Image Resizer & Optimizer", 
            font=("Segoe UI", 15, "bold"), 
            bg=self.bg_color, 
            fg="#0f172a"
        )
        header.pack(pady=(15, 2))
        
        sub = tk.Label(
            self.root, 
            text="Bulk convert, compress, and resize images for web & e-commerce", 
            font=("Segoe UI", 9), 
            bg=self.bg_color, 
            fg="#64748b"
        )
        sub.pack(pady=(0, 12))

        # 2. 文件夹路径选择
        path_frame = tk.LabelFrame(self.root, text=" Directory Selection ", font=("Segoe UI", 9, "bold"), bg=self.bg_color)
        path_frame.pack(fill="x", padx=25, pady=5)

        # 源文件夹
        tk.Label(path_frame, text="Source Folder:", bg=self.bg_color).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.src_entry = tk.Entry(path_frame, width=42, relief="solid", bd=1)
        self.src_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(path_frame, text="Browse...", command=self.browse_src, relief="groove").grid(row=0, column=2, padx=5, pady=5)

        # 输出文件夹
        tk.Label(path_frame, text="Output Folder:", bg=self.bg_color).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.dst_entry = tk.Entry(path_frame, width=42, relief="solid", bd=1)
        self.dst_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(path_frame, text="Browse...", command=self.browse_dst, relief="groove").grid(row=1, column=2, padx=5, pady=5)

        # 3. 转换设置区域
        cfg_frame = tk.LabelFrame(self.root, text=" Conversion Settings ", font=("Segoe UI", 9, "bold"), bg=self.bg_color)
        cfg_frame.pack(fill="x", padx=25, pady=10)

        # 目标格式
        tk.Label(cfg_frame, text="Target Format:", bg=self.bg_color).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.format_var = tk.StringVar(value="WEBP")
        format_cb = ttk.Combobox(cfg_frame, textvariable=self.format_var, values=["WEBP", "JPEG", "PNG"], state="readonly", width=12)
        format_cb.grid(row=0, column=1, sticky="w", padx=5, pady=8)

        # 压缩质量 (针对 JPG/WEBP)
        tk.Label(cfg_frame, text="Quality (1-100):", bg=self.bg_color).grid(row=0, column=2, sticky="w", padx=15, pady=8)
        self.quality_var = tk.IntVar(value=80)
        self.quality_scale = tk.Scale(cfg_frame, from_=10, to=100, orient="horizontal", variable=self.quality_var, bg=self.bg_color, bd=0, highlightthickness=0)
        self.quality_scale.grid(row=0, column=3, sticky="we", padx=5, pady=8)

        # 尺寸调节模式
        tk.Label(cfg_frame, text="Resize Mode:", bg=self.bg_color).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.resize_mode = tk.StringVar(value="original")
        
        mode_cb = ttk.Combobox(
            cfg_frame, 
            textvariable=self.resize_mode, 
            values=["original", "max_edge", "percentage"], 
            state="readonly", 
            width=12
        )
        mode_cb.grid(row=1, column=1, sticky="w", padx=5, pady=8)
        mode_cb.bind("<<ComboboxSelected>>", self.on_mode_change)

        # 尺寸参数输入
        self.param_label = tk.Label(cfg_frame, text="Parameter:", bg=self.bg_color)
        self.param_label.grid(row=1, column=2, sticky="w", padx=15, pady=8)
        self.param_entry = tk.Entry(cfg_frame, width=10, relief="solid", bd=1)
        self.param_entry.grid(row=1, column=3, sticky="w", padx=5, pady=8)
        self.param_entry.insert(0, "1200")
        self.param_entry.config(state="disabled")

        # 4. 执行区域
        self.start_btn = tk.Button(
            self.root, 
            text="🚀 Start Batch Processing", 
            font=("Segoe UI", 11, "bold"), 
            bg="#2563eb", 
            fg="white", 
            activebackground="#1d4ed8", 
            relief="flat", 
            cursor="hand2", 
            command=self.start_process_thread
        )
        self.start_btn.pack(pady=(10, 5), ipadx=20, ipady=6)

        # 5. 进度条与状态展示
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=510, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.status_lbl = tk.Label(self.root, text="Ready to optimize images", font=("Segoe UI", 9), bg=self.bg_color, fg="#64748b")
        self.status_lbl.pack()

    def on_mode_change(self, event=None):
        mode = self.resize_mode.get()
        if mode == "original":
            self.param_entry.config(state="disabled")
            self.param_label.config(text="Parameter:")
        elif mode == "max_edge":
            self.param_entry.config(state="normal")
            self.param_entry.delete(0, tk.END)
            self.param_entry.insert(0, "1200")
            self.param_label.config(text="Max Pixels:")
        elif mode == "percentage":
            self.param_entry.config(state="normal")
            self.param_entry.delete(0, tk.END)
            self.param_entry.insert(0, "50")
            self.param_label.config(text="Scale (%):")

    def browse_src(self):
        folder = filedialog.askdirectory()
        if folder:
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, folder)
            if not self.dst_entry.get():
                self.dst_entry.insert(0, os.path.join(folder, "Optimized_Output"))

    def browse_dst(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dst_entry.delete(0, tk.END)
            self.dst_entry.insert(0, folder)

    def start_process_thread(self):
        if self.is_processing:
            return
        src = self.src_entry.get().strip()
        dst = self.dst_entry.get().strip()

        if not os.path.exists(src):
            messagebox.showwarning("Warning", "Please select a valid source directory!")
            return
        if not dst:
            messagebox.showwarning("Warning", "Please specify an output directory!")
            return

        self.is_processing = True
        self.start_btn.config(state="disabled", bg="#94a3b8")
        threading.Thread(target=self.process_images, args=(src, dst), daemon=True).start()

    def process_images(self, src, dst):
        os.makedirs(dst, exist_ok=True)
        img_files = [f for f in os.listdir(src) if f.lower().endswith(SUPPORTED_EXTS)]
        total = len(img_files)

        if total == 0:
            self.root.after(0, self.update_status, "No supported images found in directory.", 0)
            self.root.after(0, self.finish_processing, 0)
            return

        fmt = self.format_var.get()
        quality = self.quality_var.get()
        mode = self.resize_mode.get()
        param_val = self.param_entry.get().strip()
        
        try:
            param_num = int(param_val) if param_val else 100
        except ValueError:
            param_num = 100

        processed = 0

        def process_single(file_name):
            in_path = os.path.join(src, file_name)
            base_name, _ = os.path.splitext(file_name)
            
            ext_map = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}
            out_ext = ext_map.get(fmt, ".jpg")
            out_path = os.path.join(dst, f"{base_name}{out_ext}")

            try:
                with Image.open(in_path) as im:
                    w, h = im.size
                    
                    # 尺寸计算
                    if mode == "max_edge" and param_num > 0:
                        max_edge = max(w, h)
                        if max_edge > param_num:
                            ratio = param_num / max_edge
                            new_size = (int(w * ratio), int(h * ratio))
                            im = im.resize(new_size, Image.Resampling.LANCZOS)
                    elif mode == "percentage" and 0 < param_num < 1000:
                        ratio = param_num / 100.0
                        new_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
                        im = im.resize(new_size, Image.Resampling.LANCZOS)

                    # 格式与通道转换 (解决透明 PNG 转 JPG 报错或发黑)
                    if fmt == "JPEG":
                        if im.mode in ("RGBA", "LA", "P"):
                            bg = Image.new("RGB", im.size, (255, 255, 255))
                            bg.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
                            im = bg
                        elif im.mode != "RGB":
                            im = im.convert("RGB")
                        im.save(out_path, "JPEG", quality=quality, optimize=True)
                    
                    elif fmt == "WEBP":
                        im.save(out_path, "WEBP", quality=quality, method=4)
                    
                    elif fmt == "PNG":
                        im.save(out_path, "PNG", optimize=True)

                return True
            except Exception:
                return False

        # 多线程处理池
        with ThreadPoolExecutor(max_workers=4) as executor:
            for success in executor.map(process_single, img_files):
                if success:
                    processed += 1
                progress = int((processed / total) * 100)
                self.root.after(0, self.update_status, f"Processing: {processed}/{total} files...", progress)

        self.root.after(0, self.finish_processing, processed)

    def update_status(self, text, progress):
        self.status_lbl.config(text=text, fg="#0f172a")
        self.progress_bar["value"] = progress

    def finish_processing(self, count):
        self.is_processing = False
        self.start_btn.config(state="normal", bg="#2563eb")
        self.status_lbl.config(text=f"Done! Successfully processed {count} image(s).", fg="#16a34a")
        messagebox.showinfo("Finished", f"Operation completed!\nProcessed {count} images.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BatchImageApp(root)
    root.mainloop()