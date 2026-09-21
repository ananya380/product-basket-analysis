import pandas as pd
import os
from itertools import combinations
from collections import Counter

# ============================================================
# PRODUCT BASKET ANALYSIS - TASK 29
# ============================================================

file_path = r"C:\task_29\data\online_retail_II.csv"
reports_path = r"C:\task_29\reports"

os.makedirs(reports_path, exist_ok=True)

print("=" * 60)
print("PRODUCT BASKET ANALYSIS - TASK 29")
print("=" * 60)

# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(file_path)

print("\nOriginal Dataset Shape:")
print(df.shape)

# ============================================================
# 2. CLEAN DATA
# ============================================================

df = df.dropna(subset=["Description"])

df["Invoice"] = df["Invoice"].astype(str)

cancelled_count = df["Invoice"].str.startswith("C").sum()

df = df[~df["Invoice"].str.startswith("C")]

df = df[df["Quantity"] > 0]

df["Description"] = (
    df["Description"]
    .astype(str)
    .str.strip()
)

df = df[df["Description"] != ""]

print("\nAfter Cleaning:")
print(df.shape)

print("\nCancelled Invoice Rows Removed:")
print(cancelled_count)

# ============================================================
# 3. CREATE BASKET DATA
# ============================================================

basket_data = (
    df[["Invoice", "Description"]]
    .drop_duplicates()
)

total_orders = basket_data["Invoice"].nunique()
total_products = basket_data["Description"].nunique()

avg_products = (
    basket_data.groupby("Invoice")["Description"]
    .nunique()
    .mean()
)

print("\n" + "=" * 60)
print("BASKET STATISTICS")
print("=" * 60)

print(f"Total Orders: {total_orders:,}")
print(f"Unique Products: {total_products:,}")
print(f"Average Products per Order: {avg_products:.2f}")

# Save cleaned data
cleaned_path = os.path.join(
    reports_path,
    "cleaned_basket_data.csv"
)

basket_data.to_csv(cleaned_path, index=False)

print("\nCleaned basket data saved to:")
print(cleaned_path)

# ============================================================
# 4. GENERATE PRODUCT PAIRS
# ============================================================

print("\n" + "=" * 60)
print("GENERATING PRODUCT PAIRS")
print("=" * 60)

basket_groups = basket_data.groupby("Invoice")["Description"]

pair_counter = Counter()

for invoice, products in basket_groups:

    product_list = sorted(set(products))

    if len(product_list) < 2:
        continue

    pairs = combinations(product_list, 2)

    pair_counter.update(pairs)

print(f"\nTotal Unique Product Pairs: {len(pair_counter):,}")

# ============================================================
# 5. CREATE PAIR DATAFRAME
# ============================================================

pair_data = []

for (product_1, product_2), frequency in pair_counter.items():

    pair_data.append({
        "Product_1": product_1,
        "Product_2": product_2,
        "Frequency": frequency
    })

pairs_df = pd.DataFrame(pair_data)

pairs_df = pairs_df.sort_values(
    by="Frequency",
    ascending=False
).reset_index(drop=True)

# ============================================================
# 6. CALCULATE SUPPORT
# ============================================================

pairs_df["Support"] = (
    pairs_df["Frequency"] /
    total_orders *
    100
)

# ============================================================
# 7. TOP 20 PRODUCT PAIRS
# ============================================================

top_20 = pairs_df.head(20).copy()

print("\n" + "=" * 60)
print("TOP 20 PRODUCT PAIRS")
print("=" * 60)

print(
    top_20[
        [
            "Product_1",
            "Product_2",
            "Frequency",
            "Support"
        ]
    ].to_string(index=False)
)

# Save all pairs
all_pairs_path = os.path.join(
    reports_path,
    "all_product_pairs.csv"
)

pairs_df.to_csv(
    all_pairs_path,
    index=False
)

# Save top 20
top_pairs_path = os.path.join(
    reports_path,
    "top_20_product_pairs.csv"
)

top_20.to_csv(
    top_pairs_path,
    index=False
)

# ============================================================
# 8. PRODUCT RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 60)
print("PRODUCT RECOMMENDATION ANALYSIS")
print("=" * 60)

recommendations = []

for _, row in top_20.iterrows():

    recommendations.append({
        "Product": row["Product_1"],
        "Recommended_Product": row["Product_2"],
        "Frequency": row["Frequency"],
        "Support": round(row["Support"], 2),
        "Recommendation":
            f"Customers purchasing "
            f"'{row['Product_1']}' can be recommended "
            f"'{row['Product_2']}'."
    })

recommendations_df = pd.DataFrame(
    recommendations
)

print(
    recommendations_df[
        [
            "Product",
            "Recommended_Product",
            "Frequency",
            "Support"
        ]
    ].to_string(index=False)
)

recommendation_path = os.path.join(
    reports_path,
    "product_recommendations.csv"
)

