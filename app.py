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
    .stButton>button { height: 3em; font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 左側功能選單 ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 28px;'>🎵 功能選單</h1>", unsafe_allow_html=True)
    mode = st.radio("任務：", ["🔄 1. 音檔轉MP3", "📺 2. 抓YT轉MP3"])
    st.markdown("---")
    st.info("💡 提示：YT 抓取若失敗，請稍等幾分鐘再試。")

# --- 功能 1：本地音檔轉 MP3 ---
if mode == "🔄 1. 音檔轉MP3":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：選取檔案</p>", unsafe_allow_html=True)
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

# --- 功能 2：YouTube 轉 MP3 (深度優化版) ---
elif mode == "📺 2. 抓YT轉MP3":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓YT轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：請貼上 YouTube 網址</p>", unsafe_allow_html=True)
    
    yt_url = st.text_input("網址：", placeholder="https://www.youtube.com/watch?v=...")
    
    if yt_url:
        st.markdown("---")
        if st.button("🚀 開始抓取並轉成 MP3", type="primary", use_container_width=True):
            # 建立唯一暫存檔名，避免多人同時使用的衝突
            unique_id = str(int(time.time()))
            temp_fn = f"yt_audio_{unique_id}"
            
            status = st.empty()
            status.warning("⏳ 正在全力抓取中，大約需要 30-60 秒...")
            
            # 針對雲端環境深度優化的 yt-dlp 設定
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f"{temp_fn}.%(ext)s",
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                # 關鍵：偽裝成一般電腦瀏覽器
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'referer': 'https://www.google.com/',
                'nocheckcertificate': True,
                'quiet': True,
                'no_warnings': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 抓取資訊並下載
                    info = ydl.extract_info(yt_url, download=True)
                    title = info.get('title', 'youtube_music')
                    clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
                    
                    # 讀取轉好的 MP3
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
                        # 下載後刪除伺服器暫存
                        os.remove(mp3_path)
                    else:
                        status.error("❌ 下載成功但轉檔失敗，請再試一次。")
                        
            except Exception as e:
                # 捕捉錯誤日誌，方便除錯
                err_msg = str(e)
                if "Sign in to confirm you're not a bot" in err_msg:
                    status.error("❌ YouTube 偵測到機器人。請等 10 分鐘再試，或換一個影片連結。")
                else:
                    status.error(f"❌ 抓取失敗。原因：{err_msg[:100]}...")