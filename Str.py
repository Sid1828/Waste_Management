#!/usr/bin/env python
# coding: utf-8

# In[17]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===== 1. PAGE CONFIG =====
st.set_page_config(
    page_title="Waste Management Trade Dashboard",
    layout="wide"
)

st.title("Waste Management Trade Dashboard")
st.write("Interactive dashboard built from the Final Waste Management dataset.")

# ===== 2. DATA LOADING =====
@st.cache_data
def load_data():
    # TODO: change path if needed
    path = r"C:\Users\SIDDHARTH EKBOTE\Downloads\Final Waste Management Data (1).xlsx"
    df = pd.read_excel(path)

    # Keep the same cleaning/renaming you did in the notebook
    # Drop unused columns (same as your colstodrop list) [file:1]
    cols_to_drop = [
        "typeCode","freqCode","refPeriodId","partner2Code","partner2ISO","partner2Desc",
        "classificationSearchCode","isOriginalClassification","isLeaf","customsCode",
        "customsDesc","mosCode","motCode","motDesc","qtyUnitCode","qtyUnitAbbr",
        "isQtyEstimated","altQtyUnitCode","altQtyUnitAbbr","isAltQtyEstimated",
        "isNetWgtEstimated","isGrossWgtEstimated","legacyEstimationFlag","isReported",
        "isAggregate","refYear","reporterCode","reporterISO","flowCode","partnerCode",
        "cmdCode","aggrLevel","qty","grossWgt","cifvalue","primaryValue",
        "classificationCode","partnerISO"
    ]
    df.drop(columns=cols_to_drop, inplace=True, errors="ignore")

    # Replace long commodity descriptions with short labels (Rubber, Textiles, etc.) [file:1]
    df["cmdDesc"] = df["cmdDesc"].replace({
        "Retreaded or used pneumatic tyres of rubber solid or cushion tyres, tyre treads and tyre flaps, of rubber": "Rubber",
        "Textiles worn clothing and other worn articles": "Textiles",
        "Residual products of the chemical or allied industries, not elsewhere specified or included; municipal waste; sewage sludge; other residual products.": "Industrial And Municipal Waste",
        "Waste, parings and scrap, of plastics": "Plastic",
        "Waste and scrap of precious metal or of metal clad with precious metal; other waste and scrap containing precious metal compounds, of a kind uses principally for the recovery of precious metal": "Metal"
    })

    # Rename columns to the final schema you used [file:1]
    df.rename(columns={
        "period": "Year",
        "reporterDesc": "Reporter",
        "cmdDesc": "Commodity",
        "flowDesc": "Trade",
        "partnerDesc": "Partner",
        "altQty": "Quantity",
        "netWgt": "Weight",
        "fobvalue": "FobValue"
    }, inplace=True)

    # Drop rows with missing Weight as you did [file:1]
    df = df.dropna(subset=["Weight"])

    return df

df = load_data()

# ===== 3. SIDEBAR FILTERS =====
st.sidebar.header("Global Filters")

years = sorted(df["Year"].unique())
trades = sorted(df["Trade"].unique())
reporters = sorted(df["Reporter"].unique())
partners = sorted(df["Partner"].unique())
commodities = sorted(df["Commodity"].unique())

selected_years = st.sidebar.multiselect("Year", years, default=years)
selected_trade = st.sidebar.multiselect("Trade type", trades, default=trades)
selected_reporter = st.sidebar.multiselect("Reporter", reporters, default=reporters)
selected_partner = st.sidebar.multiselect("Partner", partners, default=partners)
selected_commodity = st.sidebar.multiselect("Commodity", commodities, default=commodities)

filtered = df[
    df["Year"].isin(selected_years)
    & df["Trade"].isin(selected_trade)
    & df["Reporter"].isin(selected_reporter)
    & df["Partner"].isin(selected_partner)
    & df["Commodity"].isin(selected_commodity)
]

st.subheader("Filtered data preview")
st.dataframe(filtered.head())

# ===== 4. VISUALISATIONS =====

# ---- 4.1 Yearly Export Trade Overview (Quantity, Weight, FobValue summed by Year) [file:1]
st.header("1. Yearly Export Trade Overview")

if not filtered.empty:
    yearly = (
        filtered.groupby("Year")[["Quantity", "Weight", "FobValue"]]
        .sum()
        .reset_index()
    )

    # Convert to more readable units (like notebook) [file:1]
    yearly["Weight_kt"] = yearly["Weight"] / 1e6     # kilotons
    yearly["Fob_million"] = yearly["FobValue"] / 1e6 # million USD

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quantity and Weight by Year")
        fig, ax1 = plt.subplots(figsize=(7, 4))
        color1 = "tab:blue"
        ax1.set_xlabel("Year")
        ax1.set_ylabel("Quantity", color=color1)
        ax1.plot(yearly["Year"], yearly["Quantity"], marker="o", color=color1, label="Quantity")
        ax1.tick_params(axis="y", labelcolor=color1)

        ax2 = ax1.twinx()
        color2 = "tab:green"
        ax2.set_ylabel("Weight (kilotons)", color=color2)
        ax2.plot(yearly["Year"], yearly["Weight_kt"], marker="s", color=color2, label="Weight (kt)")
        ax2.tick_params(axis="y", labelcolor=color2)

        fig.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("FOB Value by Year (million USD)")
        fig2, ax3 = plt.subplots(figsize=(7, 4))
        sns.lineplot(
            data=yearly,
            x="Year",
            y="Fob_million",
            marker="o",
            ax=ax3
        )
        ax3.set_ylabel("FobValue (million USD)")
        st.pyplot(fig2)

