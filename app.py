import streamlit as st
import requests
import re
import os
from pydub import AudioSegment
from io import BytesIO

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
    st.success("✅ 目前連線狀態：正常")

# --- 功能 1：本地音檔轉 MP3 (維持不變) ---
if mode == "🔄 1. 音檔轉MP3":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：點按鈕選取檔案</p>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("上傳", type=["wav", "aac", "m4a"], accept_multiple_files=True, label_visibility="collapsed")
    
    if uploaded_files:
        if st.button("🚀 開始轉檔", type="primary", use_container_width=True):
            for i, file in enumerate(uploaded_files):
                try:
                    audio = AudioSegment.from_file(file)
                    mp3_data = BytesIO()
                    audio.export(mp3_data, format="mp3", bitrate="192k")
                    new_name = os.path.splitext(file.name)[0] + ".mp3"
                    st.success(f"✅ 已完成: {new_name}")
                    st.download_button(label=f"📥 下載 {new_name}", data=mp3_data.getvalue(), file_name=new_name, mime="audio/mpeg", key=f"au_{i}", use_container_width=True)
                except:
                    st.error(f"❌ {file.name} 轉換失敗")

# --- 功能 2：YouTube 轉 MP3 (使用 Cobalt API) ---
elif mode == "📺 2. 抓YT轉MP3":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓YT轉MP3 (穩定版)</h1>", unsafe_allow_html=True)
    st.markdown("<p class='big-font'>第一步：請貼上 YouTube 網址</p>", unsafe_allow_html=True)
    
    yt_url = st.text_input("網址：", placeholder="https://www.youtube.com/watch?v=...")
    
    if yt_url:
        st.markdown("---")
        if st.button("🚀 開始抓取 MP3", type="primary", use_container_width=True):
            status = st.empty()
            status.warning("⏳ 正在透過代理伺服器抓取中，請稍候...")

            # Cobalt API 請求設定
            api_url = "https://api.cobalt.tools/api/json"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = {
                "url": yt_url,
                "downloadMode": "audio", # 👈 只抓聲音
                "audioFormat": "mp3",    # 👈 直接要 MP3
                "audioBitrate": "192"    # 👈 高音質
            }

            try:
                # 向 Cobalt 發送請求
                response = requests.post(api_url, json=payload, headers=headers)
                result = response.json()

                if result.get("status") == "stream" or result.get("status") == "picker":
                    # 取得下載連結
                    download_url = result.get("url")
                    
                    # 抓取該連結的檔案內容
                    file_res = requests.get(download_url)
                    
                    status.success("🎉 抓取成功！")
                    st.download_button(
                        label="📥 點我直接下載 MP3 檔案",
                        data=file_res.content,
                        file_name="youtube_music.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )
                    st.balloons()
                else:
                    status.error(f"❌ 抓取失敗。原因：{result.get('text', '未知錯誤')}")
            
            except Exception as e:
                status.error(f"❌ 連線到轉檔伺服器失敗。")
                st.info("💡 提示：如果此功能失效，代表 Cobalt 伺服器目前繁忙，請過幾分鐘再試。")

st.markdown("---")
st.caption("💡 如果下載完檔名是亂碼，記得手動改名！")
