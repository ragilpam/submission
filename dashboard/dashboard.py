import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='whitegrid')

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# LOAD DATASET
@st.cache_data
def load_data():
    all_data_df = pd.read_csv('https://raw.githubusercontent.com/ragilpam/bike-sharing/refs/heads/main/all_data.csv')
    
    # Mapping season
    season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
    all_data_df["season"] = all_data_df["season"].map(season_mapping)

    # Mapping weekday
    weekday_mapping = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu",
                       4: "Kamis", 5: "Jumat", 6: "Sabtu"}
    all_data_df["weekday"] = all_data_df["weekday"].map(weekday_mapping)

    # Mapping cuaca
    weathersit_mapping = {1: "Cerah", 2: "Berawan/Berkabut",
                          3: "Hujan/Salju Ringan", 4: "Hujan/Salju Lebat"}
    all_data_df["weathersit"] = all_data_df["weathersit"].map(weathersit_mapping)
    
    # Grouping
    grouped_season = all_data_df.groupby("season")["cnt"].sum().reset_index()
    grouped_weekday = all_data_df.groupby("weekday")["cnt"].sum().reindex(
        ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]
    ).reset_index()
    grouped_user = all_data_df.groupby("weekday")[["casual", "registered"]].sum().reindex(
        ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]
    ).reset_index()
    grouped_hour = all_data_df.groupby("hr")["cnt"].sum().reset_index()


    return all_data_df, grouped_season, grouped_weekday, grouped_user, grouped_hour

(all_data_df, all_data_df_season, all_data_df_weekday, all_data_df_user, all_data_df_hour) = load_data()


# SIDEBAR
st.sidebar.image("https://raw.githubusercontent.com/ragilpam/submission/main/dashboard/logo.png", use_container_width=True)
st.sidebar.title("🚲 Bike Sharing Dashboard 🚲")
menu = st.sidebar.radio("Pilih Tampilan:", [
    "Informasi Umum", 
    "Analisis Pola Waktu", 
    "Analisis Cuaca", 
    "Informasi Pengguna Casual vs Registered",
    "Informasi Jam Penyewaan Tertinggi"
])

st.sidebar.markdown("---")
st.sidebar.caption("Created by Ragilpam")


# 1️⃣ INFORMASI UMUM
if menu == "Informasi Umum":
    st.title("📊 Informasi Umum")

    st.markdown("Informasi total penyewaan sepeda dari 1 Januari 2011 - 31 Desember 2012.")

    st.subheader("Total Penyewaan Sepeda")
    total_cnt = all_data_df["cnt"].sum()
    casual = all_data_df["casual"].sum()
    registered = all_data_df["registered"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Penyewaan", f"{total_cnt:,}")
    col2.metric("Pengguna Casual", f"{casual:,}")
    col3.metric("Pengguna Registered", f"{registered:,}")

    with st.expander("Lihat Sampel Data"):
        st.dataframe(all_data_df.head())

# 2️⃣ ANALISIS POLA WAKTU
elif menu == "Analisis Pola Waktu":
    st.title("⏰ Analisis Pola Waktu")
    st.markdown("Melihat pola penyewaan berdasarkan **musim, bulan, hari kerja, dan akhir pekan**.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Penyewaan Berdasarkan Musim")

        # Visualisasi
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(data=all_data_df_season, x="season", y="cnt", palette="pastel", ax=ax)
        ax.set_title("Total Penyewaan per Musim", fontsize=12, weight="bold")
        ax.set_xlabel("Musim", fontsize=12, weight="bold")
        ax.set_ylabel("Total Penyewaan", fontsize=12, weight="bold")
        ax.ticklabel_format(style='plain', axis='y')
        st.pyplot(fig)

    with col2:
        st.subheader("Penyewaan Berdasarkan Hari")

        # Visualisasi
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(data=all_data_df_weekday, x="weekday", y="cnt", palette="coolwarm", ax=ax)
        ax.set_title("Total Penyewaan per Hari", fontsize=12, weight="bold")
        ax.set_xlabel("Hari", fontsize=12, weight="bold")
        ax.set_ylabel("Total Penyewaan", fontsize=12, weight="bold")
        ax.ticklabel_format(style='plain', axis='y')
        st.pyplot(fig)

    st.subheader("Pola Penyewaan per Jam")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=all_data_df, x="hr", y="cnt", marker="o", color="royalblue", ax=ax)
    ax.set_title("Pola Penyewaan per Jam", fontsize=16, weight="bold")
    ax.set_xlabel("Jam", fontsize=14, weight="bold")
    ax.set_ylabel("Total Penyewaan", fontsize=14, weight="bold")
    ax.set_xticks(range(0, 24))
    st.pyplot(fig)


