import streamlit as st
import os
import time
import re
import platform
from io import BytesIO
from pydub import AudioSegment
import filedate

# --- 1. 強制讓程式找到 FFmpeg 工人 (爸爸的 Windows 路徑) ---
# 確保 C:\ffmpeg\bin 裡面有 ffmpeg.exe
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

# --- 2. 核心邏輯函數 ---

# 自然排序：確保檔名 1, 2, 10 的順序符合直覺
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# 修改檔案日期：確保隨身碟讀取順序正確 (Windows 專用)
def update_file_dates(file_path, target_timestamp):
    dt_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(target_timestamp))
    try:
        if platform.system() == "Windows":
            fd = filedate.File(file_path)
            fd.set(
                created=dt_str,
                modified=dt_str,
                accessed=dt_str
            )
        else:
            os.utime(file_path, (target_timestamp, target_timestamp))
        return True
    except:
        return False

# --- 3. 網頁介面配置 ---

st.set_page_config(page_title="爸爸的音樂幫手", page_icon="🎵", layout="centered")

# 左側功能選單
with st.sidebar:
    st.title("🎵 音樂工具箱")
    st.write("請選擇您要執行的任務：")
    mode = st.radio("功能切換：", ["🔄 1. 一鍵轉檔 (直接下載 MP3)", "🔢 2. 重新排序 (隨身碟專用)"])
    st.markdown("---")
    st.caption(f"執行環境: Windows | 裝置: Aspire 3")
    st.info("💡 小技巧：轉檔完下載後，記得用功能 2 幫隨身碟排順序喔！")

# --- 4. 功能分頁內容 ---

# 分頁 1：轉檔 (上傳後直接出現在網頁下載)
if mode == "🔄 1. 一鍵轉檔 (直接下載 MP3)":
    st.header("🔄 一鍵轉檔 (WAV/AAC 轉 MP3)")
    st.write("請將檔案拖到下方。轉換完成後，每一首歌都會出現一個 **[下載]** 按鈕。")
    
    uploaded_files = st.file_uploader("選擇音訊檔", type=["wav", "aac"], accept_multiple_files=True)
    
    if uploaded_files:
        st.markdown("---")
        if st.button("🚀 開始轉檔", type="primary", use_container_width=True):
            bar = st.progress(0)
            status_text = st.empty()
            
            for i, file in enumerate(uploaded_files):
                try:
                    status_text.text(f"正在轉換: {file.name}...")
                    
                    # 讀取檔案並轉為 MP3 格式
                    audio = AudioSegment.from_file(file)
                    mp3_data = BytesIO()
                    audio.export(mp3_data, format="mp3")
                    
                    # 準備新檔名
                    new_filename = os.path.splitext(file.name)[0] + ".mp3"
                    
                    # 顯示下載按鈕
                    st.success(f"✅ 轉換成功: {new_filename}")
                    st.download_button(
                        label=f"📥 點我下載 {new_filename}",
                        data=mp3_data.getvalue(),
                        file_name=new_filename,
                        mime="audio/mpeg",
                        key=f"btn_{i}_{new_filename}" # 確保每個按鈕有唯一 ID
                    )
                    
                    bar.progress((i + 1) / len(uploaded_files))
                except Exception as e:
                    st.error(f"❌ {file.name} 轉換失敗。錯誤訊息: {e}")
            
            status_text.text("✨ 所有檔案處理完畢！")

# 分頁 2：排序 (輸入隨身碟路徑直接修改)
elif mode == "🔢 2. 重新排序 (隨身碟專用)":
    st.header("🔢 重新排列播放順序")
    st.write("讓汽車音響乖乖按照檔名 1, 2, 3... 的順序播放。")
    st.info("💡 提示：在隨身碟資料夾按 **Alt + D** 複製路徑，然後貼在下面。")
    
    folder_path = st.text_input("隨身碟資料夾路徑：", placeholder="例如 D:\\我的音樂")
    
    if folder_path:
        # 去除引號
        clean_path = folder_path.strip('"').strip("'")
        
        if os.path.exists(clean_path):
            if st.button("🚀 執行順序重排", type="primary", use_container_width=True):
                # 抓取所有 MP3
                files = [f for f in os.listdir(clean_path) if f.lower().endswith(".mp3")]
                # 自然排序
                files.sort(key=natural_sort_key)
                
                if not files:
                    st.warning("在此資料夾內找不到 MP3 檔案，請確認路徑是否正確。")
                else:
                    bar = st.progress(0)
                    base_time = time.time()
                    
                    for i, filename in enumerate(files):
                        full_p = os.path.join(clean_path, filename)
                        # 每隔 10 秒一個間隔設定時間
                        new_timestamp = base_time + (i * 10)
                        update_file_dates(full_p, new_timestamp)
                        bar.progress((i + 1) / len(files))
                    
                    st.success(f"🎉 大功告成！已重新排列 {len(files)} 首歌的日期。")
                    st.balloons()
        else:
            st.error("找不到這個路徑，請檢查隨身碟是否插好，或路徑是否有誤。")