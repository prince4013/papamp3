import streamlit as st
import os
import re
from io import BytesIO
from pydub import AudioSegment
import yt_dlp

# --- 介面設定：長輩友善大字版 ---
st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

# 自定義 CSS 讓字體再大一點
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .stButton>button { height: 3em; font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 左側功能選單 ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 28px;'>🎵 功能選單</h1>", unsafe_allow_html=True)
    mode = st.radio(
        "請選擇您要做的任務：",
        ["🔄 1. 音檔轉MP3", "📺 2. 抓YT轉MP3"],
        index=0
    )
    st.markdown("---")
    st.info("💡 提示：轉換完記得點【下載】按鈕喔！")

# --- 功能 1：本地音檔轉 MP3 ---
if mode == "🔄 1. 音檔轉MP3":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：點下面按鈕選取檔案 (WAV/AAC)</p>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("上傳檔案", type=["wav", "aac", "m4a"], accept_multiple_files=True, label_visibility="collapsed")
    
    if uploaded_files:
        st.markdown("---")
        st.markdown("<p class='big-font'>第二步：按下按鈕開始轉檔</p>", unsafe_allow_html=True)
        if st.button("🚀 開始轉檔", type="primary", use_container_width=True):
            bar = st.progress(0)
            for i, file in enumerate(uploaded_files):
                try:
                    audio = AudioSegment.from_file(file)
                    mp3_data = BytesIO()
                    audio.export(mp3_data, format="mp3", bitrate="192k")
                    
                    new_filename = os.path.splitext(file.name)[0] + ".mp3"
                    st.success(f"✅ 轉換成功: {new_filename}")
                    st.download_button(
                        label=f"📥 點我下載 {new_filename}",
                        data=mp3_data.getvalue(),
                        file_name=new_filename,
                        mime="audio/mpeg",
                        key=f"audio_{i}",
                        use_container_width=True
                    )
                    bar.progress((i + 1) / len(uploaded_files))
                except Exception as e:
                    st.error(f"檔案 {file.name} 出錯了。")
            st.balloons()

# --- 功能 2：YouTube 轉 MP3 ---
elif mode == "📺 2. 抓YT轉MP3":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓YT轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：請貼上 YouTube 的網址</p>", unsafe_allow_html=True)
    
    yt_url = st.text_input("在這裡按右鍵貼上網址：", placeholder="https://www.youtube.com/watch?v=xxxxxx")
    
    if yt_url:
        st.markdown("---")
        st.markdown("<p class='big-font'>第二步：按下按鈕開始抓取</p>", unsafe_allow_html=True)
        if st.button("🚀 開始抓取並轉成 MP3", type="primary", use_container_width=True):
            status = st.empty()
            status.warning("⏳ 正在下載中，請稍候（這可能需要 30 秒到 1 分鐘）...")
            
            # yt-dlp 設定
            temp_filename = "temp_yt_audio"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': temp_filename, # 暫存檔名
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # 取得影片資訊（主要是標題）
                    info = ydl.extract_info(yt_url, download=True)
                    video_title = info.get('title', 'youtube_audio')
                    
                    # 讀取剛剛下載好的 mp3 檔案
                    with open(f"{temp_filename}.mp3", "rb") as f:
                        mp3_bytes = f.read()
                    
                    status.success(f"🎉 抓取成功：{video_title}")
                    st.download_button(
                        label=f"📥 點我下載 MP3：{video_title}",
                        data=mp3_bytes,
                        file_name=f"{video_title}.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )
                    st.balloons()
                    
                    # 清理伺服器暫存檔
                    if os.path.exists(f"{temp_filename}.mp3"):
                        os.remove(f"{temp_filename}.mp3")
                        
            except Exception as e:
                status.error(f"❌ 抓取失敗，請確認網址是否正確。錯誤訊息: {e}")

st.markdown("---")
st.caption("💡 下載完記得把檔案搬到排序資料夾，再跑『一鍵排序』喔！")