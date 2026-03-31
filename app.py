import streamlit as st
import os
from pydub import AudioSegment
from io import BytesIO

# --- 介面大字化設定 ---
st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .big-font { font-size:26px !important; font-weight: bold; color: #1E88E5; }
    .stButton>button { height: 3.5em; font-size: 22px !important; border-radius: 15px; }
    .jump-button { 
        display: block; 
        width: 100%; 
        padding: 25px; 
        background-color: #28a745; 
        color: white; 
        text-align: center; 
        font-size: 24px; 
        font-weight: bold; 
        border-radius: 15px; 
        text-decoration: none;
        margin-top: 10px;
    }
    .jump-button:hover { background-color: #218838; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 左側功能選單 ---
with st.sidebar:
    st.markdown("### 🛠️ 工具箱")
    mode = st.radio("功能：", ["🔄 1. Line音檔轉MP3", "📺 2. 抓YT音樂 (穩定版)"])
    st.markdown("---")
    st.success("✅ 系統已連線")

# --- 功能 1：音檔轉 MP3 ---
if mode == "🔄 1. Line音檔轉MP3":
    st.markdown("<h1 style='color: #FF4B4B;'>🔄 音檔轉MP3</h1>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("上傳 Line 存下來的音樂：", type=["wav", "aac", "m4a"], accept_multiple_files=True)
    
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
                    st.error(f"❌ 轉換失敗")

# --- 功能 2：YouTube 穩定橋接 ---
elif mode == "📺 2. 抓YT音樂 (穩定版)":
    st.markdown("<h1 style='color: #FF0000;'>📺 抓 YouTube 音樂</h1>", unsafe_allow_html=True)
    
    # 輸入網址
    yt_url = st.text_input("請在此處貼上 YouTube 網址：", placeholder="https://www.youtube.com/watch?v=...")
    
    if yt_url:
        st.markdown("---")
        st.markdown("<p class='big-font'>✨ 神器準備好了！</p>", unsafe_allow_html=True)
        st.write("爸爸，請點擊下方的綠色大按鈕，它會幫你直接跳轉到下載畫面：")
        
        # 這裡利用 vd6s 的特性，嘗試生成一個可以直接跳轉的連結
        # 雖然有些網站不支援自動填充，但我們可以導向最穩定的版本
        jump_url = f"https://vd6s.com/zh-tw3/"
        
        # 顯示大按鈕
        st.markdown(f'''
            <a href="{jump_url}" target="_blank" class="jump-button">
                🚀 一鍵前往：開始下載這首歌
            </a>
        ''', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-top: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 10px;">
            <p style="color: #666;"><b>操作三步驟：</b><br>
            1. 點上面綠色按鈕 (會開新視窗)<br>
            2. 在新視窗<b>按右鍵貼上網址</b>，按下開始<br>
            3. 選 <b>MP3</b> 下載，完成後記得回桌面跑「一鍵傳送」！</p>
        </div>
        """, unsafe_allow_html=True)