recommendations_df.to_csv(
    recommendation_path,
    index=False
)

# ============================================================
# 9. STRONGEST PRODUCT ASSOCIATION
# ============================================================

strongest_pair = pairs_df.iloc[0]

print("\n" + "=" * 60)
print("STRONGEST PRODUCT ASSOCIATION")
print("=" * 60)

print(
    f"Product 1 : {strongest_pair['Product_1']}"
)

print(
    f"Product 2 : {strongest_pair['Product_2']}"
)

print(
    f"Frequency : {strongest_pair['Frequency']:,}"
)

print(
    f"Support   : {strongest_pair['Support']:.2f}%"
)

# ============================================================
# 10. TOP 10 SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 PRODUCT PAIRS SUMMARY")
print("=" * 60)

for index, row in pairs_df.head(10).iterrows():

    print(
        f"{index + 1}. "
        f"{row['Product_1']} + "
        f"{row['Product_2']} | "
        f"Frequency: {row['Frequency']:,} | "
        f"Support: {row['Support']:.2f}%"
    )

print("\n" + "=" * 60)
print("TASK 29 ANALYSIS COMPLETED")
print("=" * 60)

print("\nFiles created:")
print(all_pairs_path)
print(top_pairs_path)
print(recommendation_path)

# ============================================================
# 11. VISUALIZATIONS
# ============================================================

import matplotlib.pyplot as plt
import textwrap

visuals_path = r"C:\task_29\visuals"
os.makedirs(visuals_path, exist_ok=True)

# ------------------------------------------------------------
# VISUAL 1: TOP 10 PRODUCT PAIRS BY FREQUENCY
# ------------------------------------------------------------

top10 = pairs_df.head(10).copy()

top10["Pair"] = (
    top10["Product_1"] +
    " + " +
    top10["Product_2"]
)

# Wrap long product names
top10["Pair"] = top10["Pair"].apply(
    lambda x: "\n".join(textwrap.wrap(x, width=45))
)

plt.figure(figsize=(12, 8))

plt.barh(
    top10["Pair"][::-1],
    top10["Frequency"][::-1]
)

plt.xlabel("Number of Orders")
plt.ylabel("Product Pair")

plt.title(
    "Top 10 Product Pairs by Purchase Frequency"
)

plt.tight_layout()

frequency_chart = os.path.join(
    visuals_path,
    "top_10_product_pairs_frequency.png"
)

plt.savefig(
    frequency_chart,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nFrequency chart saved to:")
print(frequency_chart)

# ------------------------------------------------------------
# VISUAL 2: TOP 10 PRODUCT PAIRS BY SUPPORT
# ------------------------------------------------------------

top_support = pairs_df.sort_values(
    by="Support",
    ascending=False
).head(10).copy()

top_support["Pair"] = (
    top_support["Product_1"] +
    " + " +
    top_support["Product_2"]
)

top_support["Pair"] = top_support["Pair"].apply(
    lambda x: "\n".join(textwrap.wrap(x, width=45))
)

plt.figure(figsize=(12, 8))

plt.barh(
    top_support["Pair"][::-1],
    top_support["Support"][::-1]
)

plt.xlabel("Support (%)")
plt.ylabel("Product Pair")

plt.title(
    "Top 10 Product Pairs by Support"
)

plt.tight_layout()

support_chart = os.path.join(
    visuals_path,
    "top_10_product_pairs_support.png"
)

plt.savefig(
    support_chart,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nSupport chart saved to:")
print(support_chart)

# ------------------------------------------------------------
# VISUAL 3: MOST FREQUENTLY ASSOCIATED PRODUCTS
# ------------------------------------------------------------

product_frequency = Counter()

for _, row in pairs_df.head(100).iterrows():

    product_frequency[row["Product_1"]] += row["Frequency"]
    product_frequency[row["Product_2"]] += row["Frequency"]

top_products = (
    pd.DataFrame(
        product_frequency.items(),
        columns=["Product", "Association_Frequency"]
    )
    .sort_values(
        by="Association_Frequency",
        ascending=False
    )
    .head(10)
)

top_products["Product"] = top_products["Product"].apply(
    lambda x: "\n".join(textwrap.wrap(x, width=30))
)

plt.figure(figsize=(12, 8))

plt.barh(
    top_products["Product"][::-1],
    top_products["Association_Frequency"][::-1]
)

plt.xlabel("Combined Pair Frequency")
plt.ylabel("Product")

plt.title(
    "Top Products in Frequently Purchased Pairs"
)

plt.tight_layout()

product_chart = os.path.join(
    visuals_path,
    "top_associated_products.png"
)

plt.savefig(
    product_chart,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nProduct association chart saved to:")
print(product_chart)

# ============================================================
# VISUALIZATION COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("ALL VISUALIZATIONS CREATED")
print("=" * 60)

print(f"\nVisuals folder:")
print(visuals_path)