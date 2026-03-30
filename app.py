import streamlit as st
import os
import time
import re
import platform
import zipfile
from io import BytesIO
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog

# --- 核心邏輯 ---
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    path = filedialog.askdirectory(master=root)
    root.destroy()
    return path

# --- 介面 ---
st.set_page_config(page_title="爸爸的音樂幫手", page_icon="🎵")

if 'page' not in st.session_state:
    st.session_state.page = "convert"

with st.sidebar:
    st.title("功能選單")
    if st.button("🔄 1. 一鍵轉檔 (並下載)", use_container_width=True):
        st.session_state.page = "convert"
    if st.button("🔢 2. 重新排列日期 (隨身碟)", use_container_width=True):
        st.session_state.page = "sort"

if st.session_state.page == "convert":
    st.header("Step 1: 格式轉換")
    uploaded_files = st.file_uploader("選擇音訊檔", type=["wav", "aac"], accept_multiple_files=True)
    if uploaded_files:
        if st.button("開始轉檔並準備下載"):
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                for uploaded_file in uploaded_files:
                    audio = AudioSegment.from_file(uploaded_file)
                    mp3_data = BytesIO()
                    audio.export(mp3_data, format="mp3")
                    new_filename = os.path.splitext(uploaded_file.name)[0] + ".mp3"
                    zip_file.writestr(new_filename, mp3_data.getvalue())
            st.success("🎉 轉檔完成！")
            st.download_button("📥 下載所有 MP3 (ZIP)", data=zip_buffer.getvalue(), file_name="music.zip")

elif st.session_state.page == "sort":
    st.header("Step 2: 重新排列日期")
    if st.button("📁 選擇隨身碟資料夾"):
        path = select_folder()
        if path: st.session_state.target_path = path

    if 'target_path' in st.session_state:
        st.info(f"已選: {st.session_state.target_path}")
        if st.button("🚀 執行排列"):
            files = [f for f in os.listdir(st.session_state.target_path) if f.lower().endswith(".mp3")]
            files.sort(key=natural_sort_key)
            now = time.time()
            for i, f in enumerate(files):
                p = os.path.join(st.session_state.target_path, f)
                os.utime(p, (now + i*10, now + i*10))
            st.success("✅ 完成！")