# 3️⃣ ANALISIS CUACA
elif menu == "Analisis Cuaca":
    st.title("🌦️ Analisis Berdasarkan Cuaca")

    st.markdown("Cuaca berperan penting dalam jumlah penyewaan sepeda.")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=all_data_df, x="weathersit", y="cnt", palette="pastel", ax=ax)
    ax.set_title("Total Penyewaan Berdasarkan Cuaca", fontsize=16, weight="bold")
    ax.set_xlabel("Cuaca", fontsize=14, weight="bold")
    ax.set_ylabel("Total Penyewaan", fontsize=14, weight="bold")
    st.pyplot(fig)

    # Informasi Tambahan
    st.markdown("""
    💡 **Informasi:**
        Cuaca cerah mendominasi jumlah peminjaman tertinggi, sedangkan saat hujan atau salju jumlahnya menurun drastis.
    """)


# 4️⃣ PENGGUNA CASUAL VS REGISTERED
elif menu == "Informasi Pengguna Casual vs Registered":
    st.title("👥 Perbandingan Pengguna Casual vs Registered")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(8, 4))
    all_data_df_user.plot(x="weekday", y=["casual", "registered"], kind="bar", color=["royalblue", "pink"], ax=ax)
    ax.set_title("Total Peminjaman per Hari", fontsize=16, weight="bold")
    ax.set_xlabel("Hari", fontsize=14, weight="bold")
    ax.set_ylabel("Total Penyewaan", fontsize=14, weight="bold")
    ax.legend(["Casual", "Registered"], title="Jenis Pengguna")
    st.pyplot(fig)

    # Informasi Tambahan
    st.markdown("""
    💡 **Informasi:**  
    - Pengguna **casual** cenderung lebih aktif di akhir pekan.  
    - Pengguna **registered** lebih aktif di hari kerja.
    """)


# 5️⃣ JAM PENYEWAAN TERTINGGI
elif menu == "Informasi Jam Penyewaan Tertinggi":
    st.title("🕒 Analisis Jam Penyewaan Tertinggi")

    st.markdown("Menunjukkan jam-jam di mana jumlah penyewaan sepeda paling tinggi.")

    # Hitung total penyewaan per jam
    jam_tertinggi = all_data_df_hour.loc[all_data_df_hour["cnt"].idxmax()]

    # Tampilkan jam penyewaan tertinggi
    st.metric(
        label="⏰ Jam dengan Penyewaan Tertinggi",
        value=f"{int(jam_tertinggi['hr'])}:00",
        delta=f"{int(jam_tertinggi['cnt']):,} penyewaan"
    )

    # Visualisasi pola penyewaan per jam
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=all_data_df_hour, x="hr", y="cnt", marker="o", color="royalblue", ax=ax)
    ax.set_title("Total Penyewaan Sepeda per Jam", fontsize=16, weight="bold")
    ax.set_xlabel("Jam (0–23)", fontsize=14, weight="bold")
    ax.set_ylabel("Total Penyewaan", fontsize=14, weight="bold")
    ax.axvline(jam_tertinggi["hr"], color="red", linestyle="--", label="Puncak Penyewaan")
    ax.set_xticks(range(0, 24))
    ax.legend()
    st.pyplot(fig)

    # Informasi tambahan
    st.markdown(f"""
    💡 **Informasi:**  
    - Jam dengan penyewaan tertinggi adalah sekitar **{int(jam_tertinggi['hr'])}:00**.  
    - Hal ini menunjukkan puncak aktivitas pengguna sepeda, biasanya bertepatan dengan jam **pulang kerja, rekreasi atau waktu santai para pengguna**.

    """)


