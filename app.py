import streamlit as st
import os
from io import BytesIO
from pydub import AudioSegment

# --- 介面設定 ---
st.set_page_config(page_title="爸爸的音樂轉檔工具", page_icon="🎵", layout="centered")

# 使用大字級的標題與樣式
st.markdown("<h1 style='text-align: center; font-size: 40px;'>🎵 爸爸的轉檔神器</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>將 Line 的音訊變成一般的 MP3</p>", unsafe_allow_html=True)
st.markdown("---")

# --- 轉檔功能 ---
st.markdown("<h3 style='font-size: 24px;'>第一步：選取檔案</h3>", unsafe_allow_html=True)

# 修改為中文標籤「上傳檔案」
uploaded_files = st.file_uploader(
    label="上傳檔案", 
    type=["wav", "aac", "m4a"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown("---")
    st.markdown("<h3 style='font-size: 24px;'>第二步：按下按鈕開始轉檔</h3>", unsafe_allow_html=True)
    
    if st.button("🚀 開始轉檔", type="primary", use_container_width=True):
        bar = st.progress(0)
        status_text = st.empty()
        
        for i, file in enumerate(uploaded_files):
            try:
                status_text.markdown(f"<p style='font-size: 18px;'>正在轉換: <b>{file.name}</b> ...</p>", unsafe_allow_html=True)
                
                # 執行轉檔
                audio = AudioSegment.from_file(file)
                mp3_data = BytesIO()
                audio.export(mp3_data, format="mp3", bitrate="192k")
                
                new_filename = os.path.splitext(file.name)[0] + ".mp3"
                
                # 顯示大按鈕
                st.success(f"✅ 轉換成功: {new_filename}")
                st.download_button(
                    label=f"📥 點我下載 {new_filename}",
                    data=mp3_data.getvalue(),
                    file_name=new_filename,
                    mime="audio/mpeg",
                    key=f"final_dl_{i}",
                    use_container_width=True
                )
                
                bar.progress((i + 1) / len(uploaded_files))
            except Exception as e:
                st.error(f"❌ {file.name} 轉換失敗。")
        
        status_text.markdown("<p style='color: green; font-size: 20px; font-weight: bold;'>✨ 處理完畢！請點擊按鈕存到電腦。</p>", unsafe_allow_html=True)
        st.balloons()

st.markdown("---")
st.caption("💡 提示：下載後的檔案會出現在您的『下載』資料夾中。")
