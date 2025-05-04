import streamlit as st
import pandas as pd
import os
from fpdf import FPDF

# Load data
pkl_path = "absensi_mahasiswa.pkl"
if os.path.exists(pkl_path):
    df = pd.read_pickle(pkl_path)
else:
    df = pd.DataFrame(columns=["NIM", "Nama", "Jenis Kelamin", "Kelas", "Status"])

st.title("App Absensi Mahasiswa")

# Tampilkan daftar absensi
st.subheader("Daftar Kehadiran Mahasiswa")

row_top = st.columns([20, 2])
with row_top[1]:
    cek_all = st.checkbox("")

header_cols = st.columns([2, 3, 2, 2, 1]) 
header_cols[0].markdown("**NIM**")
header_cols[1].markdown("**Nama**")
header_cols[2].markdown("**Jenis Kelamin**")
header_cols[3].markdown("**Kelas**")
header_cols[4].markdown("**Status**")

# Checklist per mahasiswa
if cek_all:
    df["Status"] = True

for i in df.index:
    cols = st.columns([2, 3, 2, 2, 1])
    cols[0].write(df.at[i, "NIM"])
    cols[1].write(df.at[i, "Nama"])
    cols[2].write(df.at[i, "Jenis Kelamin"])
    cols[3].write(df.at[i, "Kelas"])
    df.at[i, "Status"] = cols[4].checkbox(
        "", value=df.at[i, "Status"], key=f"absen_{i}"
    )

# Simpan & Export
col_kiri, col_kanan = st.columns(2)
with col_kiri:
    if st.button("💾 Simpan Absensi"):
        df.to_pickle(pkl_path)
        st.success("Absensi berhasil disimpan.")

with col_kanan:
    def export_pdf(dataframe):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Laporan Absensi Mahasiswa", ln=True, align="C")
        pdf.ln(10)
        for idx, row in dataframe.iterrows():
            line = f"{row['NIM']} - {row['Nama']} - {row['Jenis Kelamin']} - {row['Kelas']} - {'Hadir' if row['Status'] else 'Tidak Hadir'}"
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output("laporan_absensi.pdf")

    if st.button("📄 Export PDF"):
        export_pdf(df)
        with open("laporan_absensi.pdf", "rb") as file:
            st.download_button("⬇️ Download PDF", file, "laporan_absensi.pdf")

# Tambah Mahasiswa
st.markdown("---")
with st.expander("➕ Tambah Mahasiswa"):
    with st.form("form_tambah"):
        col1, col2 = st.columns(2)
        with col1:
            nim = st.text_input("NIM")
            nama = st.text_input("Nama")
        with col2:
            jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
            kelas = st.text_input("Kelas")
        submitted = st.form_submit_button("Tambah")
        if submitted:
            if nim and nama and kelas:
                new_row = pd.DataFrame([{
                    "NIM": nim,
                    "Nama": nama,
                    "Jenis Kelamin": jk,
                    "Kelas": kelas,
                    "Status": False
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_pickle(pkl_path)
                st.success(f"Mahasiswa {nama} berhasil ditambahkan dan ditampilkan di daftar.")
                st.rerun()
            else:
                st.warning("Mohon lengkapi semua kolom.")
