import os
from yt_dlp import YoutubeDL

def list_formats(url):
    """Return available formats for a given YouTube or playlist URL as (label, id) tuples."""
    ydl_opts = {"quiet": True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # If it's a playlist, take the first video
    if "entries" in info:
        info = info["entries"][0]  # pick first video in playlist

    formats = info.get("formats", [])
    results = []
    for f in formats:
        fmt_id = f.get("format_id")
        ext = f.get("ext")
        resolution = f.get("resolution") or f"{f.get('height','?')}p"
        fps = f.get("fps", "")
        size = f.get("filesize") or f.get("filesize_approx")
        size_mb = f"{round(size/1024/1024,1)} MB" if size else "?"
        label = f"{fmt_id} | {ext} | {resolution} {fps}fps | {size_mb}"
        results.append((label, fmt_id))
    return results



def download_video(url, fmt, output_folder, audio_only=False,
                   codec="mp3", quality="192",
                   subtitles=False, auto_subs=False,
                   playlist=False, embed_subs=False,
                   thumb=False, embed_thumb=False,
                   container="mp4"):
    """Download video or playlist using yt-dlp with given options."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Default options
    ydl_opts = {
        "ignoreerrors": True,
        "noplaylist": not playlist,   # Single video if False, playlist if True
        "yesplaylist": playlist,      # Explicit control
    }

    # Output naming
    if playlist:
        # Include playlist index to avoid overwrites
        ydl_opts["outtmpl"] = os.path.join(output_folder, "%(playlist_index)s - %(title)s.%(ext)s")
    else:
        # Just the video title
        ydl_opts["outtmpl"] = os.path.join(output_folder, "%(title)s.%(ext)s")

    # Audio-only mode
    if audio_only:
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": codec,
            "preferredquality": quality
        }]
    else:
        ydl_opts["format"] = fmt or "bestvideo+bestaudio/best"
        ydl_opts["merge_output_format"] = container

    # Subtitles & thumbnails
    if subtitles:
        ydl_opts["writesubtitles"] = True
    if auto_subs:
        ydl_opts["writeautomaticsub"] = True
    if embed_subs:
        ydl_opts["embedsubtitles"] = True
    if thumb:
        ydl_opts["writethumbnail"] = True
    if embed_thumb:
        ydl_opts["embedthumbnail"] = True

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
