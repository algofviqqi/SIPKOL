# -*- coding: utf-8 -*-
import streamlit as st
import requests

# 1. Konfigurasi Halaman & Tema Dasar
st.set_page_config(
    page_title="Breast Cancer Diagnostics",
    page_icon="🎗️",
    layout="wide"
)

# 2. Sentuhan Warna Kustom via CSS
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
st.markdown("Aplikasi diagnosis kanker payudara berbasis *Machine Learning* (SVM). Silakan isi parameter di bawah.")
st.markdown("---")

# 4. Layout Utama (Kiri untuk Input, Kanan untuk Hasil)
col_input, col_result = st.columns([2, 1], gap="large")

with col_input:
    st.subheader("📋 Input Parameter Fitur")
    
    # Memisahkan 30 fitur ke dalam 3 Tab agar rapi
    tab1, tab2, tab3 = st.tabs(["Fitur 1-10", "Fitur 11-20", "Fitur 21-30"])
    inputs = [0.0] * 30 

    # Tab 1
    with tab1:
        sub_col1, sub_col2 = st.columns(2)
        for i in range(10):
            target_col = sub_col1 if i % 2 == 0 else sub_col2
            with target_col:
                inputs[i] = st.number_input(f"Feature {i+1}", min_value=0.0, value=0.25, step=0.01, key=f"f_{i}")

    # Tab 2
    with tab2:
        sub_col1, sub_col2 = st.columns(2)
        for i in range(10, 20):
            target_col = sub_col1 if i % 2 == 0 else sub_col2
            with target_col:
                inputs[i] = st.number_input(f"Feature {i+1}", min_value=0.0, value=0.10, step=0.01, key=f"f_{i}")

    # Tab 3
    with tab3:
        sub_col1, sub_col2 = st.columns(2)
        for i in range(20, 30):
            target_col = sub_col1 if i % 2 == 0 else sub_col2
            with target_col:
                inputs[i] = st.number_input(f"Feature {i+1}", min_value=0.0, value=0.05, step=0.01, key=f"f_{i}")

    st.markdown(" ")
    predict_btn = st.button("🚀 Lakukan Prediksi Diagnosis", type="primary", use_container_width=True)

# 5. Bagian Kanan (Output Analisis)
with col_result:
    st.subheader("📊 Hasil Analisis")
    
    if predict_btn:
        with st.spinner('Menghubungkan ke server model...'):
            try:
                url = "https://sipkol.vercel.app/predict"
                response = requests.post(url, json={"features": inputs}, timeout=10)
                
                if response.status_code == 200:
                    hasil = response.json()
                    
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    
                    prediction_text = hasil['prediction']
                    # Logika warna teks hasil berdasarkan nilai prediksi
                    if "malignant" in str(prediction_text).lower() or str(prediction_text) == "1":
                        st.error(f"### Hasil: {prediction_text}")
                    else:
                        st.success(f"### Hasil: {prediction_text}")
                    
                    st.metric(label="Tingkat Keyakinan Model (Probability)", value=f"{hasil['probability']:.2%}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Gagal mengambil data. Error code: {response.status_code}")
            except Exception as e:
                st.error(f"Gagal terhubung ke API: {e}")
    else:
        st.info("Isi data di sebelah kiri, lalu klik tombol prediksi untuk memproses.")
