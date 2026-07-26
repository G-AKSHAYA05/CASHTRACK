import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="CashTrack",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# Constants
# -----------------------------
CSV_FILE = "expenses.csv"
CATEGORIES = [
    "Food", "Travel", "Shopping", "Bills", 
    "Education", "Entertainment", "Healthcare", "others"
]

# -----------------------------
# Helper Functions
# -----------------------------
def initialize_data():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Date", "Title", "Category", "Amount", "Notes"])
        df.to_csv(CSV_FILE, index=False)

def load_data():
    return pd.read_csv(CSV_FILE)

def save_expense(date, title, category, amount, notes):
    new_row = pd.DataFrame([{
        "Date": date,
        "Title": title,
        "Category": category,
        "Amount": amount,
        "Notes": notes
    }])

    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# Initialize and load data immediately
initialize_data()
df = load_data()

# -----------------------------
# Main Header
# -----------------------------
st.title("💰 CashTrack")
st.caption("Track your daily expenses and manage your monthly budget easily.")

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("💰 CashTrack")
st.sidebar.success("Welcome 👋")
st.sidebar.write(f"📅 Today: {datetime.now().strftime('%d %B %Y')}")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [" Dashboard", " Add Expense", " History", " Analytics"]
)

# -----------------------------
# Dashboard
# -----------------------------
if page == " Dashboard":
    st.header(" Dashboard")
    
    if df.empty:
        st.info("No expenses found! Add your first expense.")
    else:
        # Calculate statistics
        total_expense = df["Amount"].sum()
        total_transactions = len(df)
        highest_expense = df["Amount"].max()
        average_expense = df["Amount"].mean()

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Expense", f"₹{total_expense:.2f}")
        with col2:
            st.metric("🧾 Transactions", total_transactions)
        with col3:
            st.metric("📈 Highest Expense", f"₹{highest_expense:.2f}")
        with col4:
            st.metric(" Average Expense", f"₹{average_expense:.2f}")

# -----------------------------
# Add Expense
# -----------------------------
elif page == " Add Expense":
    st.header(" Add New Expense")
    
    with st.form("expense_form", clear_on_submit=True):
        title = st.text_input("Expense Title")
        amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", CATEGORIES)
        date = st.date_input("Date")
        notes = st.text_area("Notes (Optional)")
        
        submit = st.form_submit_button("Add Expense")
        
        if submit:
            if title == "":
                st.error("Please enter an expense title.")
            elif amount <= 0:
                st.error("Amount should be greater than zero.")
            else:
                save_expense(date, title, category, amount, notes)
                st.success("Expense Added Successfully! ✅")

# -----------------------------
# History
# -----------------------------
elif page == " History":
    st.header(" Expense History")
    
    if df.empty:
        st.info("No expenses found.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

# ----------------------------
# Analytics
# ----------------------------
elif page == " Analytics":
    st.header(" Expense Analytics")
    
    if df.empty:
        st.info("No expenses available.")
    else:
        st.subheader("Category-wise Expenses")
        category_data = df.groupby("Category")["Amount"].sum()
        st.bar_chart(category_data)
        
        st.subheader("Expenses Over Time")
        date_data = df.groupby("Date")["Amount"].sum()
        st.line_chart(date_data)

# -----------------------------
# Footer
# -----------------------------
st.sidebar.divider()
st.sidebar.caption("Made with ❤️ using Streamlit")
st.sidebar.caption("Python Workshop Project")