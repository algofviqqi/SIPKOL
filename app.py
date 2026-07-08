# -*- coding: utf-8 -*-
"""
Aplikasi Web Frontend Streamlit - Breast Cancer Prediction
Menggunakan model SVM melalui API Backend Vercel
"""

import streamlit as st
import requests

# 1. Konfigurasi Halaman & Tema Dasar
st.set_page_config(
    page_title="Breast Cancer Diagnostics",
    page_icon="🎗️",
    layout="wide"
)

# 2. Sentuhan Warna Kustom via CSS (Mempercantik Font & Card Kontainer)
st.markdown("""
    <style>
    /* Background aplikasi utama */
    .stApp {
        background-color: #fdfbfb;
    }
    /* Mengubah warna teks judul utama */
    h1 {
        color: #721c24 !important;
        font-weight: 700;
    }
    /* Desain kotak untuk hasil prediksi */
    .result-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #e83e8c;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Aplikasi
st.title("🎗️ Breast Cancer Prediction Dashboard")
st.markdown("Aplikasi diagnosis kanker payudara berbasis *Machine Learning* (Backend: SVM). Silakan isi parameter klinis di bawah ini.")
st.markdown("---")

# 4. Layout Utama (Membagi Halaman: Kiri untuk Input, Kanan untuk Hasil)
col_input, col_result = st.columns([2, 1], gap="large")

with col_input:
    st.subheader("📋 Input Parameter Fitur")
    st.info("Silakan masukkan nilai untuk ke-30 fitur di bawah ini. Fitur telah dibagi menjadi 3 kelompok agar mempermudah pengisian.")
    
    # Memisahkan 30 fitur ke dalam 3 Tab agar halaman tidak terlalu panjang ke bawah
    tab1, tab2, tab3 = st.tabs(["Fitur 1-10", "Fitur 11-20", "Fitur 21-30"])
    inputs = [0.0] * 30 

    # --- TAB 1: Fitur 1 - 10 ---
    with tab1:
        sub_col1, sub_col2 = st.columns(2)
        for i in range(10):
            target_col = sub_col1 if i % 2 == 0 else sub_col2
            with target_col:
                inputs[i] = st.number_input(f"Feature {i+1}", min_value=0.0, value=0.25, step=0.01, key=f"f_{i}")

    # --- TAB 2: Fitur 11 - 20 ---
    with tab2:
        sub_col1, sub_col2 = st.columns(2)
        for i in range(10, 20):
            target_col = sub_col1 if i % 2 == 0 else sub_col2
            with target_col:
                inputs[i] = st.number_input(f"Feature {i+1}", min_value=0.0, value=0.10, step=0.01, key=f"f_{i}")

    # --- TAB 3: Fitur 21 - 30 ---
    with tab3:
        sub_col1, sub_col2 = st.columns(2)
        for i in range(20, 30):
            target_col = sub_col1 if i % 2 == 0 else sub_col2
            with target_col:
                inputs[i] = st.number_input(f"Feature {i+1}", min_value=0.0, value=0.05, step=0.01, key=f"f_{i}")

    st.markdown(" ")
    # Tombol Prediksi dengan ukuran penuh mengikuti lebar kolom
    predict_btn = st.button("🚀 Lakukan Prediksi Diagnosis", type="primary", use_container_width=True)

# 5. Bagian Kanan (Output Analisis & Keterangan Hasil Lengkap)
with col_result:
    st.subheader("📊 Hasil Analisis")
    
    if predict_btn:
        with st.spinner('Menghubungkan ke server model untuk pemrosesan...'):
            try:
                url = "https://sipkol.vercel.app/predict"
                response = requests.post(url, json={"features": inputs}, timeout=10)
                
                if response.status_code == 200:
                    hasil = response.json()
                    prediction_val = str(hasil['prediction']).strip()
                    probabilitas = hasil['probability']
                    
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    
                    # --- LOGIKA PENJELASAN BERDASARKAN HASIL PREDIKSI ---
                    if prediction_val == "1" or "malignant" in prediction_val.lower():
                        st.error("### Hasil: Terindikasi Ganas (Malignant)")
                        
                        # Menampilkan metrik rincian nilai
                        st.markdown(f"""
                        **Rincian Output Model:**
                        * 🔢 **Angka Prediksi (Class):** `{prediction_val}`
                        * 📋 **Istilah Medis:** Malignant (Kanker Ganas)
                        * 🎯 **Confidence (Probabilitas):** `{probabilitas:.2%}`
                        
                        ---
                        **Keterangan Klinis:** Model mendeteksi karakteristik massa sel yang mengarah pada keganasan (*Malignant*) dengan tingkat keyakinan sebesar **{probabilitas:.2%}**.
                        
                        ⚠️ **Rekomendasi Tindakan:** 
                        * Hasil ini merupakan prediksi awal berdasarkan komputasi sistem cerdas SVM dan **bukan** merupakan diagnosis final medis resmi.
                        * Sangat disarankan untuk segera berkonsultasi dengan Dokter Spesialis Onkologi guna pemeriksaan lebih lanjut seperti Biopsi atau Mammografi ulang.
                        """)
                        
                    else:
                        st.success("### Hasil: Terindikasi Jinak (Benign)")
                        
                        # Menampilkan metrik rincian nilai
                        st.markdown(f"""
                        **Rincian Output Model:**
                        * 🔢 **Angka Prediksi (Class):** `{prediction_val}`
                        * 📋 **Istilah Medis:** Benign (Tumor Jinak / Non-Kanker)
                        * 🎯 **Confidence (Probabilitas):** `{probabilitas:.2%}`
                        
                        ---
                        **Keterangan Klinis:** Model mendeteksi karakteristik massa sel yang mengarah pada sifat jinak (*Benign*) atau non-kanker dengan tingkat keyakinan sebesar **{probabilitas:.2%}**.
                        
                        ✅ **Rekomendasi Tindakan:** 
                        * Meskipun hasil model menunjukkan indikasi aman, tetap lakukan pemeriksaan payudara sendiri (SADARI) secara berkala.
                        * Jika di kemudian hari Anda merasakan adanya perubahan fisik atau gejala klinis yang janggal, tetap konsultasikan dengan tenaga medis profesional.
                        """)
                    
                    # Menampilkan metrik angka probabilitas secara visual di bawah teks penjelasan
                    st.divider()
                    st.metric(label="Tingkat Keyakinan Model (Probability)", value=f"{probabilitas:.2%}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Gagal mengambil data dari API Vercel. Error code: {response.status_code}")
            except Exception as e:
                st.error(f"Gagal terhubung ke API Backend: {e}")
    else:
        # Tampilan standby saat pengguna baru pertama kali membuka web
        st.info("Silakan isi parameter fitur di panel sebelah kiri, lalu klik tombol **Lakukan Prediksi Diagnosis** untuk melihat ringkasan medis hasil analisis.")

# 6. Bagian Footer Rata Tengah (Pernyataan Tema & Identitas Hak Cipta)
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.85rem; line-height: 1.6;">
        © 2026 Breast Cancer Prediction Dashboard — Komputasi Cerdas Deteksi Dini Kanker Payudara dengan SVM <br>
        Sistem ini dikembangkan secara akademis oleh: <strong>ABDUL ROHMAN ALGOFVIQQI SUGIARTO</strong> (NIM: <strong>G.231.21.0177</strong>)
    </div>
""", unsafe_allow_html=True)
