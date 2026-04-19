import os
from datetime import date
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker Dashboard", page_icon="💸", layout="centered")

CSV_FILE = "expenses.csv"
REQUIRED_COLUMNS = ["Date", "Title", "Amount", "Category"]
CATEGORY_OPTIONS = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]

def load_expenses():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)

        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                if col == "Date":
                    df[col] = str(date.today())
                else:
                    df[col] = ""

        df = df[REQUIRED_COLUMNS]
        return df

    return pd.DataFrame(columns=REQUIRED_COLUMNS)

def save_expenses(df):
    df.to_csv(CSV_FILE, index=False)

df = load_expenses()

st.title("💸 Expense Tracker Dashboard")
st.write("Track your expenses and view simple spending summaries.")

st.subheader("Add a New Expense")

expense_date = st.date_input("Date", value=date.today())
title = st.text_input("Expense title")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.selectbox("Category", CATEGORY_OPTIONS)

if st.button("Add Expense"):
    if title.strip() == "":
        st.warning("Please enter an expense title.")
    elif amount <= 0:
        st.warning("Please enter an amount greater than 0.")
    else:
        new_expense = pd.DataFrame(
            [{
                "Date": str(expense_date),
                "Title": title,
                "Amount": amount,
                "Category": category
            }]
        )
        df = pd.concat([df, new_expense], ignore_index=True)
        save_expenses(df)
        st.success("Expense added successfully.")
        st.rerun()

st.subheader("Filter Expenses")

filter_options = ["All"] + CATEGORY_OPTIONS
selected_category = st.selectbox("Choose a category to view", filter_options)

st.subheader("Reset Data")

if st.button("Reset All Expenses"):
    empty_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    save_expenses(empty_df)
    st.success("All expenses have been deleted.")
    st.rerun()

if not df.empty:
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

if selected_category == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Category"] == selected_category].copy()

st.subheader("All Expenses")

if filtered_df.empty:
    st.info("No expenses found for the selected filter.")
else:
    st.dataframe(filtered_df, use_container_width=True)

    total_spent = filtered_df["Amount"].sum()
    st.metric("Total Spent", f"{total_spent:.2f}")

    st.subheader("Spending by Category")
    category_summary = filtered_df.groupby("Category", as_index=False)["Amount"].sum()
    st.dataframe(category_summary, use_container_width=True)

    st.subheader("Spending Chart")
    chart_data = category_summary.set_index("Category")
    st.bar_chart(chart_data)