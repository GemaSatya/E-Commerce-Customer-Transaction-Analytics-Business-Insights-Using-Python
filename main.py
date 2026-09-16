from src.data_loader import (
    load_excel_data,
    dataset_summary
)
from src.preprocessing import (
    merge_datasets,
    clean_data,
    check_missing_value,
    dataset_information
)
from src.analysis import *
import src.analysis as analysis
from src.visualization import generate_all_visualization


# Load dataset
file = "eCommerceData.xlsx"
data = load_excel_data(file)
dataset_summary(data)

# Preprocessing
# Merge semua tabel
df = merge_datasets(
    data
)

# Cleaning
df = clean_data(
    df
)

# Check kualitas data
check_missing_value(
    df
)

dataset_information(
    df
)

# Analisis Bisnis
# KPI
print(
    calculate_kpi(df)
)

# Customer
print(
    top_customer_transaction(df)
)

# City
print(
    city_performance(df)
)

# Merchant
print(
    merchant_performance(df)
)

# Coupon
print(
    coupon_burn_rate(df)
)

# Summary
print(
    generate_summary(df)
)

# Visualization
generate_all_visualization(
    df,
    analysis
)