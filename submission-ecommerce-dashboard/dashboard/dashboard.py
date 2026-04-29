import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 120,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base     = os.path.dirname(__file__)
    main_df  = pd.read_csv(os.path.join(base, "main_data.csv"),
                           parse_dates=["order_purchase_timestamp"])
    rfm_df   = pd.read_csv(os.path.join(base, "rfm_data.csv"))
    cat_perf = pd.read_csv(os.path.join(base, "category_performance.csv"))
    return main_df, rfm_df, cat_perf

main_df, rfm_df, cat_perf = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🛒 E-Commerce Dashboard")
    st.markdown("**Brazilian E-Commerce Public Dataset**")
    st.divider()

    st.subheader("📅 Filter Rentang Waktu")
    min_date = main_df["order_purchase_timestamp"].dt.date.min()
    max_date = main_df["order_purchase_timestamp"].dt.date.max()

    date_range = st.date_input(
        "Pilih rentang tanggal:",
        value=(pd.to_datetime("2017-01-01").date(),
               pd.to_datetime("2018-08-31").date()),
        min_value=min_date,
        max_value=max_date
    )
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    st.divider()
    st.subheader("🔢 Filter Top N Kategori")
    top_n = st.slider("Tampilkan top N kategori:", min_value=5, max_value=20, value=10, step=1)

    st.divider()
    st.markdown("**Dibuat oleh:** Nathan Alfa Shidqi")

# ─────────────────────────────────────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────────────────────────────────────
filtered_df = main_df[
    (main_df["order_purchase_timestamp"].dt.date >= start_date) &
    (main_df["order_purchase_timestamp"].dt.date <= end_date)
].copy()

# ─────────────────────────────────────────────────────────────────────────────
# HEADER & METRICS
# ─────────────────────────────────────────────────────────────────────────────
st.title("🛒 Brazilian E-Commerce Analytics Dashboard")
st.divider()

