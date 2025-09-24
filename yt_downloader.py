# import os
# import argparse
# from yt_dlp import YoutubeDL

# def list_formats(url):
#     """List available formats for a given YouTube URL."""
#     ydl_opts = {"quiet": True}
#     with YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=False)
#         formats = info.get("formats", [])
#         print("\n📺 Available formats:")
#         print("=" * 80)
#         for f in formats:
#             fmt_id = f.get("format_id")
#             ext = f.get("ext")
#             resolution = f.get("resolution") or f"{f.get('height','?')}p"
#             fps = f.get("fps", "")
#             size = f.get("filesize") or f.get("filesize_approx")
#             size_mb = f"{round(size/1024/1024,1)} MB" if size else "?"
#             print(f"{fmt_id:<6} | {ext:<4} | {resolution:<6} {fps}fps | {size_mb}")
#         print("=" * 80)

# def download_video(url, fmt, output_folder, audio_only, codec, quality, subtitles, auto_subs, playlist):
#     """Download video/audio using yt-dlp with given options."""
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     ydl_opts = {
#         "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
#         "ignoreerrors": True,
#         "noplaylist": not playlist,
#     }

#     if audio_only:
#         ydl_opts["format"] = "bestaudio/best"
#         ydl_opts["postprocessors"] = [{
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": codec,
#             "preferredquality": quality
#         }]
#     else:
#         ydl_opts["format"] = fmt or "bestvideo+bestaudio/best"
#         ydl_opts["merge_output_format"] = "mp4"

#     if subtitles:
#         ydl_opts["writesubtitles"] = True
#     if auto_subs:
#         ydl_opts["writeautomaticsub"] = True

#     with YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="YouTube Downloader (yt-dlp CLI wrapper)")

#     parser.add_argument("url", help="YouTube video/playlist/channel URL")
#     parser.add_argument("-f", "--format", help="Format ID (e.g. 136) or yt-dlp format string", default=None)
#     parser.add_argument("-o", "--output", help="Output folder", default="downloads")
#     parser.add_argument("--audio-only", help="Download audio only", action="store_true")
#     parser.add_argument("--codec", help="Audio codec (mp3/m4a/wav/opus/flac)", default="mp3")
#     parser.add_argument("--quality", help="Audio quality (e.g. 64,128,192,320 kbps)", default="192")
#     parser.add_argument("--subtitles", help="Download subtitles if available", action="store_true")
#     parser.add_argument("--auto-subs", help="Download auto-generated subtitles", action="store_true")
#     parser.add_argument("--playlist", help="Download full playlist/channel if link supports it", action="store_true")
#     parser.add_argument("--list-formats", help="List available formats for this video", action="store_true")

#     args = parser.parse_args()

#     if args.list_formats:
#         list_formats(args.url)
#     else:
#         download_video(
#             url=args.url,
#             fmt=args.format,
#             output_folder=args.output,
#             audio_only=args.audio_only,
#             codec=args.codec,
#             quality=args.quality,
#             subtitles=args.subtitles,
#             auto_subs=args.auto_subs,
#             playlist=args.playlist,
#         )


import os
import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def fetch_formats():
    """Fetch available formats for the given URL and update dropdown"""
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL first")
        return

    try:
        ydl_opts = {'quiet': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])

        if not formats:
            messagebox.showerror("Error", "No formats found for this video.")
            return

        # Clear old dropdown menu
        menu = format_dropdown["menu"]
        menu.delete(0, "end")

        format_map.clear()

        # Populate dropdown with available formats
        for f in formats:
            fmt_id = f.get("format_id")
            ext = f.get("ext")
            resolution = f.get("resolution") or f"{f.get('height', 'N/A')}p"
            fps = f.get("fps", "")
            size = f.get("filesize") or f.get("filesize_approx")
            size_mb = f"{round(size/1024/1024,1)} MB" if size else "?"
            label = f"{fmt_id} | {ext} | {resolution} {fps}fps | {size_mb}"

            format_map[label] = fmt_id
            menu.add_command(
                label=label,
                command=lambda val=fmt_id: format_var.set(val)
            )

        # Set default to bestvideo+bestaudio
        format_var.set("bestvideo+bestaudio/best")

        messagebox.showinfo("Formats Loaded", f"Found {len(format_map)} formats. Select one from the dropdown.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch formats: {e}")

def download_video():
    url = url_entry.get().strip()
    output_folder = folder_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fmt = format_var.get()  # This will now be just the format_id

    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'format': fmt,
        'merge_output_format': container_var.get(),
        'ignoreerrors': True,
        'noplaylist': not playlist_var.get(),
        'writesubtitles': subs_var.get(),
        'writeautomaticsub': auto_subs_var.get(),
        'embedsubtitles': embed_subs_var.get(),
        'writethumbnail': thumb_var.get(),
        'embedthumbnail': embed_thumb_var.get(),
    }

    if audio_only_var.get():
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec_var.get(),
            'preferredquality': quality_var.get()
        }]

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "✅ Download completed!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- UI ----------------
root = tk.Tk()
root.title("YouTube Downloader (yt-dlp)")
root.geometry("600x650")

# URL
tk.Label(root, text="YouTube URL:").pack()
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Button to fetch formats
tk.Button(root, text="🔍 Get Available Formats", command=fetch_formats, bg="blue", fg="white").pack(pady=5)

# Format dropdown (dynamic)
format_var = tk.StringVar(value="")
format_map = {}
tk.Label(root, text="Select Format:").pack()
format_dropdown = tk.OptionMenu(root, format_var, "")
format_dropdown.pack()

# Output folder
tk.Button(root, text="Choose Output Folder", command=choose_folder).pack()
folder_var = tk.StringVar(value=os.getcwd())
tk.Label(root, textvariable=folder_var, fg="gray").pack()

# Container dropdown
container_var = tk.StringVar(value="mp4")
tk.Label(root, text="Output Container:").pack()
tk.OptionMenu(root, container_var, "mp4", "mkv", "webm").pack()

# Playlist
playlist_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Download Playlist/Channel (if available)", variable=playlist_var).pack()

# Subtitles
subs_var = tk.BooleanVar(value=False)
auto_subs_var = tk.BooleanVar(value=False)
embed_subs_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Download Subtitles", variable=subs_var).pack()
tk.Checkbutton(root, text="Download Auto-Subtitles", variable=auto_subs_var).pack()
tk.Checkbutton(root, text="Embed Subtitles", variable=embed_subs_var).pack()

# Thumbnails
thumb_var = tk.BooleanVar(value=False)
embed_thumb_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Download Thumbnail", variable=thumb_var).pack()
tk.Checkbutton(root, text="Embed Thumbnail", variable=embed_thumb_var).pack()

# Audio
tk.Label(root, text="\n🎵 Audio Options").pack()
audio_only_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Audio Only", variable=audio_only_var).pack()
codec_var = tk.StringVar(value="mp3")
quality_var = tk.StringVar(value="192")
tk.Label(root, text="Audio Codec:").pack()
tk.OptionMenu(root, codec_var, "mp3", "m4a", "wav", "opus", "flac").pack()
tk.Label(root, text="Audio Quality (kbps):").pack()
tk.OptionMenu(root, quality_var, "64", "128", "192", "256", "320").pack()

# Download Button
tk.Button(root, text="🚀 Download", command=download_video, bg="green", fg="white").pack(pady=20)

root.mainloop()
