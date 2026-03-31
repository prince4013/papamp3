import streamlit as st
import os
import re
import time
from io import BytesIO
from pydub import AudioSegment
import yt_dlp

st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

st.markdown("<h1 style='text-align: center; color: #FF0000;'>📺 抓YT轉MP3 (強化版)</h1>", unsafe_allow_html=True)

yt_url = st.text_input("請在此處貼上 YouTube 網址：", placeholder="https://www.youtube.com/watch?v=...")

if yt_url:
    if st.button("🚀 開始抓取並轉成 MP3", type="primary", use_container_width=True):
        # 1. 強力清洗網址 (只留下最核心的影片 ID)
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", yt_url)
        if match:
            video_id = match.group(1)
            clean_url = f"https://www.youtube.com/watch?v={video_id}"
        else:
            clean_url = yt_url

        unique_id = str(int(time.time()))
        temp_fn = f"yt_audio_{unique_id}"
        status = st.empty()
        status.warning("⏳ 正在嘗試突破 YouTube 封鎖並下載中...")

        ydl_opts = {
            'format': 'ba/b',
            'outtmpl': f"{temp_fn}.%(ext)s",
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            # 💡 關鍵：強制使用 IPv4 並模擬真實瀏覽器行為
            'source_address': '0.0.0.0', 
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(clean_url, download=True)
                title = info.get('title', 'youtube_music')
                clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
                
                mp3_path = f"{temp_fn}.mp3"
                if os.path.exists(mp3_path):
                    with open(mp3_path, "rb") as f:
                        mp3_bytes = f.read()
                    status.success(f"🎉 成功抓取：{clean_title}")
                    st.download_button(label=f"📥 點我下載 MP3：{clean_title}", data=mp3_bytes, file_name=f"{clean_title}.mp3", mime="audio/mpeg", use_container_width=True)
                    os.remove(mp3_path)
        except Exception as e:
            status.error("❌ 雲端伺服器遭封鎖。")
            st.info("💡 建議：請將 cookies.txt 上傳至 GitHub，或使用下方的『電腦本地一鍵抓取』。")