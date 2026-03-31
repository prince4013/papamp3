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
    st.info("💡 轉換完成後，請點擊下載按鈕儲存到電腦。")

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
                except Exception as e:
                    st.error(f"❌ {file.name} 轉檔失敗")

# --- 功能 2：YouTube 轉 MP3 (串接 Cobalt API 穩定版) ---
elif mode == "📺 抓YT轉MP3":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓YT轉MP3</h1>", unsafe_allow_html=True)
    yt_url = st.text_input("請貼上 YouTube 網址：", placeholder="https://www.youtube.com/watch?v=...")
    
    if yt_url:
        if st.button("🚀 抓取 MP3", type="primary", use_container_width=True):
            status = st.empty()
            status.warning("⏳ 正在連線到轉檔伺服器，請稍候約 15-30 秒...")

            # 串接 Cobalt API
            api_url = "https://api.cobalt.tools/api/json"
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            payload = {
                "url": yt_url,
                "downloadMode": "audio",
                "audioFormat": "mp3",
                "audioBitrate": "128" # 稍微降低一點以增加成功率
            }

            try:
                # 增加 timeout 防止網頁無限期轉圈圈
                response = requests.post(api_url, json=payload, headers=headers, timeout=60)
                result = response.json()

                if result.get("status") in ["stream", "picker"]:
                    download_url = result.get("url")
                    file_res = requests.get(download_url, timeout=60)
                    
                    status.success("🎉 抓取成功！請點擊下方按鈕下載。")
                    st.download_button(
                        label="📥 點我下載 MP3 檔案",
                        data=file_res.content,
                        file_name="youtube_music.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )
                    st.balloons()
                else:
                    status.error(f"❌ 伺服器回應：{result.get('text', '暫時無法下載此影片')}")
            except Exception as e:
                status.error("❌ 連線超時或伺服器忙碌中，請再點一次按鈕試試。")
