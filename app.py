import streamlit as st
import os
from io import BytesIO
from pydub import AudioSegment

# --- 介面設定 ---
st.set_page_config(page_title="爸爸的音樂轉檔工具", page_icon="🎵", layout="centered")

st.title("🎵 爸爸的專屬音樂轉檔器")
st.write("請將 Line 下載的音訊檔拖到下方，轉換完後直接點擊下載 MP3。")
st.markdown("---")

# --- 唯一功能：上傳與轉檔 ---
uploaded_files = st.file_uploader("請選擇音訊檔 (支援 wav, aac, m4a)", type=["wav", "aac", "m4a"], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 開始轉檔", type="primary", use_container_width=True):
        bar = st.progress(0)
        status_text = st.empty()
        
        for i, file in enumerate(uploaded_files):
            try:
                status_text.text(f"正在轉換: {file.name}...")
                
                # 核心轉檔 (雲端自動處理 FFmpeg)
                audio = AudioSegment.from_file(file)
                mp3_data = BytesIO()
                audio.export(mp3_data, format="mp3", bitrate="192k")
                
                # 準備新檔名
                new_filename = os.path.splitext(file.name)[0] + ".mp3"
                
                # 顯示下載按鈕
                st.success(f"✅ 轉換成功: {new_filename}")
                st.download_button(
                    label=f"📥 點我下載 {new_filename}",
                    data=mp3_data.getvalue(),
                    file_name=new_filename,
                    mime="audio/mpeg",
                    key=f"cloud_dl_{i}" 
                )
                
                bar.progress((i + 1) / len(uploaded_files))
            except Exception as e:
                st.error(f"❌ {file.name} 轉換失敗。錯誤: {e}")
        
        status_text.text("✨ 所有檔案處理完畢！請點擊上方按鈕下載，並存入隨身碟。")