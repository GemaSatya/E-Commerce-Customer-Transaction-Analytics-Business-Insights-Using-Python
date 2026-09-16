"""
==========================================================
DATA LOADER MODULE
==========================================================

Purpose:
    Handle loading raw e-commerce dataset from Excel file.

Dataset:
    eCommerceData.xlsx

Sheets:
    - customers
    - transactions
    - cities
    - genders
    - branches
    - merchants

Author:
    Gema Satya
==========================================================
"""

import pandas as pd
import os

def load_excel_data(file_path):
    """
    Load all sheets from e-commerce Excel dataset.

    Parameters
    ----------
    file_path : str
        Path to Excel dataset.

    Returns
    -------
    dict
        Dictionary containing all dataframe tables.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset tidak ditemukan: {file_path}"
        )

    print("Loading dataset...")

    customers = pd.read_excel(
        file_path,
        sheet_name="customers"
    )
    
    transactions = pd.read_excel(
        file_path,
        sheet_name="transactions"
    )

    cities = pd.read_excel(
        file_path,
        sheet_name="cities"
    )

    genders = pd.read_excel(
        file_path,
        sheet_name="genders"
    )

    branches = pd.read_excel(
        file_path,
        sheet_name="branches"
    )

    merchants = pd.read_excel(
        file_path,
        sheet_name="merchants"
    )

    print("Dataset berhasil dimuat")

    return {
        "customers": customers,

        "transactions": transactions,

        "cities": cities,

        "genders": genders,

        "branches": branches,

        "merchants": merchants
    }

def dataset_summary(data):
    """
    Display basic information
    from every dataframe.

    Parameters
    ----------
    data : dict
        Dictionary of dataframe.
    """

    print("\n========== DATASET SUMMARY ==========")

    for name, df in data.items():

        print(
            f"\n{name.upper()}"
        )

        print(
            "Rows :",
            df.shape[0]
        )

        print(
            "Columns :",
            df.shape[1]
        )

        print(
            df.head(3)
        )
