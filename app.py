import streamlit as st
import requests
import re
import os
from pydub import AudioSegment
from io import BytesIO

# --- 介面大字化設定 ---
st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:26px !important; font-weight: bold; color: #1E88E5; }
    .stButton>button { height: 3.5em; font-size: 22px !important; border-radius: 15px; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 功能選單 ---
with st.sidebar:
    st.markdown("### 🛠️ 功能切換")
    mode = st.radio("請選擇：", ["🔄 本地音檔轉MP3", "📺 抓YT轉MP3"])
    st.markdown("---")
    st.info("💡 提示：YT 抓取會直接幫您轉成 MP3。")

# --- 功能 1：音檔轉 MP3 ---
if mode == "🔄 本地音檔轉MP3":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("上傳音訊檔案 (WAV/AAC/M4A)", type=["wav", "aac", "m4a"], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🚀 開始轉檔", use_container_width=True):
            for i, file in enumerate(uploaded_files):
                try:
                    audio = AudioSegment.from_file(file)
                    mp3_data = BytesIO()
                    audio.export(mp3_data, format="mp3", bitrate="192k")
                    new_name = os.path.splitext(file.name)[0] + ".mp3"
                    st.success(f"✅ 完成: {new_name}")
                    st.download_button(label=f"📥 下載 {new_name}", data=mp3_data.getvalue(), file_name=new_name, mime="audio/mpeg", key=f"au_{i}", use_container_width=True)
                except:
                    st.error(f"❌ {file.name} 轉檔失敗")

# --- 功能 2：YouTube 轉 MP3 (更新至 Cobalt 最新 API) ---
elif mode == "📺 2. 抓YT轉MP3":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓YT轉MP3</h1>", unsafe_allow_html=True)
    yt_url = st.text_input("請貼上 YouTube 網址：", placeholder="https://www.youtube.com/watch?v=...")
    
    if yt_url:
        if st.button("🚀 抓取 MP3", type="primary", use_container_width=True):
            status = st.empty()
            status.warning("⏳ 正在連線到最新轉檔伺服器...")

            # --- 關鍵修正：最新 API 網址與設定 ---
            api_url = "https://api.cobalt.tools/" 
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "url": yt_url,
                "downloadMode": "audio",
                "audioFormat": "mp3",
                "audioBitrate": "128" # 確保穩定度
            }

            try:
                response = requests.post(api_url, json=payload, headers=headers, timeout=30)
                result = response.json()

                # Cobalt v10 的回傳邏輯
                if result.get("status") == "stream":
                    download_url = result.get("url")
                    file_res = requests.get(download_url, stream=True)
                    
                    status.success("🎉 抓取成功！")
                    st.download_button(
                        label="📥 下載 MP3 到電腦",
                        data=file_res.content,
                        file_name="youtube_music.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )
                    st.balloons()
                else:
                    status.error(f"❌ 伺服器忙碌：{result.get('text', '請稍後再試')}")
            except Exception as e:
                status.error("❌ 連線超時，請重新點擊按鈕。")
