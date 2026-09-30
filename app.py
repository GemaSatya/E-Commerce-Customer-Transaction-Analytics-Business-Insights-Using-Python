from pathlib import Path

from flask import Flask, render_template, request

import src.analysis as analysis
from src.data_loader import load_excel_data
from src.preprocessing import clean_data, merge_datasets


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "eCommerceData.xlsx"

app = Flask(__name__)


def load_dashboard_data():
    """Load and prepare the dataset once when the application starts."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")
    return clean_data(merge_datasets(load_excel_data(str(DATASET_PATH))))


df = load_dashboard_data()


def _chart_points(series, width=620, height=230, padding=34):
    """Convert a pandas series into SVG-friendly coordinates."""
    values = series.astype(float).tolist()
    maximum = max(values) if values else 1
    minimum = min(values) if values else 0
    span = maximum - minimum or 1
    usable_width = width - (padding * 2)
    usable_height = height - (padding * 2)
    points = []
    for index, value in enumerate(values):
        x = padding if len(values) == 1 else padding + (
            index / (len(values) - 1)
        ) * usable_width
        y = height - padding - ((value - minimum) / span) * usable_height
        points.append({"x": round(x, 1), "y": round(y, 1), "value": int(value)})
    return points


def dashboard_context(city=None):
    filtered = df if not city else df[df["city_name"] == city]
    kpi = analysis.calculate_kpi(filtered)
    cities = analysis.city_performance(filtered).head(6)
    merchants = analysis.top_merchant_transaction(filtered, limit=6)
    customers = analysis.top_customer_transaction(filtered, limit=6)
    monthly = analysis.monthly_transaction(filtered)
    gender = analysis.gender_transaction(filtered)
    coupon = analysis.coupon_burn_rate(filtered)

    return {
        "kpi": kpi,
        "cities": [
            {"name": name, "transactions": int(row["total_transaction"]),
             "customers": int(row["unique_customer"])}
            for name, row in cities.iterrows()
        ],
        "merchants": [{"name": name, "value": int(value)}
                      for name, value in merchants.items()],
        "customers": [{"name": str(name), "value": int(value)}
                      for name, value in customers.items()],
        "monthly_labels": [str(label) for label in monthly.index],
        "monthly_points": _chart_points(monthly),
        "gender": [{"name": str(name), "value": int(value)}
                   for name, value in gender.items()],
        "coupon": coupon,
        "selected_city": city or "All cities",
        "city_options": sorted(df["city_name"].dropna().unique().tolist()),
        "has_data": not filtered.empty,
    }

@app.get("/")
def dashboard():
    return render_template("dashboard.html", **dashboard_context())


@app.get("/dashboard")
def dashboard_partial():
    city = request.args.get("city") or None
    return render_template("dashboard_content.html", **dashboard_context(city))


if __name__ == "__main__":
    app.run(debug=True)
