"""
==========================================================
BUSINESS ANALYSIS MODULE
==========================================================

Purpose:
    Perform business analysis on processed
    e-commerce transaction dataset.

Analysis:
    - Customer performance
    - City performance
    - Merchant performance
    - Customer activity
    - Gender behavior
    - Coupon burn rate
    - Business KPI

Input:
    Clean dataframe from preprocessing.py

Output:
    Analytical tables and metrics


Author:
    Gema Satya
==========================================================
"""
import pandas as pd

# ==========================================================
# KPI OVERVIEW
# ==========================================================


def calculate_kpi(df):
    """
    Calculate overall business KPI.

    Returns
    -------
    dict
        KPI metrics
    """

    kpi = {

        "total_transaction":
            df["transaction_id"].nunique(),


        "total_customer":
            df["customer_id"].nunique(),


        "total_city":
            df["city_name"].nunique(),


        "total_merchant":
            df["merchant_name"].nunique()

    }

    return kpi

# ==========================================================
# CUSTOMER ANALYSIS
# ==========================================================

def top_customer_transaction(df, limit=10):
    """
    Find customers with highest transaction frequency.
    """

    result = (
        df.groupby("customer_id")
        .size()
        .sort_values(
            ascending=False
        )
        .head(limit)
    )

    return result

def customer_activity(df):
    """
    Analyze customer transaction activity.

    Returns:
        customer level summary
    """

    result = (
        df.groupby("customer_id")
        .agg(

            total_transaction=
            (
                "transaction_id",
                "count"
            ),

            city=
            (
                "city_name",
                "first"
            ),

            gender=
            (
                "gender_name",
                "first"
            )

        )
    )

    return (
        result
        .sort_values(
            "total_transaction",
            ascending=False
        )
    )

# ==========================================================
# CITY ANALYSIS
# ==========================================================

def city_performance(df):
    """
    Analyze transaction performance by city.
    """
    result = (
        df.groupby("city_name")
        .agg(

            total_transaction=
            (
                "transaction_id",
                "count"
            ),


            unique_customer=
            (
                "customer_id",
                "nunique"
            ),


            avg_transaction_per_customer=
            (
                "customer_id",
                lambda x:
                len(x) / x.nunique()
            )

        )
        .sort_values(
            "total_transaction",
            ascending=False
        )
    )

    return result

def top_city_transaction(df, limit=5):
    """
    Top cities based on transaction volume.
    """

    result = (
        df.groupby("city_name")
        .size()
        .sort_values(
            ascending=False
        )
        .head(limit)
    )

    return result

def dominant_city(df):
    """
    Return city with highest transaction.
    """

    city = (
        city_performance(df)
        .index[0]
    )

    return city

# ==========================================================
# MERCHANT ANALYSIS
# ==========================================================

def top_merchant_transaction(df, limit=5):
    """
    Find merchants with highest transaction.
    """


    result = (
        df.groupby("merchant_name")
        .size()
        .sort_values(
            ascending=False
        )
        .head(limit)
    )


    return result

def merchant_performance(df):
    """
    Analyze merchant transaction performance.
    """

    result = (
        df.groupby("merchant_name")
        .agg(

            total_transaction=
            (
                "transaction_id",
                "count"
            ),


            unique_customer=
            (
                "customer_id",
                "nunique"
            )

        )
        .sort_values(
            "total_transaction",
            ascending=False
        )
    )

    result["market_share"] = (
        result["total_transaction"]
        /
        len(df)
        *
        100
    )

    return result

def merchant_by_city(df):
    """
    Find dominant merchant in every city.
    """

    result = (
        df.groupby(
            [
                "city_name",
                "merchant_name"
            ]
        )
        .size()
        .reset_index(
            name="transaction"
        )
    )

    result = result.sort_values(
        [
            "city_name",
            "transaction"
        ],
        ascending=[
            True,
            False
        ]
    )

    return result

# ==========================================================
# TIME ANALYSIS
# ==========================================================

def monthly_transaction(df):
    """
    Calculate monthly transaction trend.
    """

    result = (
        df.groupby("month")
        .size()
    )

    return result

def city_monthly_transaction(
        df,
        city
):
    """
    Monthly transaction trend
    for selected city.
    """

    result = (
        df[
            df["city_name"] == city
        ]
        .groupby("month")
        .size()
    )

    return result

# ==========================================================
# CUSTOMER DEMOGRAPHIC
# ==========================================================
def gender_transaction(df):
    """
    Transaction distribution by gender.
    """

    result = (
        df.groupby("gender_name")
        .size()
        .sort_values(
            ascending=False
        )
    )

    return result

def city_gender(df, city):
    """
    Gender distribution
    in specific city.
    """
    result = (
        df[
            df["city_name"] == city
        ]
        .groupby("gender_name")
        .size()
    )

    return result

# ==========================================================
# PROMOTION ANALYSIS
# ==========================================================
def coupon_burn_rate(df):
    """
    Calculate coupon utilization.

    Formula:
    coupon used / coupon issued * 100
    """

    total_coupon = (
        df["coupon_name"]
        .notna()
        .sum()
    )

    burn_coupon = (
        df["burn_date"]
        .notna()
        .sum()
    )

    if total_coupon == 0:
        rate = 0

    else:
        rate = (
            burn_coupon
            /
            total_coupon
            *
            100
        )

    return {
        "total_coupon":
            total_coupon,

        "coupon_used":
            burn_coupon,

        "burn_rate":
            round(rate,2)
    }

# ==========================================================
# AUTOMATIC BUSINESS SUMMARY
# ==========================================================

def generate_summary(df):

    """
    Generate high level business insight.
    """

    city = city_performance(df)

    merchant = merchant_performance(df)

    summary = {
        "highest_transaction_city":
            city.index[0],

        "highest_city_transaction":
            city.iloc[0]
            ["total_transaction"],

        "highest_city_customer":
            city.iloc[0]
            ["unique_customer"],

        "main_merchant":
            merchant.index[0],

        "burn_rate":
            coupon_burn_rate(df)
            ["burn_rate"]

    }

    return summary