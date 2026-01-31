from expense import Expense
import re 
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def main():

    #get user input of expenses
    expense = get_Expense()
    print(expense)
    #write to file  
    store_Expense()
    #read the file and categorise the expenses 
    categorise_Expense()
    pass

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
    if value <= 0:
        raise ValueError("Amount must be greater than £0.00")
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def get_Expense():
    print(f"Getting Expenses")
    expense_name = input("Enter expense name: ")

    while True:
        expense_input = input("Enter expense amount (e.g. £12.50 or 12.50): ")
        try:
            expense_amount = parse_gbp_amount(expense_input)
            break
        except ValueError as e:
            print(f"Invalid amount: {e}. Please try again.")
    
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

def store_Expense():
    print(f"Storing Expenses to Excel File")

def categorise_Expense():
    print(f"Categorising Expenses")

#having main on its own will cause it to run whenever imoported into another class
if __name__ == "__main__":  
    #only true/only runs when ran as a file
    main()