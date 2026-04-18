import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker Dashboard", page_icon="💸", layout="centered")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.title("💸 Expense Tracker Dashboard")
st.write("Track your expenses and view simple spending summaries.")

st.subheader("Add a New Expense")

title = st.text_input("Expense title")
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])

if st.button("Add Expense"):
    if title.strip() == "":
        st.warning("Please enter an expense title.")
    elif amount <= 0:
        st.warning("Please enter an amount greater than 0.")
    else:
        st.session_state.expenses.append(
            {
                "Title": title,
                "Amount": amount,
                "Category": category
            }
        )
        st.success("Expense added successfully.")

st.subheader("All Expenses")

if len(st.session_state.expenses) == 0:
    st.info("No expenses added yet.")
else:
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df, use_container_width=True)

    total_spent = df["Amount"].sum()
    st.metric("Total Spent", f"{total_spent:.2f}")

    st.subheader("Spending by Category")
    category_summary = df.groupby("Category", as_index=False)["Amount"].sum()
    st.dataframe(category_summary, use_container_width=True)