import streamlit as st
import requests
import re
import os
import time
from pydub import AudioSegment
from io import BytesIO

# --- 介面大字化設定 ---
st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:26px !important; font-weight: bold; color: #1E88E5; }
    .stButton>button { height: 3.5em; font-size: 22px !important; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 左側功能選單 ---
with st.sidebar:
    st.markdown("### 🛠️ 工具箱")
    mode = st.radio("功能：", ["🔄 1. Line音檔轉MP3", "📺 2. 抓YT音樂 (直連下載)"])
    st.markdown("---")
    st.success("✅ 通道狀態：連線中")

# --- 功能 1：音檔轉 MP3 (維持運作) ---
if mode == "🔄 1. Line音檔轉MP3":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("上傳音訊檔案：", type=["wav", "aac", "m4a"], accept_multiple_files=True)
    
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
                    st.error("❌ 轉換失敗")

# --- 功能 2：YouTube 直連下載 (多通道熱備份版) ---
elif mode == "📺 2. 抓YT音樂 (直連下載)":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓 YouTube 音樂</h1>", unsafe_allow_html=True)
    
    yt_url = st.text_input("請在此處貼上 YouTube 網址：", placeholder="https://www.youtube.com/watch?v=...")
    
    if yt_url:
        st.markdown("---")
        if st.button("🚀 抓取 128k MP3 (直接下載)", type="primary", use_container_width=True):
            status = st.empty()
            
            # --- 隱藏通道清單 (如果一組失敗，自動換下一組) ---
            api_endpoints = [
                "https://api.cobalt.re/",            # 通道 A (全球分身)
                "https://cobalt.k6.com.br/",         # 通道 B (巴西分身)
                "https://cobalt-api.v06.io/"          # 通道 C (備用分身)
            ]
            
            success = False
            for i, api in enumerate(api_endpoints):
                status.warning(f"⏳ 正在嘗試通道 {i+1}... (這可能需要 20 秒)")
                
                payload = {
                    "url": yt_url,
                    "downloadMode": "audio",
                    "audioFormat": "mp3",
                    "audioBitrate": "128" # 爸爸要求的 128kbps
                }
                
                try:
                    # 第一步：請求下載連結
                    res = requests.post(api, json=payload, headers={"Accept": "application/json"}, timeout=20)
                    data = res.json()
                    
                    if data.get("status") == "stream":
                        # 第二步：直接從通道抓取檔案內容
                        file_url = data.get("url")
                        file_res = requests.get(file_url, stream=True, timeout=60)
                        
                        status.success(f"🎉 通道 {i+1} 抓取成功！")
                        st.download_button(
                            label="📥 點我直接存檔 (MP3)",
                            data=file_res.content,
                            file_name="爸爸下載的音樂.mp3",
                            mime="audio/mpeg",
                            use_container_width=True
                        )
                        st.balloons()
                        success = True
                        break # 成功了就跳出迴圈
                except Exception as e:
                    continue # 失敗了就換下一個 API
            
            if not success:
                status.error("❌ 目前所有直連通道都遭到 YouTube 封鎖。")
                st.info("💡 爸爸，請先用側邊欄的按鈕跳轉下載，等我修復新的通道！")
