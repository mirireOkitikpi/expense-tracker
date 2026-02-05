from expense import Expense
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import date
import gspread
#from google.oauth2.service_account import Credentials

SPREADSHEET_NAME = "Expense Tracker"
CREDENTIALS_FILE = "credentials.json"

def get_sheets_client():
    """Authenticate and return a gspread client using OAuth (user login)."""
    return gspread.oauth(
        credentials_filename="credentials.json",
        authorized_user_filename="token.json",
    )

def get_or_create_spreadsheet(client):
    """Open existing spreadsheet or create a new one with headers."""
    try:
        spreadsheet = client.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(SPREADSHEET_NAME)
        sheet = spreadsheet.sheet1
        sheet.append_row(["Name", "Category", "Amount", "Date"])
        print(f"Created new spreadsheet: {SPREADSHEET_NAME}")
    return spreadsheet

def main():
    #get user input of expenses
    expense = get_Expense()
    print(expense)
    #write to file
    store_Expense(expense)
    #read the file and categorise the expenses
    categorise_Expense()

MONEY_PATTERN = re.compile(r"""
^\s*£?\s*
(?:
    \d{1,3}(?:,\d{3})* # comma formatting eg; 1,000 and 1,000,000
    | \d+
)
(?:\.\d{1,2})?          # rounds 12.5 to 12.50 does not permit 11.999+
\s*$
""",re.VERBOSE)

def parse_gbp_amount(raw: str) -> Decimal: # str is used rather than int or float for symbols like $ and £
    s = (raw or "").strip()
    if not s:
        raise ValueError("Amount if Required")
    if not MONEY_PATTERN.match(s):
        raise ValueError("Enter a valid amount like £12.50 or 12.50.")

    normalised = s.replace("£", "").replace(",","").strip()

    try:
        value = Decimal(normalised)
    except InvalidOperation:
        raise ValueError("Enter a valid numeric amount")
    if value <=0:
        raise ValueError("Amount must be greater than £0.00")
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def get_Expense():
    print(f"Getting Expenses")
    expense_name = input("Enter expense name: ")

    while True:
        raw_amount = input("Enter expense amount (£): ")
        try:
            expense_amount = parse_gbp_amount(raw_amount)
            break
        except ValueError as e:
            print(f"Invalid amount: {e}")

    expense_categories = [
        "Food",
        "Entertainment",
        "Rent",
        "Subsrciption",
        "Work",
        "Utilites",
    ]
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"  {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

def store_Expense(expense):
    """Store expense to Google Sheets."""
    print(f"Storing Expense to Google Sheets...")
    try:
        client = get_sheets_client()
        spreadsheet = get_or_create_spreadsheet(client)
        sheet = spreadsheet.sheet1

        row = [
            expense.name,
            expense.category,
            str(expense.amount),
            date.today().isoformat()
        ]
        sheet.append_row(row)
        print(f"Expense saved successfully!")
    except FileNotFoundError:
        print(f"Error: {CREDENTIALS_FILE} not found. Please add your service account credentials.")
    except Exception as e:
        print(f"Error saving expense: {e}")

def categorise_Expense():
    """Read expenses from Google Sheets and display summary by category."""
    print(f"\nExpense Summary by Category:")
    print("-" * 40)
    try:
        client = get_sheets_client()
        spreadsheet = get_or_create_spreadsheet(client)
        sheet = spreadsheet.sheet1

        records = sheet.get_all_records()

        if not records:
            print("No expenses recorded yet.")
            return

        category_totals = {}
        for record in records:
            category = record.get("Category", "Unknown")
            amount = Decimal(str(record.get("Amount", 0)))
            category_totals[category] = category_totals.get(category, Decimal("0")) + amount

        grand_total = Decimal("0")
        for category, total in sorted(category_totals.items()):
            print(f"  {category}: £{total:.2f}")
            grand_total += total

        print("-" * 40)
        print(f"  Total: £{grand_total:.2f}")

    except FileNotFoundError:
        print(f"Error: {CREDENTIALS_FILE} not found. Please add your service account credentials.")
    except Exception as e:
        print(f"Error reading expenses: {e}")

#having main on its own will cause it to run whenever imoported into another class
if __name__ == "__main__":
    #only true/only runs when ran as a file
    main()
