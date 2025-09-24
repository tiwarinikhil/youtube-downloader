import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from backend import list_formats, download_video

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def fetch_formats():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL first")
        return
    try:
        formats = list_formats(url)
        if not formats:
            format_status.config(text="❌ No formats found.", foreground="red")
            return

        format_map.clear()
        format_dropdown["values"] = []
        for label, fmt_id in formats:
            format_map[label] = fmt_id
            format_dropdown["values"] = (*format_dropdown["values"], label)

        format_var.set(list(format_map.keys())[0])  # default
        format_status.config(text=f"✅ {len(format_map)} formats loaded.", foreground="green")
    except Exception as e:
        format_status.config(text=f"❌ Error: {e}", foreground="red")

def start_download():
    url = url_entry.get().strip()
    output_folder = folder_var.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    chosen_label = format_var.get()
    fmt = format_map.get(chosen_label, "bestvideo+bestaudio/best")

    try:
        download_video(
            url=url,
            fmt=fmt,
            output_folder=output_folder,
            audio_only=audio_only_var.get(),
            codec=codec_var.get(),
            quality=quality_var.get(),
            subtitles=subs_var.get(),
            auto_subs=auto_subs_var.get(),
            playlist=(mode_var.get() == "playlist"),  # 👈 Radio button decides mode
            embed_subs=embed_subs_var.get(),
            thumb=thumb_var.get(),
            embed_thumb=embed_thumb_var.get(),
            container=container_var.get()
        )
        messagebox.showinfo("Success", "✅ Download completed!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- UI ----------------
root = tk.Tk()
root.title("🎬 YouTube Downloader")
root.geometry("600x640")
root.configure(bg="#f4f6f9")

# Style
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10), background="#f4f6f9")
style.configure("TCheckbutton", background="#f4f6f9")
style.configure("TRadiobutton", background="#f4f6f9")

# Title
title_label = tk.Label(root, text="🎥 YouTube Downloader", font=("Segoe UI", 16, "bold"), bg="#f4f6f9")
title_label.pack(pady=10)

# URL Frame
url_frame = ttk.LabelFrame(root, text="Video URL")
url_frame.pack(fill="x", padx=10, pady=5)

url_entry = ttk.Entry(url_frame, width=65)
url_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
ttk.Button(url_frame, text="Get Formats", command=fetch_formats).grid(row=0, column=1, padx=5, pady=5)

format_status = tk.Label(url_frame, text="", font=("Segoe UI", 9), bg="#f4f6f9", fg="gray")
format_status.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(0,5))

# Mode Frame (Single vs Playlist)
mode_frame = ttk.LabelFrame(root, text="Mode")
mode_frame.pack(fill="x", padx=10, pady=5)

mode_var = tk.StringVar(value="single")  # default = single video
ttk.Radiobutton(mode_frame, text="Single Video", variable=mode_var, value="single").grid(row=0, column=0, padx=10, pady=5, sticky="w")
ttk.Radiobutton(mode_frame, text="Playlist/Channel", variable=mode_var, value="playlist").grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Format Frame
format_frame = ttk.LabelFrame(root, text="Format Selection")
format_frame.pack(fill="x", padx=10, pady=5)

format_var = tk.StringVar()
format_map = {}
format_dropdown = ttk.Combobox(format_frame, textvariable=format_var, state="readonly", width=55)
format_dropdown.grid(row=0, column=0, padx=5, pady=5)

# Output Frame
folder_frame = ttk.LabelFrame(root, text="Output")
folder_frame.pack(fill="x", padx=10, pady=5)

folder_var = tk.StringVar(value=os.getcwd())
ttk.Label(folder_frame, textvariable=folder_var).grid(row=0, column=0, padx=5, pady=5, sticky="w")
ttk.Button(folder_frame, text="Choose Folder", command=choose_folder).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(folder_frame, text="Container:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
container_var = tk.StringVar(value="mp4")
ttk.Combobox(folder_frame, textvariable=container_var, values=["mp4", "mkv", "webm"], state="readonly", width=10)\
    .grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Options Frame
options_frame = ttk.LabelFrame(root, text="Options")
options_frame.pack(fill="x", padx=10, pady=5)

subs_var = tk.BooleanVar()
auto_subs_var = tk.BooleanVar()
embed_subs_var = tk.BooleanVar()
thumb_var = tk.BooleanVar()
embed_thumb_var = tk.BooleanVar()

for i, (text, var) in enumerate([
    ("Download Subtitles", subs_var),
    ("Auto Subtitles", auto_subs_var),
    ("Embed Subtitles", embed_subs_var),
    ("Download Thumbnail", thumb_var),
    ("Embed Thumbnail", embed_thumb_var),
]):
    ttk.Checkbutton(options_frame, text=text, variable=var).grid(row=i//2, column=i%2, sticky="w", padx=10, pady=3)

# Audio Frame
audio_frame = ttk.LabelFrame(root, text="Audio Options")
audio_frame.pack(fill="x", padx=10, pady=5)

audio_only_var = tk.BooleanVar()
ttk.Checkbutton(audio_frame, text="Audio Only", variable=audio_only_var).grid(row=0, column=0, sticky="w", padx=10, pady=3)

ttk.Label(audio_frame, text="Codec:").grid(row=1, column=0, sticky="w", padx=10)
codec_var = tk.StringVar(value="mp3")
ttk.Combobox(audio_frame, textvariable=codec_var, values=["mp3", "m4a", "wav", "opus", "flac"],
             state="readonly", width=10).grid(row=1, column=1, padx=5, pady=3)

ttk.Label(audio_frame, text="Quality (kbps):").grid(row=2, column=0, sticky="w", padx=10)
quality_var = tk.StringVar(value="192")
ttk.Combobox(audio_frame, textvariable=quality_var, values=["64", "128", "192", "256", "320"],
             state="readonly", width=10).grid(row=2, column=1, padx=5, pady=3)

# Download Button
ttk.Button(root, text="🚀 Download", command=start_download).pack(pady=15)

# Credits
credits = tk.Label(root, text="Made with ❤️  |  GitHub: https://github.com/tiwarinikhil",
                   font=("Segoe UI", 9), fg="gray", bg="#f4f6f9", cursor="hand2")
credits.pack(pady=5)

def open_github(event):
    import webbrowser
    webbrowser.open("https://github.com/tiwarinikhil")

credits.bind("<Button-1>", open_github)

root.mainloop()
