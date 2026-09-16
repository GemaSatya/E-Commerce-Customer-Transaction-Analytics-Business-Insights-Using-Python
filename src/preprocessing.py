"""
==========================================================
DATA PREPROCESSING MODULE
==========================================================

Purpose:
    Prepare raw e-commerce datasets for analysis.

Process:
    1. Merge transaction data with dimension tables
    2. Handle missing values
    3. Convert data types
    4. Create additional features

Input:
    Raw dataframe from data_loader.py

Output:
    Clean analytical dataframe


Author:
    Gema Satya
==========================================================
"""

import pandas as pd

def merge_datasets(data):
    """
    Merge all e-commerce tables into one analytical dataframe.

    Parameters
    ----------
    data : dict
        Dictionary containing dataframe tables.

    Returns
    -------
    pandas.DataFrame
        Combined transaction dataset.
    """

    print("\nStarting data merging...")

    transactions = data["transactions"]

    customers = data["customers"]

    cities = data["cities"]

    genders = data["genders"]

    branches = data["branches"]

    merchants = data["merchants"]

    # Merge customer information
    df = transactions.merge(
        customers,
        on="customer_id",
        how="left"
    )

    # Merge city information
    df = df.merge(
        cities,
        on="city_id",
        how="left"
    )

    # Merge gender information
    df = df.merge(
        genders,
        on="gender_id",
        how="left"
    )

    # Merge branch information
    df = df.merge(
        branches,
        on="branch_id",
        how="left"
    )

    # Merge merchant information
    df = df.merge(
        merchants,
        on="merchant_id",
        how="left"
    )

    print(
        "Data merging completed"
    )
    
    return df

def clean_data(df):
    """
    Clean analytical dataset.

    Cleaning process:
    - Remove duplicate rows
    - Handle missing values
    - Convert date column

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
        Clean dataframe
    """

    print("\nStarting data cleaning...")

    # Copy dataframe
    df = df.copy()

    # Remove duplicate transaction
    duplicate_count = df.duplicated().sum()

    df = df.drop_duplicates()

    print(
        f"Removed duplicates: {duplicate_count}"
    )

    # Convert transaction date

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    # Remove invalid dates
    invalid_date = df["transaction_date"].isna().sum()

    if invalid_date > 0:

        df = df.dropna(
            subset=[
                "transaction_date"
            ]
        )

        print(
            f"Removed invalid dates: {invalid_date}"
        )

    # Create month feature
    df["month"] = (
        df["transaction_date"]
        .dt
        .to_period("M")
        .astype(str)
    )

    print(
        "Data cleaning completed"
    )

    return df

def check_missing_value(df):
    """
    Display missing value summary.

    Parameters
    ----------
    df : pandas.DataFrame

    """
    print(
        "\n========== Missing Value =========="
    )

    missing = (
        df.isnull()
        .sum()
        .sort_values(
            ascending=False
        )
    )

    print(
        missing[missing > 0]
    )

def dataset_information(df):
    """
    Display final dataset information.

    Parameters
    ----------
    df : pandas.DataFrame
    """

    print(
        "\n========== FINAL DATASET =========="
    )

    print(
        "Rows:",
        df.shape[0]
    )

    print(
        "Columns:",
        df.shape[1]
    )

    print(
        "\nColumn List:"
    )

    print(
        df.columns.tolist()
    )

    print(
        "\nPreview:"
    )

    print(
        df.head()
    )