else:
    st.info("No data for the selected filters.")


# ---- 4.2 FOB Trend Over the Years by Commodity [file:1]
st.header("2. FOB Trend Over the Years by Commodity")

if not filtered.empty:
    # Aggregate by Year and Commodity [file:1]
    yearly_cmd = (
        filtered.groupby(["Year", "Commodity"])[["Quantity", "Weight", "FobValue"]]
        .sum()
        .reset_index()
    )
    yearly_cmd["Fob_million"] = yearly_cmd["FobValue"] / 1e6

    fig3, ax4 = plt.subplots(figsize=(9, 5))
    sns.lineplot(
        data=yearly_cmd,
        x="Year",
        y="Fob_million",
        hue="Commodity",
        marker="o",
        ax=ax4
    )
    ax4.set_ylabel("FobValue (million USD)")
    ax4.set_title("FOB Value Trend by Commodity")
    ax4.legend(title="Commodity")
    st.pyplot(fig3)
else:
    st.info("No data for the selected filters.")


# ---- 4.3 Partner-wise Weight Share per Commodity (Bar/Facet) [built from cleaned schema] [file:1]
st.header("3. Partner-wise Weight by Commodity")

if not filtered.empty:
    commodity_for_bar = st.selectbox("Select commodity for partner breakdown", commodities)
    subset = filtered[filtered["Commodity"] == commodity_for_bar]

    if subset.empty:
        st.info("No rows for this commodity with current filters.")
    else:
        partner_weight = (
            subset.groupby("Partner")["Weight"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        fig4, ax5 = plt.subplots(figsize=(9, 5))
        sns.barplot(
            data=partner_weight,
            x="Weight",
            y="Partner",
            ax=ax5,
            palette="viridis"
        )
        ax5.set_xlabel("Weight")
        ax5.set_ylabel("Partner")
        ax5.set_title(f"Top 15 Partners by Weight – {commodity_for_bar}")
        st.pyplot(fig4)
else:
    st.info("No data for the selected filters.")


# ---- 4.4 Commodity Mix Over Years (Stacked area by Weight) [file:1]
st.header("4. Commodity Mix Over the Years (by Weight)")

if not filtered.empty:
    yearly_commodity = (
        filtered.groupby(["Year", "Commodity"])["Weight"]
        .sum()
        .reset_index()
    )

    # Pivot to wide for area plot
    pivot_ac = yearly_commodity.pivot(index="Year", columns="Commodity", values="Weight").fillna(0)

    fig5, ax6 = plt.subplots(figsize=(9, 5))
    ax6.stackplot(
        pivot_ac.index,
        [pivot_ac[col] for col in pivot_ac.columns],
        labels=pivot_ac.columns
    )
    ax6.set_xlabel("Year")
    ax6.set_ylabel("Weight")
    ax6.set_title("Commodity Weight Mix Over Years")
    ax6.legend(loc="upper left", bbox_to_anchor=(1, 1))
    st.pyplot(fig5)
else:
    st.info("No data for the selected filters.")


# ---- 4.5 Trade Type Distribution (Export vs Import) [file:1]
st.header("5. Trade Type Distribution (Weight)")

if not filtered.empty:
    trade_weight = (
        filtered.groupby("Trade")["Weight"]
        .sum()
        .reset_index()
    )

    col3, col4 = st.columns(2)

    with col3:
        fig6, ax7 = plt.subplots(figsize=(5, 5))
        ax7.pie(
            trade_weight["Weight"],
            labels=trade_weight["Trade"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax7.set_title("Weight Share by Trade Type")
        st.pyplot(fig6)

    with col4:
        fig7, ax8 = plt.subplots(figsize=(5, 5))
        sns.barplot(
            data=trade_weight,
            x="Trade",
            y="Weight",
            ax=ax8
        )
        ax8.set_title("Total Weight by Trade Type")
        st.pyplot(fig7)
else:
    st.info("No data for the selected filters.")


# ---- 4.6 Heatmap: Year vs Commodity by Weight [file:1]
st.header("6. Heatmap – Year vs Commodity (Weight)")

if not filtered.empty:
    heat = (
        filtered.groupby(["Year", "Commodity"])["Weight"]
        .sum()
        .reset_index()
    )
    pivot_hm = heat.pivot(index="Commodity", columns="Year", values="Weight").fillna(0)

    fig8, ax9 = plt.subplots(figsize=(9, 5))
    sns.heatmap(
        pivot_hm,
        cmap="YlGnBu",
        ax=ax9
    )
    ax9.set_title("Weight Heatmap: Commodity vs Year")
    st.pyplot(fig8)
else:
    st.info("No data for the selected filters.")


# In[ ]:




