
categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Health",
    "Bills",
    "Education",
    "Travel",
    "Other"
]


def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    print("\nAdd Expense")

    desc = input("Description: ")
    amount = float(input("Amount: "))

    print("\nCategories:")
    for i, c in enumerate(categories, 1):
        print(i, c)

    cat = int(input("Choose category number: ")) - 1
    category = categories[cat]

    date = input("Date (YYYY-MM-DD, leave blank for today): ")

    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    expense = {
        "description": desc,
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully.\n")


def view_expenses(expenses):
    print("\nAll Expenses\n")

    total = 0

    for i, e in enumerate(expenses, 1):
        print(f"{i}. {e['date']} | {e['description']} | {e['category']} | ₹{e['amount']}")
        total += e["amount"]

    print("\nTotal spent:", total, "\n")


def delete_expense(expenses):
    view_expenses(expenses)

    try:
        idx = int(input("Enter expense number to delete: ")) - 1
        removed = expenses.pop(idx)
        save_expenses(expenses)

        print("Deleted:", removed["description"])
    except:
        print("Invalid selection")


def monthly_summary(expenses):
    month = input("Enter month (YYYY-MM): ")

    filtered = [e for e in expenses if e["date"].startswith(month)]

    if not filtered:
        print("No expenses found.")
        return

    total = sum(e["amount"] for e in filtered)

    print("\nMonthly Summary")
    print("Transactions:", len(filtered))
    print("Total spent:", total)


def main():
    expenses = load_expenses()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Monthly Summary")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            delete_expense(expenses)

        elif choice == "4":
            monthly_summary(expenses)

        elif choice == "0":
            print("Goodbye")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
=======
# expense-tracker-py
A Python CLI application to track daily expenses, analyze spending, set budgets, and export reports.
>>>>>>> 68d70b28dd0133ca8308a4c1027d2cf059b98152
