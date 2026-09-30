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


# ==========================================================
# BRANCH ANALYSIS
# ==========================================================


def branch_performance(df):
    """
    Analyze transaction performance by branch.
    """

    result = (
        df.groupby("branch_name")
        .agg(
            total_transaction=("transaction_id", "count"),
            unique_customer=("customer_id", "nunique"),
            unique_merchant=("merchant_name", "nunique"),
        )
        .sort_values("total_transaction", ascending=False)
    )

    result["avg_transaction_per_customer"] = (
        result["total_transaction"] / result["unique_customer"]
    ).round(2)

    return result


def top_branch_transaction(df, limit=5):
    """
    Find branches with highest transaction volume.
    """

    result = (
        df.groupby("branch_name")
        .size()
        .sort_values(ascending=False)
        .head(limit)
    )

    return result


# ==========================================================
# COUPON DEEP DIVE
# ==========================================================


def coupon_breakdown(df):
    """
    Break down coupon usage by coupon name.
    """

    coupon_df = df[df["coupon_name"].notna()].copy()

    if coupon_df.empty:
        return pd.DataFrame(
            columns=["coupon_name", "issued", "redeemed", "burn_rate"]
        )

    result = (
        coupon_df.groupby("coupon_name")
        .agg(
            issued=("transaction_id", "count"),
            redeemed=("burn_date", lambda x: x.notna().sum()),
        )
        .sort_values("issued", ascending=False)
    )

    result["burn_rate"] = (result["redeemed"] / result["issued"] * 100).round(1)

    return result


def coupon_trend(df):
    """
    Monthly coupon issuance and redemption trend.
    """

    coupon_df = df[df["coupon_name"].notna()].copy()

    if coupon_df.empty:
        return pd.DataFrame(columns=["issued", "redeemed"])

    result = (
        coupon_df.groupby("month")
        .agg(
            issued=("transaction_id", "count"),
            redeemed=("burn_date", lambda x: x.notna().sum()),
        )
        .sort_index()
    )

    return result


# ==========================================================
# CUSTOMER SEGMENTATION
# ==========================================================


def customer_segments(df):
    """
    Segment customers by transaction frequency.
    """

    customer_txns = df.groupby("customer_id").size()

    segments = {
        "one_time": int((customer_txns == 1).sum()),
        "occasional": int(((customer_txns >= 2) & (customer_txns <= 5)).sum()),
        "regular": int(((customer_txns >= 6) & (customer_txns <= 15)).sum()),
        "loyal": int((customer_txns > 15).sum()),
    }

    total = sum(segments.values()) or 1
    segments_pct = {k: round(v / total * 100, 1) for k, v in segments.items()}

    return {"counts": segments, "percentages": segments_pct}


def avg_transactions_per_customer(df):
    """
    Calculate average transactions per customer.
    """

    total_txns = len(df)
    unique_customers = df["customer_id"].nunique()

    return round(total_txns / unique_customers, 2) if unique_customers else 0


# ==========================================================
# TEMPORAL PATTERNS
# ==========================================================


def day_of_week_pattern(df):
    """
    Transaction distribution by day of week.
    """

    df_copy = df.copy()
    df_copy["day_of_week"] = df_copy["transaction_date"].dt.day_name()

    result = (
        df_copy.groupby("day_of_week")
        .size()
        .reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
        .fillna(0)
        .astype(int)
    )

    return result


def weekly_trend(df):
    """
    Weekly transaction trend.
    """

    df_copy = df.copy()
    df_copy["week"] = df_copy["transaction_date"].dt.to_period("W").astype(str)

    result = df_copy.groupby("week").size().sort_index()

    return result


def transaction_velocity(df):
    """
    Average transactions per day.
    """

    date_range = (
        df["transaction_date"].max() - df["transaction_date"].min()
    ).days

    return round(len(df) / date_range, 2) if date_range > 0 else 0


# ==========================================================
# MERCHANT DEEP DIVE
# ==========================================================


def merchant_market_share(df, limit=10):
    """
    Calculate market share for top merchants.
    """

    result = (
        df.groupby("merchant_name")
        .size()
        .sort_values(ascending=False)
        .head(limit)
    )

    total = len(df)
    share = (result / total * 100).round(1)

    return share


def merchant_city_dominance(df):
    """
    Find dominant merchant per city with transaction count.
    """

    result = (
        df.groupby(["city_name", "merchant_name"])
        .size()
        .reset_index(name="transactions")
    )

    result = result.sort_values(
        ["city_name", "transactions"], ascending=[True, False]
    )

    idx = result.groupby("city_name")["transactions"].idxmax()
    dominant = result.loc[idx].sort_values("transactions", ascending=False)

    return dominant