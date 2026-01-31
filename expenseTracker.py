from expense import Expense

def main():

    #get user input of expenses
    expense = get_Expense()
    print(expense)
    #write to file  
    store_Expense()
    #read the file and categorise the expenses 
    categorise_Expense()
    pass

def get_Expense():
    print(f"Getting Expenses")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    
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