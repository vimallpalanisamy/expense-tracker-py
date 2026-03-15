import json
import os
import csv
import sys
from datetime import datetime, date
from collections import defaultdict

# Fix Unicode printing on Windows
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = "expenses.json"
BUDGET_FILE = "budgets.json"

CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Shopping",
    "Entertainment",
    "Health & Medical",
    "Utilities & Bills",
    "Education",
    "Travel",
    "Personal Care",
    "Other",
]


def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def generate_id(expenses):
    return max((e["id"] for e in expenses), default=0) + 1


def parse_date(date_str):
    if not date_str.strip():
        return date.today()
    return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()


def format_currency(amount):
    return f"₹{amount:,.2f}"


def add_expense(expenses):
    print("\nAdd Expense")

    description = input("Description: ").strip()

    try:
        amount = float(input("Amount (₹): "))
    except ValueError:
        print("Invalid amount")
        return

    print("\nCategories")
    for i, cat in enumerate(CATEGORIES, 1):
        print(i, cat)

    try:
        cat = int(input("Choose category: ")) - 1
        category = CATEGORIES[cat]
    except:
        print("Invalid category")
        return

    date_input = input("Date (YYYY-MM-DD) [Enter = today]: ")

    try:
        exp_date = parse_date(date_input)
    except:
        print("Invalid date")
        return

    expense = {
        "id": generate_id(expenses),
        "description": description,
        "amount": amount,
        "category": category,
        "date": exp_date.strftime("%Y-%m-%d")
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added")


def view_expenses(expenses):

    if not expenses:
        print("No expenses found")
        return

    total = 0

    print("\nExpenses\n")

    for e in expenses:
        print(
            f"{e['id']} | {e['date']} | {e['description']} | {e['category']} | {format_currency(e['amount'])}"
        )
        total += e["amount"]

    print("\nTotal:", format_currency(total))


def delete_expense(expenses):

    try:
        exp_id = int(input("Enter expense ID to delete: "))
    except:
        print("Invalid ID")
        return

    for i, e in enumerate(expenses):
        if e["id"] == exp_id:
            expenses.pop(i)
            save_expenses(expenses)
            print("Expense deleted")
            return

    print("Expense not found")


def monthly_analytics(expenses):

    month = input("Month (YYYY-MM): ")

    monthly = [e for e in expenses if e["date"].startswith(month)]

    if not monthly:
        print("No data for this month")
        return

    total = sum(e["amount"] for e in monthly)

    by_category = defaultdict(float)

    for e in monthly:
        by_category[e["category"]] += e["amount"]

    print("\nMonthly Summary")
    print("Total:", format_currency(total))

    print("\nCategory Breakdown")

    for cat, amt in by_category.items():
        percent = (amt / total) * 100
        print(f"{cat} : {format_currency(amt)} ({percent:.1f}%)")


def overall_summary(expenses):

    if not expenses:
        print("No data available")
        return

    total = sum(e["amount"] for e in expenses)

    by_category = defaultdict(float)

    for e in expenses:
        by_category[e["category"]] += e["amount"]

    print("\nOverall Summary")
    print("Total Expenses:", format_currency(total))

    print("\nTop Categories")

    for cat, amt in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        percent = (amt / total) * 100
        print(f"{cat} : {format_currency(amt)} ({percent:.1f}%)")


def export_csv(expenses):

    if not expenses:
        print("No data to export")
        return

    filename = "expenses_export.csv"

    with open(filename, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow(["id", "date", "description", "category", "amount"])

        for e in expenses:
            writer.writerow(
                [e["id"], e["date"], e["description"], e["category"], e["amount"]]
            )

    print("Exported to", filename)


def load_budgets():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)
    return {}


def save_budgets(budgets):
    with open(BUDGET_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


def set_budget():

    budgets = load_budgets()

    print("\nCategories")

    for i, cat in enumerate(CATEGORIES, 1):
        print(i, cat)

    try:
        idx = int(input("Choose category: ")) - 1
        category = CATEGORIES[idx]

        amount = float(input("Monthly budget: "))

        budgets[category] = amount

        save_budgets(budgets)

        print("Budget set")

    except:
        print("Invalid input")


def main():

    expenses = load_expenses()

    while True:

        print("\nPERSONAL EXPENSE TRACKER")

        print("1 Add Expense")
        print("2 View Expenses")
        print("3 Delete Expense")
        print("4 Monthly Analytics")
        print("5 Overall Summary")
        print("6 Set Budget")
        print("7 Export CSV")
        print("0 Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            delete_expense(expenses)

        elif choice == "4":
            monthly_analytics(expenses)

        elif choice == "5":
            overall_summary(expenses)

        elif choice == "6":
            set_budget()

        elif choice == "7":
            export_csv(expenses)

        elif choice == "0":
            print("Goodbye")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()