total_revenue   = filtered_df["price"].sum()
total_orders    = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_unique_id"].nunique()
avg_review      = filtered_df["review_score"].mean()
avg_order_val   = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Total Revenue",    f"R$ {total_revenue:,.0f}")
col2.metric("📦 Total Pesanan",    f"{total_orders:,}")
col3.metric("👥 Total Pelanggan",  f"{total_customers:,}")
col4.metric("⭐ Avg Review Score", f"{avg_review:.2f} / 5")
col5.metric("🧾 Avg Order Value",  f"R$ {avg_order_val:,.2f}")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TAB NAVIGASI
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📈 Tren Revenue Bulanan",
    "📦 Performa Kategori Produk",
    "👥 RFM Segmentasi Pelanggan"
])

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 1 — TREN REVENUE BULANAN                                            ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab1:
    filtered_df["purchase_yearmonth"] = (
        filtered_df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    )
    monthly_filt = (
        filtered_df
        .groupby("purchase_yearmonth", as_index=False)
        .agg(total_revenue=("price", "sum"), total_orders=("order_id", "nunique"))
        .sort_values("purchase_yearmonth")
    )

    fig, axes = plt.subplots(2, 1, figsize=(13, 8), sharex=True)
    fig.suptitle("Tren Revenue & Volume Pesanan Bulanan (2017–2018)",
                 fontsize=14, fontweight="bold")

    x = range(len(monthly_filt))

    # Panel atas: Revenue
    bars = axes[0].bar(x, monthly_filt["total_revenue"] / 1e6,
                       color="steelblue", edgecolor="white", linewidth=0.5)
    if len(monthly_filt) > 0:
        max_idx = monthly_filt["total_revenue"].idxmax()
        bars[max_idx].set_color("#e05c2a")
        axes[0].annotate(
            f'Puncak\nR${monthly_filt["total_revenue"].max()/1e6:.2f}M',
            xy=(max_idx, monthly_filt["total_revenue"].max() / 1e6),
            xytext=(max_idx + 1.2, monthly_filt["total_revenue"].max() / 1e6 * 0.9),
            arrowprops=dict(arrowstyle="->", color="#e05c2a"),
            color="#e05c2a", fontsize=8, fontweight="bold"
        )
    axes[0].set_ylabel("Total Revenue (Juta BRL)")
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.1f}M"))
    axes[0].set_title("Total Revenue Bulanan", fontsize=11)
    axes[0].grid(axis="y", alpha=0.3)

    # Panel bawah: Volume
    axes[1].plot(x, monthly_filt["total_orders"], marker="o",
                 color="darkorange", linewidth=2, markersize=5, zorder=3)
    axes[1].fill_between(x, monthly_filt["total_orders"], alpha=0.15, color="darkorange")
    axes[1].set_ylabel("Jumlah Pesanan")
    axes[1].set_title("Volume Pesanan Bulanan", fontsize=11)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(monthly_filt["purchase_yearmonth"],
                            rotation=45, ha="right", fontsize=7)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    axes[1].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 2 — PERFORMA KATEGORI PRODUK                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab2:
    cat_filt = (
        filtered_df
        .groupby("product_category_name_english", as_index=False)
        .agg(
            total_revenue=("price", "sum"),
            total_orders=("order_id", "count"),
            avg_review=("review_score", "mean")
        )
        .sort_values("total_revenue", ascending=False)
    )

    top_rev = cat_filt.head(top_n)
    top_vol = cat_filt.sort_values("total_orders", ascending=False).head(top_n)

    # Bar chart revenue & volume
    fig, axes = plt.subplots(1, 2, figsize=(16, max(5, top_n * 0.5 + 1)))
    fig.suptitle(f"Top {top_n} Kategori Produk — Revenue vs Volume (2017–2018)",
                 fontsize=13, fontweight="bold")

    pal_rev = ["#1a5276" if i == 0 else "#2980b9" for i in range(top_n)]
    pal_vol = ["#784212" if i == 0 else "#e67e22" for i in range(top_n)]

    b1 = axes[0].barh(top_rev["product_category_name_english"][::-1],
                      top_rev["total_revenue"][::-1] / 1e6,
                      color=pal_rev[::-1], edgecolor="white")
    for bar, val in zip(b1, top_rev["total_revenue"][::-1]):
        axes[0].text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2,
                     f"R${val/1e6:.2f}M", va="center", fontsize=7)
    axes[0].set_xlabel("Total Revenue (Juta BRL)")
    axes[0].set_title("Revenue Tertinggi", fontsize=11)
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.1f}M"))
    axes[0].grid(axis="x", alpha=0.3)

    b2 = axes[1].barh(top_vol["product_category_name_english"][::-1],
                      top_vol["total_orders"][::-1],
                      color=pal_vol[::-1], edgecolor="white")
    for bar, val in zip(b2, top_vol["total_orders"][::-1]):
        axes[1].text(bar.get_width() + 10, bar.get_y() + bar.get_height() / 2,
                     f"{int(val):,}", va="center", fontsize=7)
    axes[1].set_xlabel("Jumlah Pesanan")
    axes[1].set_title("Volume Penjualan Tertinggi", fontsize=11)
    axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    axes[1].grid(axis="x", alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Scatter: Review Score vs Revenue
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sc = ax2.scatter(
        cat_filt["avg_review"],
        cat_filt["total_revenue"] / 1e6,
        s=cat_filt["total_orders"] / 20,
        c=cat_filt["total_orders"],
        cmap="YlOrRd", alpha=0.7, edgecolors="gray", linewidth=0.4
    )
    for _, row in cat_filt.head(5).iterrows():
        ax2.annotate(row["product_category_name_english"],
                     xy=(row["avg_review"], row["total_revenue"] / 1e6),
                     xytext=(4, 4), textcoords="offset points", fontsize=7)
    cb = plt.colorbar(sc, ax=ax2)
    cb.set_label("Volume Penjualan", fontsize=9)
    ax2.set_xlabel("Rata-Rata Skor Ulasan (1–5)")
    ax2.set_ylabel("Total Revenue (Juta BRL)")
    ax2.set_title("Korelasi Review Score vs Revenue per Kategori\n(ukuran bubble = volume penjualan)",
                  fontsize=11)
    ax2.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  TAB 3 — RFM SEGMENTASI PELANGGAN                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
with tab3:
    segment_order = ["Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Lost Customers"]
    colors_map = {
        "Champions":           "#1abc9c",
        "Loyal Customers":     "#3498db",
        "Potential Loyalists": "#f39c12",
        "At Risk":             "#e74c3c",
        "Lost Customers":      "#95a5a6"
    }

    seg_summary = (
        rfm_df.groupby("segment", as_index=False)
        .agg(
            jumlah_pelanggan=("customer_unique_id", "count"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
            total_revenue=("monetary", "sum")
        )
    )
    seg_summary = seg_summary[seg_summary["segment"].isin(segment_order)].copy()
    seg_summary["segment"] = pd.Categorical(
        seg_summary["segment"], categories=segment_order, ordered=True
    )
    seg_summary = seg_summary.sort_values("segment")
    bar_colors  = [colors_map.get(s, "gray") for s in seg_summary["segment"]]

    # Bar charts: jumlah, revenue, avg monetary
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("Segmentasi Pelanggan Berdasarkan RFM Analysis (2017–2018)",
                 fontsize=13, fontweight="bold")

    b0 = axes[0].bar(seg_summary["segment"], seg_summary["jumlah_pelanggan"],
                     color=bar_colors, edgecolor="white")
    for bar, val in zip(b0, seg_summary["jumlah_pelanggan"]):
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 100,
                     f"{int(val):,}", ha="center", fontsize=8, fontweight="bold")
    axes[0].set_title("Jumlah Pelanggan per Segmen", fontsize=10)
    axes[0].set_ylabel("Jumlah Pelanggan")
    axes[0].set_xticklabels(seg_summary["segment"], rotation=20, ha="right", fontsize=7)
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    axes[0].grid(axis="y", alpha=0.3)

    b1 = axes[1].bar(seg_summary["segment"], seg_summary["total_revenue"] / 1e6,
                     color=bar_colors, edgecolor="white")
    for bar, val in zip(b1, seg_summary["total_revenue"]):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                     f"R${val/1e6:.2f}M", ha="center", fontsize=8, fontweight="bold")
    axes[1].set_title("Total Revenue per Segmen", fontsize=10)
    axes[1].set_ylabel("Total Revenue (Juta BRL)")
    axes[1].set_xticklabels(seg_summary["segment"], rotation=20, ha="right", fontsize=7)
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.1f}M"))
    axes[1].grid(axis="y", alpha=0.3)

    b2 = axes[2].bar(seg_summary["segment"], seg_summary["avg_monetary"],
                     color=bar_colors, edgecolor="white")
    for bar, val in zip(b2, seg_summary["avg_monetary"]):
        axes[2].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                     f"R${val:.0f}", ha="center", fontsize=8, fontweight="bold")
    axes[2].set_title("Rata-Rata Pengeluaran per Pelanggan", fontsize=10)
    axes[2].set_ylabel("Rata-Rata Monetary (BRL)")
    axes[2].set_xticklabels(seg_summary["segment"], rotation=20, ha="right", fontsize=7)
    axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"R${v:.0f}"))
    axes[2].grid(axis="y", alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Pie chart proporsi segmen
    fig3, ax3 = plt.subplots(figsize=(7, 7))
    pie_data   = seg_summary.set_index("segment")["jumlah_pelanggan"]
    pie_colors = [colors_map.get(s, "gray") for s in pie_data.index]
    wedges, texts, autotexts = ax3.pie(
        pie_data,
        labels=pie_data.index,
        colors=pie_colors,
        autopct=lambda p: f"{p:.1f}%\n({int(p/100*pie_data.sum()):,})",
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(edgecolor="white", linewidth=2)
    )
    for t in autotexts:
        t.set_fontsize(8)
    ax3.set_title("Proporsi Segmen Pelanggan Berdasarkan RFM Analysis",
                  fontsize=12, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center; color:gray; font-size:12px;'>"
    "Brazilian E-Commerce Analytics Dashboard · Nathan Alfa Shidqi · "
    "Olist E-Commerce Public Dataset (2016–2018)"
    "</div>",
    unsafe_allow_html=True
)
