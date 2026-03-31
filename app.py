import streamlit as st
import os
from pydub import AudioSegment
from io import BytesIO

# --- 介面大字化設定 ---
st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:26px !important; font-weight: bold; color: #1E88E5; }
    .guide-text { font-size:20px !important; color: #555; line-height: 1.6; }
    .stButton>button { height: 3.5em; font-size: 22px !important; border-radius: 15px; }
    .link-button { 
        display: inline-block; 
        padding: 20px 40px; 
        font-size: 24px; 
        cursor: pointer; 
        text-align: center; 
        text-decoration: none; 
        outline: none; 
        color: #fff; 
        background-color: #FF0000; 
        border: none; 
        border-radius: 15px; 
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 左側功能選單 ---
with st.sidebar:
    st.markdown("### 🛠️ 功能切換")
    mode = st.radio("請選擇任務：", ["🔄 1. 音檔轉MP3 (處理Line傳來的檔案)", "📺 2. 抓YT轉MP3 (穩定下載區)"])
    st.markdown("---")
    st.info("💡 下載完記得把檔案搬到隨身碟，再跑『一鍵排序』喔！")

# --- 功能 1：音檔轉 MP3 (維持運作) ---
if mode == "🔄 1. 音檔轉MP3 (處理Line傳來的檔案)":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    st.markdown("<p class='guide-text'>適合處理從 Line 存下來的音樂，把它們變成車上能聽的格式。</p>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("點下面選取檔案：", type=["wav", "aac", "m4a"], accept_multiple_files=True)
    
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

# --- 功能 2：YouTube 下載導航 (改為穩定直連模式) ---
elif mode == "📺 2. 抓YT轉MP3 (穩定下載區)":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓取 YouTube 音樂</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #fff3f3; padding: 20px; border-radius: 15px; border-left: 5px solid #FF0000;">
        <p class="big-font">爸爸，這套方法最穩定、絕對不失敗：</p>
        <p class="guide-text">
            1. 點擊下方<b>「紅色大按鈕」</b>開啟工具網頁。<br>
            2. 把 YouTube 網址<b>「貼上」</b>到那個網頁的框框。<br>
            3. 按下網頁上的<b>「藍色箭頭」</b>或 <b>Download</b> 就能存到電腦了！
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 這裡做一個巨大的連結按鈕
    st.markdown('<a href="https://cobalt.tools/" target="_blank" class="link-button">🚀 點我開啟：YouTube 下載工具 (Cobalt)</a>', unsafe_allow_html=True)
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p class='guide-text'><b>💡 小撇步：</b></p>", unsafe_allow_html=True)
    st.markdown("- 進去工具網頁後，畫面很乾淨，沒有廣告，請放心操作。")
    st.markdown("- 下載完後，記得再用回桌面那個「一鍵傳送」把檔案送進隨身碟喔！")
