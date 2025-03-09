import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ========================== DASHBOARD ANALISIS PEMINJAMAN SEPEDA ==========================
st.title("Dashboard Analisis Peminjaman Sepeda")
st.write("Dashboard ini menampilkan analisis berdasarkan musim dan waktu dalam sehari.")

# ========================== BAGIAN 1: ANALISIS BERDASARKAN MUSIM ==========================
st.header("Analisis Berdasarkan Musim")

# Mengunduh dataset harian
url_day = "https://raw.githubusercontent.com/zarifaayyasy/BikeSharing/refs/heads/main/Data/day.csv"
df_day = pd.read_csv(url_day, parse_dates=["dteday"])

# Ubah kode musim jadi label yang lebih mudah dipahami
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df_day["season"] = df_day["season"].map(season_labels)

# Hitung total peminjaman sepeda tiap musim
seasonal_rentals = df_day.groupby("season")["cnt"].sum().reset_index()

# Cari musim dengan peminjaman tertinggi dan terendah
most_rentals = seasonal_rentals.loc[seasonal_rentals["cnt"].idxmax()]
least_rentals = seasonal_rentals.loc[seasonal_rentals["cnt"].idxmin()]

# Urutkan musim sesuai keinginan tampilannya
season_order = ["Spring", "Summer", "Fall", "Winter"]

# Atur warna batang: yang tertinggi (biru), yang terendah (merah), sisanya abu-abu
bar_colors = [
    "gray" if season not in [most_rentals["season"], least_rentals["season"]]
    else "#72BCD4" if season == most_rentals["season"]
    else "#D9534F"
    for season in season_order
]

# Buat bar chart
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=seasonal_rentals, x="season", y="cnt", order=season_order, palette=bar_colors, ax=ax1)

# Tambahkan teks jumlah peminjaman pada bar tertinggi dan terendah
ax1.text(season_order.index(most_rentals["season"]), most_rentals["cnt"], f"{most_rentals['cnt']:,}",
         ha='center', va='bottom', fontsize=12, fontweight='bold', color="black")
ax1.text(season_order.index(least_rentals["season"]), least_rentals["cnt"], f"{least_rentals['cnt']:,}",
         ha='center', va='top', fontsize=12, fontweight='bold', color="black")

ax1.set_xlabel("Musim")
ax1.set_ylabel("Total Peminjaman Sepeda")
ax1.set_title("Perbandingan Peminjaman Sepeda Berdasarkan Musim")
ax1.grid(axis="y", linestyle="--", alpha=0.7)

st.pyplot(fig1)

st.write(f"*Musim dengan penyewa terbanyak:* {most_rentals['season']} ({most_rentals['cnt']:,} peminjaman)")
st.write(f"*Musim dengan penyewa terendah:* {least_rentals['season']} ({least_rentals['cnt']:,} peminjaman)")

# ========================== BAGIAN 2: ANALISIS BERDASARKAN JAM ==========================
st.header("Analisis Berdasarkan Jam")

# Mengunduh dataset per jam
url_hour = "https://raw.githubusercontent.com/zarifaayyasy/BikeSharing/refs/heads/main/Data/hour.csv"
df_hour = pd.read_csv(url_hour)

# Pastikan kolom "hr" ada di dataset
if "hr" in df_hour.columns:
    # Hitung rata-rata peminjaman per jam
    avg_rentals_hour = df_hour.groupby("hr")["cnt"].mean().reset_index()

    # Buat line chart untuk melihat tren peminjaman per jam
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=avg_rentals_hour, x="hr", y="cnt", marker="o", color="b", linewidth=2, ax=ax2)
    
    ax2.set_xticks(range(0, 24))
    ax2.set_xlabel("Jam dalam Sehari")
    ax2.set_ylabel("Rata-rata Peminjaman Sepeda")
    ax2.set_title("Pola Peminjaman Sepeda Berdasarkan Waktu")
    ax2.grid(True)
    
    st.pyplot(fig2)
else:
    st.error("Kolom 'hr' tidak ditemukan. Pastikan kamu menggunakan dataset 'hour.csv'.")