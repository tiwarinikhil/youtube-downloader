# 🎬 YouTube Downloader (yt-dlp GUI)

A modern desktop GUI for downloading YouTube **videos** and **playlists** using [yt-dlp](https://github.com/yt-dlp/yt-dlp), built with Python and Tkinter.

---

## ✨ Features
- 🎥 **Single Video or Playlist/Channel** mode (choose from UI).
- 🎚️ **Format selection** (resolution, codec, size).
- 🎧 **Audio only** downloads (MP3, M4A, WAV, Opus, FLAC).
- 📂 **Custom output folder** and container format (MP4, MKV, WEBM).
- 💬 **Subtitles** support (normal, auto, embed).
- 🖼️ **Thumbnail** download & embedding.
- ✅ Clean, modern Tkinter UI with dropdowns, checkboxes, and radio buttons.
- 🖱️ Inline status updates (no popups for format fetch).
- 🔗 Clickable **GitHub credits link**.

---

## 📦 Requirements
- Python **3.8+**
- `yt-dlp` (core downloader)
- `tkinter` (GUI)
- `ttk` (modern themed widgets, comes with tkinter)
- `ffmpeg` (for audio extraction, embedding thumbnails, etc.)

---

## 🛠️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/yt-dlp-gui.git
   cd yt-dlp-gui
   
2. **Create a virtual environment (optional but recommended)**
  '''bash
  python -m venv venv
  source venv/bin/activate   # On Linux/Mac
  venv\Scripts\activate      # On Windows


