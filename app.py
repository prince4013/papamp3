import streamlit as st
import os
import re
import time
from io import BytesIO
from pydub import AudioSegment
import yt_dlp

# --- 介面設定 ---
st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .stButton>button { height: 3.5em; font-size: 22px !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 左側功能選單 ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 28px;'>🎵 功能選單</h1>", unsafe_allow_html=True)
    mode = st.radio("請選擇任務：", ["🔄 1. 音檔轉MP3", "📺 2. 抓YT轉MP3"])
    st.markdown("---")
    if os.path.exists("cookies.txt"):
        st.success("✅ 已偵測到通行證 (Cookies)")
    else:
        st.info("💡 提示：若抓取失敗，請考慮加入 cookies.txt")

# --- 功能 1：本地音檔轉 MP3 ---
if mode == "🔄 1. 音檔轉MP3":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：點按鈕選取檔案 (WAV/AAC)</p>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("上傳", type=["wav", "aac", "m4a"], accept_multiple_files=True, label_visibility="collapsed")
    
    if uploaded_files:
        if st.button("🚀 開始轉檔", type="primary", use_container_width=True):
            bar = st.progress(0)
            for i, file in enumerate(uploaded_files):
                try:
                    audio = AudioSegment.from_file(file)
                    mp3_data = BytesIO()
                    audio.export(mp3_data, format="mp3", bitrate="192k")
                    new_name = os.path.splitext(file.name)[0] + ".mp3"
                    st.success(f"✅ 已完成: {new_name}")
                    st.download_button(label=f"📥 下載 {new_name}", data=mp3_data.getvalue(), file_name=new_name, mime="audio/mpeg", key=f"au_{i}", use_container_width=True)
                    bar.progress((i + 1) / len(uploaded_files))
                except:
                    st.error(f"❌ {file.name} 轉換失敗")
            st.balloons()

# --- 功能 2：YouTube 轉 MP3 (相容性最強版) ---
elif mode == "📺 2. 抓YT轉MP3":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓YT轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：請貼上 YouTube 網址</p>", unsafe_allow_html=True)
    
    yt_url = st.text_input("網址：", placeholder="https://www.youtube.com/watch?v=...")
    
    if yt_url:
        st.markdown("---")
        if st.button("🚀 開始抓取並轉成 MP3", type="primary", use_container_width=True):
            # 1. 自動清理網址：只留下影片 ID，去掉播放清單參數
            if "&list=" in yt_url:
                yt_url = yt_url.split("&list=")[0]
            if "?si=" in yt_url:
                yt_url = yt_url.split("?si=")[0]

            unique_id = str(int(time.time()))
            temp_fn = f"yt_audio_{unique_id}"
            
            status = st.empty()
            status.warning("⏳ 正在下載中，請耐心等候（約 30-60 秒）...")
            
            # 2. 放寬格式限制，改用 m4a/mp4 再轉 mp3
            ydl_opts = {
                'format': 'ba/b', # 👈 改成抓取「任何音訊 (ba)」或「任何影片 (b)」
                'outtmpl': f"{temp_fn}.%(ext)s",
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'quiet': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(yt_url, download=True)
                    title = info.get('title', 'youtube_music')
                    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
                    
                    mp3_path = f"{temp_fn}.mp3"
                    if os.path.exists(mp3_path):
                        with open(mp3_path, "rb") as f:
                            mp3_bytes = f.read()
                        
                        status.success(f"🎉 成功抓取：{clean_title}")
                        st.download_button(
                            label=f"📥 點我下載 MP3：{clean_title}",
                            data=mp3_bytes,
                            file_name=f"{clean_title}.mp3",
                            mime="audio/mpeg",
                            use_container_width=True
                        )
                        st.balloons()
                        os.remove(mp3_path)
                    else:
                        status.error("❌ 格式轉換失敗，請換一個影片試試。")
                        
            except Exception as e:
                status.error(f"❌ 抓取失敗。原因：{str(e)[:100]}...")

st.markdown("---")
st.caption("💡 下載完後請執行桌面的『一鍵傳送並排序』！")