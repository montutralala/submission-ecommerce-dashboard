# 🛒 Brazilian E-Commerce Analytics Dashboard

Dashboard interaktif untuk menganalisis data transaksi e-commerce Brasil dari dataset publik Olist (2016–2018), dibangun menggunakan **Python** dan **Streamlit**.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-link.streamlit.app)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56.0-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Deskripsi Proyek

Data ini merupakan tahap nalisis dilakukan terhadap **Brazilian E-Commerce Public Dataset** yang mencakup ~100.000 transaksi dari September 2016 hingga Oktober 2018.

### ❓ Pertanyaan Bisnis yang Dijawab

1. **Tren Revenue** — Bagaimana pertumbuhan pendapatan bulanan selama 2017–2018, dan kapan puncak serta penurunan terbesarnya?
2. **Performa Kategori** — Kategori produk mana yang menghasilkan revenue tertinggi dan volume penjualan terbanyak, serta bagaimana korelasinya dengan skor ulasan?
3. **Segmentasi Pelanggan** — Bagaimana distribusi pelanggan berdasarkan analisis RFM, dan kelompok mana yang paling bernilai?

---

## 🖥️ Preview Dashboard

| Tab | Isi |
|---|---|
| 📈 **Tren Revenue Bulanan** | Grafik bar + line chart revenue dan volume pesanan per bulan |
| 📦 **Performa Kategori Produk** | Ranking kategori berdasarkan revenue & volume + scatter plot review |
| 👥 **RFM Segmentasi Pelanggan** | Bar chart, pie chart, dan tabel ringkasan segmen RFM |

---

## 📊 Fitur Dashboard

- 🗓️ **Filter Rentang Waktu** — Filter seluruh data berdasarkan rentang tanggal
- 🔢 **Filter Top N Kategori** — Tampilkan top 5–20 kategori sesuai kebutuhan
- 📈 **Tren Revenue & Volume** — Visualisasi pertumbuhan bulanan dengan penanda puncak otomatis
- 📦 **Performa Kategori** — Bar chart horizontal + scatter plot korelasi review vs revenue
- 👥 **RFM Segmentasi** — Identifikasi Champions, Loyal, Potential, At Risk, dan Lost Customers
- 📋 **Tabel Data** — Expandable data table di setiap visualisasi

---

## 🧰 Library yang Digunakan

| Library | Versi | Kegunaan |
|---|---|---|
| `streamlit` | 1.56.0 | Framework dashboard interaktif |
| `pandas` | 3.0.2 | Manipulasi dan analisis data |
| `numpy` | 2.4.2 | Komputasi numerik |
| `matplotlib` | 3.10.9 | Visualisasi data |
| `seaborn` | 0.13.2 | Visualisasi statistik |
---

## 📂 Dataset

**Brazilian E-Commerce Public Dataset** oleh Olist via Kaggle:

- 🔗 [Kaggle — Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- 📅 Periode: September 2016 – Oktober 2018
- 📦 Jumlah pesanan: ~100.000
- 🗃️ Tabel relasional: 8 tabel (orders, items, customers, products, payments, reviews, sellers, category)

---

## 👤 Author

**Nathan Alfa Shidqi**

---

## 📄 License

Proyek ini menggunakan lisensi [MIT](LICENSE).
