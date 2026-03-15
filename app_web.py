import streamlit as st
import pandas as pd
import datetime
import os

# Nama file database di server
NAMA_FILE = 'database_tamu.csv'

# Judul Aplikasi
st.set_page_config(page_title="Buku Tamu Digital", page_icon="🛡️")
st.title("🛡️ GuestLog Digital - Pos Sekuriti")
st.markdown("---")

# Inisialisasi Database
if not os.path.exists(NAMA_FILE):
    df_init = pd.DataFrame(columns=['Waktu', 'Nama', 'Instansi', 'Keperluan'])
    df_init.to_csv(NAMA_FILE, index=False)

# --- Sidebar untuk Menu ---
menu = st.sidebar.selectbox("Pilih Menu", ["Input Tamu", "Lihat Database"])

if menu == "Input Tamu":
    st.subheader("📝 Catat Kunjungan Baru")
    
    with st.form("form_tamu", clear_on_submit=True):
        nama = st.text_input("Nama Lengkap")
        instansi = st.text_input("Asal Instansi")
        keperluan = st.text_area("Keperluan")
        submit = st.form_submit_button("Simpan Data")
        
        if submit:
            if nama and instansi and keperluan:
                waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                data_baru = pd.DataFrame([[waktu, nama, instansi, keperluan]], 
                                         columns=['Waktu', 'Nama', 'Instansi', 'Keperluan'])
                
                # Simpan ke CSV
                data_baru.to_csv(NAMA_FILE, mode='a', header=False, index=False)
                st.success(f"Berhasil! Data {nama} telah tersimpan.")
            else:
                st.error("Mohon isi semua kolom!")

elif menu == "Lihat Database":
    st.subheader("📊 Daftar Riwayat Tamu")
    
    # Membaca data
    df = pd.read_csv(NAMA_FILE)
    
    # Fitur Pencarian di Web
    cari = st.text_input("Cari Nama Tamu...")
    if cari:
        df = df[df['Nama'].str.contains(cari, case=False)]
    
    # Menampilkan Tabel
    st.dataframe(df, use_container_width=True)
    
    # Tombol Download Excel (Sangat berguna untuk laporan)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Laporan (CSV)", data=csv, file_name="laporan_tamu.csv", mime='text/csv')