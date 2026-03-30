import streamlit as st
import os
import time
import re
import platform
import zipfile
from io import BytesIO
from pydub import AudioSegment
import filedate # 這是我們用來修改 Windows 日期的秘密武器

# --- 核心邏輯：自然排序 (讓 1, 2, 10 乖乖排好) ---
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# --- 核心邏輯：修改檔案日期 (Windows 專用優化) ---
def update_file_dates(file_path, target_timestamp):
    # 將時間轉為 filedate 喜歡的格式 "YYYY-MM-DD HH:MM:SS"
    dt_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(target_timestamp))
    
    try:
        if platform.system() == "Windows":
            # 同時修改 建立日期、修改日期、存取日期
            fd = filedate.File(file_path)
            fd.set(
                created=dt_str,
                modified=dt_str,
                accessed=dt_str
            )
        else:
            # Mac 系統使用
            os.utime(file_path, (target_timestamp, target_timestamp))
        return True
    except Exception as e:
        print(f"修改日期出錯: {e}")
        return False

# --- 網頁介面設定 ---
st.set_page_config(page_title="爸爸的音樂幫手", page_icon="🎵", layout="centered")

# 初始化分頁狀態
if 'page' not in st.session_state:
    st.session_state.page = "convert"

# --- 側邊欄：大按鈕選單 ---
with st.sidebar:
    st.title("🎵 音樂工具箱")
    st.write("請選擇您要執行的功能：")
    if st.button("🔄 1. 一鍵轉檔 (WAV/AAC 轉 MP3)", use_container_width=True):
        st.session_state.page = "convert"
    if st.button("🔢 2. 重新排序 (隨身碟專用)", use_container_width=True):
        st.session_state.page = "sort"
    st.markdown("---")
    st.caption(f"系統偵測: {platform.system()} Windows")

# --- 頁面 1: 轉檔功能 ---
if st.session_state.page == "convert":
    st.header("Step 1: 格式轉換")
    st.write("把 Line 下載的 wav 或 aac 檔案丟進來，我會幫您轉成 mp3。")
    
    uploaded_files = st.file_uploader("請選擇或拖曳檔案", type=["wav", "aac"], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🚀 開始轉檔並準備下載", type="primary", use_container_width=True):
            zip_buffer = BytesIO()
            try:
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    bar = st.progress(0)
                    status = st.empty()
                    
                    for i, uploaded_file in enumerate(uploaded_files):
                        status.text(f"正在處理: {uploaded_file.name}...")
                        
                        # 讀取並轉換
                        audio = AudioSegment.from_file(uploaded_file)
                        mp3_io = BytesIO()
                        audio.export(mp3_io, format="mp3")
                        
                        # 放入 ZIP
                        new_name = os.path.splitext(uploaded_file.name)[0] + ".mp3"
                        zip_file.writestr(new_name, mp3_io.getvalue())
                        
                        bar.progress((i + 1) / len(uploaded_files))
                    
                status.success("🎉 全部轉檔完成！")
                st.download_button(
                    label="📥 點我下載所有 MP3 檔案 (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="爸爸的音樂.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"糟糕，轉檔出錯了。請確認電腦是否有安裝 FFmpeg。錯誤訊息: {e}")

# --- 頁面 2: 排序功能 ---
elif st.session_state.page == "sort":
    st.header("Step 2: 重新排列日期")
    st.info("請將隨身碟資料夾的路徑貼在下面（例如：D:\\我的音樂）")
    
    target_path = st.text_input("資料夾路徑", placeholder="在此貼上路徑後按 Enter...")
    
    if target_path:
        # 清除可能的引號
        clean_path = target_path.strip('"').strip("'")
        
        if os.path.exists(clean_path):
            if st.button("🚀 執行順序重排", type="primary", use_container_width=True):
                # 抓取所有 MP3 檔案
                mp3_files = [f for f in os.listdir(clean_path) if f.lower().endswith(".mp3")]
                # 依照數字排序
                mp3_files.sort(key=natural_sort_key)
                
                if not mp3_files:
                    st.warning("這個資料夾裡面沒有 MP3 檔案喔！")
                else:
                    bar = st.progress(0)
                    base_time = time.time()
                    
                    for i, filename in enumerate(mp3_files):
                        full_path = os.path.join(clean_path, filename)
                        # 每隔 10 秒一個間隔，確保機器讀得到先後
                        new_time = base_time + (i * 10)
                        update_file_dates(full_path, new_time)
                        bar.progress((i + 1) / len(mp3_files))
                    
                    st.success(f"✅ 完成！已重新排列 {len(mp3_files)} 首歌曲。")
                    st.balloons()
        else:
            st.error("找不到這個路徑，請確認路徑是否正確（例如有沒有漏掉磁碟代號 D:）。")