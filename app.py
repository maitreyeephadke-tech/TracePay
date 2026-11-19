import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "tracepay_icon.png"
SAMPLE_PATH = BASE_DIR / "sample_data" / "sample_transactions.csv"

st.set_page_config(
    page_title="TracePay",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "₹",
    layout="wide"
)

# =====================================================
# DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #101512;
    color: #E8F0EA;
}

[data-testid="stSidebar"] {
    background-color: #18211B;
    border-right: 1px solid #29392E;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #E8F0EA !important;
}

div[data-testid="stMetric"] {
    background-color: #18211B;
    border: 1px solid #29392E;
    padding: 18px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"] {
    color: #A6B8AA !important;
}

div[data-testid="stMetricValue"] {
    color: #B9E8C8 !important;
}

.stButton > button {
    border-radius: 10px;
}

hr {
    border-color: #29392E;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR BRANDING
# =====================================================

def show_sidebar_brand():

    with st.sidebar:

        if LOGO_PATH.exists():
            st.image(LOGO_PATH, width=75)

        st.markdown("## TracePay")

        st.caption("Every rupee. Better understood.")

        st.caption("TRANSACTION INTELLIGENCE")

        st.divider()


# =====================================================
# SAMPLE DATA
# =====================================================

def get_sample_data():

    if SAMPLE_PATH.exists():
        return pd.read_csv(SAMPLE_PATH)

    sample = {
        "Date": [
            "2026-11-01", "2026-11-01", "2026-11-02",
            "2026-11-02", "2026-11-03", "2026-11-04",
            "2026-11-05", "2026-11-06", "2026-11-07",
            "2026-11-08", "2026-11-09", "2026-11-10",
            "2026-11-11", "2026-11-12", "2026-11-13",
            "2026-11-14", "2026-11-15", "2026-11-16",
            "2026-11-17", "2026-11-18", "2026-11-19"
        ],

        "Description": [
            "Swiggy", "Uber", "Amazon", "Salary", "Netflix",
            "Electricity Bill", "DMart", "Spotify", "Pharmacy",
            "Flipkart", "Swiggy", "Internet Bill", "Salary",
            "Uber", "Amazon", "Movie Tickets", "Electricity Bill",
            "Uber", "Spotify", "Amazon", "Salary"
        ],

        "Amount": [
            450, 280, 1299, 25000, 649, 1800, 2200, 119,
            450, 1599, 680, 999, 25000, 250, 899, 750,
            1800, 280, 119, 1299, 25000
        ],

        "Type": [
            "Debit", "Debit", "Debit", "Credit", "Debit",
            "Debit", "Debit", "Debit", "Debit", "Debit",
            "Debit", "Debit", "Credit", "Debit", "Debit",
            "Debit", "Debit", "Debit", "Debit", "Debit", "Credit"
        ]
    }

    return pd.DataFrame(sample)


# =====================================================
# CLEAN TRANSACTION DATA
# =====================================================

def clean_data(df):

    df = df.copy()

    required_columns = ["Date", "Description", "Amount", "Type"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing columns: " + ", ".join(missing_columns)
        )

    df = df[required_columns]

    df["Date"] = pd.to_datetime(
        df["Date"], errors="coerce"
    )

    df["Description"] = (
        df["Description"]
        .astype(str)
        .str.strip()
    )

    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    )

    df["Type"] = (
        df["Type"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df = df.dropna(
        subset=["Date", "Description", "Amount"]
    )

    df = df[df["Description"] != ""]

    df = df[df["Type"].isin(["Debit", "Credit"])]

    df["Amount"] = df["Amount"].abs()

    df = df.sort_values(
        "Date", ascending=False
    )

    return df.reset_index(drop=True)


# =====================================================
# CATEGORIZATION
# =====================================================

def categorize_transaction(description, transaction_type):

    name = str(description).lower()

    if transaction_type == "Credit":
        return "Income"

    category_rules = {

        "Food": [
            "swiggy", "zomato", "restaurant", "cafe",
            "food", "pizza", "coffee", "dominos", "burger"
        ],

        "Shopping": [
            "amazon", "flipkart", "dmart", "shopping",
            "myntra", "mall", "store", "retail"
        ],

        "Transport": [
            "uber", "ola", "cab", "taxi", "metro",
            "bus", "fuel", "petrol", "train", "travel"
        ],

        "Subscriptions": [
            "netflix", "spotify", "prime", "subscription",
            "youtube premium", "hotstar"
        ],

        "Bills": [
            "electricity", "internet", "water bill",
            "phone bill", "gas bill", "utility"
        ],

        "Healthcare": [
            "pharmacy", "hospital", "doctor", "medicine",
            "medical", "clinic"
        ]
    }

    for category, keywords in category_rules.items():

        if any(keyword in name for keyword in keywords):
            return category

    return "Other"


def add_categories(df):

    df = df.copy()

    df["Category"] = df.apply(
        lambda row: categorize_transaction(
            row["Description"], row["Type"]
        ),
        axis=1
    )

    return df


# =====================================================
# LOAD DATA
# =====================================================

def load_transactions():

    st.sidebar.markdown("### Your Data")

    uploaded_file = st.sidebar.file_uploader(
        "Upload transaction CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            uploaded_df = pd.read_csv(uploaded_file)

            cleaned_df = clean_data(uploaded_df)

            st.sidebar.success("File uploaded successfully!")

            return add_categories(cleaned_df)

        except Exception as error:

            st.sidebar.error(f"Upload error: {error}")

    sample_df = clean_data(get_sample_data())

    return add_categories(sample_df)


# =====================================================
# ANALYSIS
# =====================================================

def get_summary(df):

    debit_df = df[df["Type"] == "Debit"]

    credit_df = df[df["Type"] == "Credit"]

    total_spent = debit_df["Amount"].sum()

    total_income = credit_df["Amount"].sum()

    transaction_count = len(df)

    duplicate_mask = df.duplicated(
        subset=["Date", "Description", "Amount", "Type"],
        keep=False
    )

    unusual_mask = pd.Series(
        False, index=df.index
    )

    if not debit_df.empty:

        median_debit = debit_df["Amount"].median()

        if median_debit > 0:

            unusual_mask = (
                (df["Type"] == "Debit")
                & (df["Amount"] > median_debit * 2.5)
            )

    review_mask = duplicate_mask | unusual_mask

    return {
        "spent": total_spent,
        "income": total_income,
        "transactions": transaction_count,
        "review": int(review_mask.sum()),
        "duplicate_mask": duplicate_mask,
        "unusual_mask": unusual_mask
    }


# =====================================================
# SIDEBAR & NAVIGATION
# =====================================================

show_sidebar_brand()

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Transactions", "Smart Review"]
)

df = load_transactions()

if df.empty:
    st.warning("No valid transactions found.")
    st.stop()

summary = get_summary(df)


# =====================================================
# OVERVIEW
# =====================================================

if page == "Overview":

    st.title("Transaction Overview")

    st.caption(
        "Understand your spending, track transactions, "
        "and see what stands out."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Spent", f"₹{summary['spent']:,.0f}")
    col2.metric("Total Income", f"₹{summary['income']:,.0f}")
    col3.metric("Transactions", summary["transactions"])
    col4.metric("Needs Review", summary["review"])

    st.divider()

    spending_df = df[df["Type"] == "Debit"]

    category_totals = (
        spending_df.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )

    left, right = st.columns([1.5, 1])

    with left:

        st.subheader("Spending by Category")

        if not category_totals.empty:

            fig = px.bar(
                category_totals,
                x="Category",
                y="Amount",
                color="Category",
                text_auto=".2s"
            )

            fig.update_layout(
                template="plotly_dark",
                showlegend=False,
                plot_bgcolor="#101512",
                paper_bgcolor="#101512",
                font_color="#E8F0EA",
                xaxis_title="Category",
                yaxis_title="Amount (₹)"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("No spending data available.")

    with right:

        st.subheader("Category Breakdown")

        if not category_totals.empty:

            fig2 = px.pie(
                category_totals,
                names="Category",
                values="Amount",
                hole=0.55
            )

            fig2.update_layout(
                template="plotly_dark",
                plot_bgcolor="#101512",
                paper_bgcolor="#101512",
                font_color="#E8F0EA"
            )

            st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Recent Transactions")

    recent_df = df.head(8).copy()

    recent_df["Date"] = recent_df["Date"].dt.strftime(
        "%d %b %Y"
    )

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TRANSACTIONS
# =====================================================

elif page == "Transactions":

    st.title("Transaction Explorer")

    st.caption(
        "Search, filter, and explore your transaction history."
    )

    search_text = st.text_input(
        "Search transactions",
        placeholder="Search merchant or description..."
    )

    col1, col2 = st.columns(2)

    with col1:

        category_filter = st.selectbox(
            "Category",
            ["All"] + sorted(df["Category"].unique().tolist())
        )

    with col2:

        type_filter = st.selectbox(
            "Transaction Type",
            ["All", "Debit", "Credit"]
        )

    filtered_df = df.copy()

    if search_text:

        filtered_df = filtered_df[
            filtered_df["Description"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if category_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Category"] == category_filter
        ]

    if type_filter != "All":

        filtered_df = filtered_df[
            filtered_df["Type"] == type_filter
        ]

    st.divider()

    st.metric("Transactions Found", len(filtered_df))

    display_df = filtered_df.copy()

    display_df["Date"] = display_df["Date"].dt.strftime(
        "%d %b %Y"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered_df.copy()

    csv_data["Date"] = csv_data["Date"].dt.strftime(
        "%Y-%m-%d"
    )

    csv_data = csv_data.drop(
        columns=["Category"],
        errors="ignore"
    )

    st.download_button(
        "Download Transactions as CSV",
        data=csv_data.to_csv(index=False),
        file_name="tracepay_transactions.csv",
        mime="text/csv"
    )


# =====================================================
# SMART REVIEW
# =====================================================

elif page == "Smart Review":

    st.title("Smart Review")

    st.caption(
        "Simple checks that help you identify transactions "
        "worth taking a closer look at."
    )

    duplicate_df = df[summary["duplicate_mask"]].copy()

    unusual_df = df[summary["unusual_mask"]].copy()

    # POSSIBLE DUPLICATES

    st.subheader("Possible Duplicate Transactions")

    if not duplicate_df.empty:

        st.warning(
            f"{len(duplicate_df)} transaction entries share "
            "the same date, description, amount and type."
        )

        duplicate_df["Date"] = duplicate_df["Date"].dt.strftime(
            "%d %b %Y"
        )

        st.dataframe(
            duplicate_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No possible duplicate transactions found.")

    st.divider()

    # UNUSUALLY LARGE TRANSACTIONS

    st.subheader("Unusually Large Transactions")

    if not unusual_df.empty:

        st.warning(
            "These debit transactions are considerably larger "
            "than the median debit amount in your dataset."
        )

        unusual_df["Date"] = unusual_df["Date"].dt.strftime(
            "%d %b %Y"
        )

        st.dataframe(
            unusual_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("No unusually large debit transactions found.")

    st.divider()

    # RECURRING MERCHANTS

    st.subheader("Recurring Merchants")

    debit_df = df[df["Type"] == "Debit"].copy()

    if not debit_df.empty:

        debit_df["Month"] = debit_df["Date"].dt.to_period("M")

        merchant_months = (
            debit_df.groupby("Description")["Month"]
            .nunique()
            .reset_index(name="Months")
        )

        recurring_merchants = merchant_months[
            merchant_months["Months"] >= 2
        ]

        if not recurring_merchants.empty:

            st.info(
                "These merchants appear in more than one calendar month."
            )

            st.dataframe(
                recurring_merchants,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No merchants found across multiple months. "
                "Upload transactions covering more than one month "
                "to explore this feature."
            )

    else:

        st.info("No debit transactions available.")

    st.divider()

    st.caption(
        "TracePay uses rule-based checks. These results are indicators "
        "for review, not confirmation of errors or fraud."
    )


# =====================================================
# FOOTER
# =====================================================

st.sidebar.divider()

st.sidebar.caption("TracePay | Transaction Intelligence")

st.sidebar.caption("Every rupee. Better understood.")