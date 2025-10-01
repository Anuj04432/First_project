import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
BUDGET_FILE = "budget.txt"

def save_budget(amount):
    with open(BUDGET_FILE,"w") as f:
        f.write(str(amount))

def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE,"r") as f:
            return float(f.read().strip())
    return None


# Initialize CSV if not exists
if not os.path.isfile(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Note"])

# Load Data
def load_data():
    return pd.read_csv(FILE_NAME)

# Add expense
def add_expense(category, amount, note):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, note])

# Clear all data
def clear_data():
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Note"])

# Streamlit App
st.set_page_config(page_title="💰 My Personal Expenses", layout="centered")
st.title("💰 My Personal Expenses Tracker")

menu = ["Add Expense", "Show Summary", "Show Graph", "Clear Data","Budget & Alerts","Export Data"]
choice = st.sidebar.radio("Menu", menu)

if choice == "Add Expense":
    st.subheader("➕ Add New Expense")
    category = st.text_input("Category")
    amount = st.text_input("Amount")
    note = st.text_input("Note (optional)")

    if st.button("Add Expense"):
        if category == "" or amount == "":
            st.error("⚠️ Category and Amount are required!")
        else:
            try:
                amount = float(amount)
                add_expense(category, amount, note)
                st.success(f"✅ Expense Added: {category} - ₹{amount}")
            except ValueError:
                st.error("⚠️ Amount must be a number!")

elif choice == "Show Summary":
    st.subheader("📄 Expense Summary")
    df = load_data()
    if df.empty:
        st.info("No expenses yet!")
    else:
        st.dataframe(df)
        total = df["Amount"].sum()
        st.write(f"### 💵 Total Spent: ₹{total}")

elif choice == "Show Graph":
    st.subheader("📊 Expenses by Category")
    df = load_data()
    if df.empty:
        st.info("No expenses to plot!")
    else:
        category_summary = df.groupby("Category")["Amount"].sum()
        fig, ax = plt.subplots()
        category_summary.plot(kind="bar", color="skyblue", ax=ax)
        ax.set_title("Expenses by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount")
        st.pyplot(fig)

elif choice == "Budget & Alerts":
    st.header=("Budget Limit")
    df = load_data()

    budget = load_budget()
    if budget is None:
        new_budget = st.number_input("Enter your monthly budget",min_value=0.0,step=100.0)
        if st.button("Save Budget"):
            save_budget(new_budget)
            st.success(f"The budget has been seted:₹{new_budget}")
            budget = new_budget
    else:
        st.info(f"Your monthly budget is:₹{budget}")

        total_spent = df["Amount"].sum()
        st.write(f"Total amount spent:₹{total_spent}")

        if total_spent > budget:
            st.error("You have exceed your budget")
        else:
            st.success(f"You are within your budget.Remaining balance:₹{budget-total_spent}")
            

        if st.button("Reset Budget"):
            os.remove(BUDGET_FILE)
            st.warning("!!Budget has been reseted!!")


elif choice == "Clear Data":
    st.subheader("🗑 Clear All Expenses")
    if st.button("Clear All Data"):
        clear_data()
        st.success("✅ All expenses cleared!")

