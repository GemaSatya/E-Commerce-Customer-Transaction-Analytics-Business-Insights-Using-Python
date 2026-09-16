"""
==========================================================
VISUALIZATION MODULE
==========================================================

Purpose:
    Generate business visualization
    from analytical results.

Visualization:
    - Customer ranking
    - City performance
    - Merchant performance
    - Monthly trend
    - Customer distribution
    - Gender distribution


Author:
    Gema Satya
==========================================================
"""

import os

import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# SET OUTPUT DIRECTORY
# ==========================================================

OUTPUT_DIR = "reports/images"

def create_output_folder():
    """
    Create visualization output folder.
    """

    if not os.path.exists(OUTPUT_DIR):

        os.makedirs(
            OUTPUT_DIR
        )

# ==========================================================
# CUSTOMER VISUALIZATION
# ==========================================================

def plot_top_customer(
        customer_data,
        limit=10
):

    """
    Plot top customers by transaction.
    """

    create_output_folder()

    plt.figure(
        figsize=(10,5)
    )

    sns.barplot(
        x=customer_data.values,
        y=customer_data.index
    )

    plt.title(
        "Top Customer Based on Transaction"
    )

    plt.xlabel(
        "Number of Transaction"
    )

    plt.ylabel(
        "Customer ID"
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/top_customer.png",
        dpi=300
    )

    plt.close()

# ==========================================================
# CITY VISUALIZATION
# ==========================================================

def plot_top_city(
        city_data
):

    """
    Plot top cities by transaction.
    """

    create_output_folder()

    plt.figure(
        figsize=(8,5)
    )

    sns.barplot(
        x=city_data.values,
        y=city_data.index
    )

    plt.title(
        "Top City Based on Transaction"
    )

    plt.xlabel(
        "Transaction"
    )

    plt.ylabel(
        "City"
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/top_city.png",
        dpi=300
    )

    plt.close()

# ==========================================================
# MERCHANT VISUALIZATION
# ==========================================================

def plot_top_merchant(
        merchant_data
):

    """
    Plot merchant ranking.
    """

    create_output_folder()

    plt.figure(
        figsize=(8,5)
    )

    sns.barplot(
        x=merchant_data.values,
        y=merchant_data.index
    )

    plt.title(
        "Top Merchant Based on Transaction"
    )

    plt.xlabel(
        "Transaction"
    )

    plt.ylabel(
        "Merchant"
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/top_merchant.png",
        dpi=300
    )

    plt.close()

# ==========================================================
# TIME TREND VISUALIZATION
# ==========================================================

def plot_monthly_transaction(
        monthly_data
):

    """
    Plot monthly transaction trend.
    """
    
    create_output_folder()

    plt.figure(
        figsize=(12,5)
    )

    sns.lineplot(
        x=monthly_data.index,
        y=monthly_data.values,
        marker="o"
    )

    plt.xticks(
        rotation=45
    )

    plt.title(
        "Monthly Transaction Trend"
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Transaction"
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/monthly_transaction.png",
        dpi=300
    )

    plt.close()

# ==========================================================
# CUSTOMER CITY VISUALIZATION
# ==========================================================

def plot_customer_city(
        city_customer
):

    """
    Plot unique customer distribution by city.
    """

    create_output_folder()

    plt.figure(
        figsize=(10,6)
    )

    sns.barplot(
        x=city_customer.values,
        y=city_customer.index
    )

    plt.title(
        "Unique Customer By City"
    )

    plt.xlabel(
        "Customer"
    )

    plt.ylabel(
        "City"
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/customer_city.png",
        dpi=300
    )

    plt.close()

# ==========================================================
# GENDER VISUALIZATION
# ==========================================================

def plot_gender_transaction(
        gender_data
):

    """
    Plot transaction distribution by gender.
    """

    create_output_folder()

    plt.figure(
        figsize=(6,5)
    )

    sns.barplot(
        x=gender_data.index,
        y=gender_data.values
    )

    plt.title(
        "Transaction Distribution By Gender"
    )

    plt.xlabel(
        "Gender"
    )

    plt.ylabel(
        "Transaction"
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/gender_transaction.png",
        dpi=300
    )

    plt.close()

# ==========================================================
# COMPLETE REPORT GENERATOR
# ==========================================================

def generate_all_visualization(df, analysis):

    """
    Generate all charts automatically.

    Parameters
    ----------
    df :
        Clean dataframe


    analysis :
        imported analysis module

    """

    print(
        "\nGenerating visualization..."
    )

    plot_top_customer(
        analysis.top_customer_transaction(df)
    )

    plot_top_city(
        analysis.top_city_transaction(df)
    )

    plot_top_merchant(
        analysis.top_merchant_transaction(df)
    )

    plot_monthly_transaction(
        analysis.monthly_transaction(df)
    )

    gender = (
        analysis.gender_transaction(df)
    )

    plot_gender_transaction(
        gender
    )

    print(
        "Visualization completed"
    )