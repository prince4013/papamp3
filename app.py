import streamlit as st
import os
from pydub import AudioSegment
from io import BytesIO

# --- 頁面大字化與樣式設定 ---
st.set_page_config(page_title="爸爸的音樂神器", page_icon="🎵", layout="centered")

st.markdown("""
    <style>
    .section-title { font-size:32px !important; font-weight: bold; margin-bottom: 10px; }
    .guide-box { background-color: #f0f7ff; padding: 20px; border-radius: 15px; border-left: 8px solid #1E88E5; margin-bottom: 20px; }
    .guide-text { font-size:20px !important; color: #333; line-height: 1.6; }
    .big-font { font-size:24px !important; font-weight: bold; }
    .stButton>button { height: 3.5em; font-size: 22px !important; border-radius: 15px; }
    
    /* 紅色跳轉按鈕樣式 */
    .yt-button { 
        display: block; 
        width: 100%; 
        padding: 20px; 
        background-color: #FF0000; 
        color: white !important; 
        text-align: center; 
        font-size: 26px; 
        font-weight: bold; 
        border-radius: 15px; 
        text-decoration: none;
        margin: 20px 0;
    }
    .yt-button:hover { background-color: #cc0000; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 頂部標題 ---
st.markdown("<h1 style='text-align: center;'>🚀 爸爸的音樂神器</h1>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 第一區：YouTube 抓歌區 (穩定跳轉模式)
# ==========================================
st.markdown("<div class='section-title' style='color: #FF0000;'>第一種 📺 從 YouTube 抓歌</div>", unsafe_allow_html=True)

st.markdown("""
<div class="guide-box">
    <p class="big-font">💡 操作說明：</p>
    <p class="guide-text">
        1. 點擊下方<b>「紅色大按鈕」</b>開啟工具網頁。<br>
        2. 在新網頁的框框裡<b>「按右鍵貼上」</b>影片網址。<br>
        3. 按下 <b>開始/下載</b>，選擇 <b>MP3</b> 存到電腦即可！
    </p>
</div>
""", unsafe_allow_html=True)

# 醒目的紅色跳轉按鈕
st.markdown('<a href="https://vd6s.com/zh-tw3/" target="_blank" class="yt-button">🚀 點我開啟：YouTube 下載工具 (穩定不失敗)</a>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# 第二區：Line 音檔轉檔區 (本地轉檔模式)
# ==========================================
st.markdown("<div class='section-title' style='color: #FF4B4B;'>🔄 第二種：Line 音檔轉 MP3</div>", unsafe_allow_html=True)
st.markdown("<p class='guide-text'>如果是從 Line 存下來的音樂 (WAV/AAC)，請在下面轉換：</p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("點按鈕選取電腦裡的檔案：", type=["wav", "aac", "m4a"], accept_multiple_files=True, label_visibility="collapsed")

if uploaded_files:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 開始轉為 MP3 格式", use_container_width=True):
        progress_bar = st.progress(0)
        for i, file in enumerate(uploaded_files):
            try:
                # 執行轉檔
                audio = AudioSegment.from_file(file)
                mp3_data = BytesIO()
                audio.export(mp3_data, format="mp3", bitrate="192k")
                
                new_name = os.path.splitext(file.name)[0] + ".mp3"
                st.success(f"✅ 轉換成功: {new_name}")
                
                # 提供下載按鈕
                st.download_button(
                    label=f"📥 點我下載：{new_name}",
                    data=mp3_data.getvalue(),
                    file_name=new_name,
                    mime="audio/mpeg",
                    key=f"dl_{i}",
                    use_container_width=True
                )
                progress_bar.progress((i + 1) / len(uploaded_files))
            except:
                st.error(f"❌ 檔案 {file.name} 格式不支援或已損壞。")
        st.balloons()

# --- 底部提醒 ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>✨ 音樂全部下載完後，記得點桌面的<b>「一鍵傳送並排序」</b>送進隨身碟！</p>", unsafe_allow_html=True)
