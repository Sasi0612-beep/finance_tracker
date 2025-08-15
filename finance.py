import pandas as pd
from tabulate import tabulate
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class FinanceTracker:
    def __init__(self):
        self.records = []

    def add_income(self, description, amount):
        self.records.append({"Type": "Income", "Description": description, "Amount": amount})

    def add_expense(self, description, amount):
        self.records.append({"Type": "Expense", "Description": description, "Amount": -amount})

    def get_balance(self):
        return sum(record["Amount"] for record in self.records)

    def display_table(self):
        df = pd.DataFrame(self.records)
        df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")
        print("\nFinance Summary:")
        print(tabulate(df, headers="keys", tablefmt="grid"))
        print(f"\nRemaining Balance: ${self.get_balance():,.2f}")
        return df

    def export_to_pdf(self, filename="finance_report.pdf"):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 40, "Finance Report")

        c.setFont("Helvetica-Bold", 12)
        y = height - 80
        c.drawString(50, y, "Type")
        c.drawString(150, y, "Description")
        c.drawString(400, y, "Amount")
        c.setFont("Helvetica", 12)
        y -= 20

        for record in self.records:
            if y < 50:
                c.showPage()
                y = height - 50
            c.drawString(50, y, record["Type"])
            c.drawString(150, y, record["Description"])
            c.drawString(400, y, f"${record['Amount']:,.2f}")
            y -= 20

        c.setFont("Helvetica-Bold", 12)
        if y < 70:
            c.showPage()
            y = height - 50
        c.drawString(50, y - 10, f"Remaining Balance: ${self.get_balance():,.2f}")
        c.save()
        print(f"\nPDF report saved as '{filename}'")

def main():
    tracker = FinanceTracker()
    
    print("Welcome to the Interactive Finance Tracker")
    
    while True:
        print("\nChoose an option:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Summary")
        print("4. Export to PDF")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            description = input("Enter income description: ")
            amount = int(input("Enter income amount: "))
            tracker.add_income(description, amount)
        elif choice == '2':
            description = input("Enter expense description: ")
            amount = int(input("Enter expense amount: "))
            tracker.add_expense(description, amount)
        elif choice == '3':
            tracker.display_table()
        elif choice == '4':
            filename = input("Enter filename for PDF (default: finance_report.pdf): ").strip()
            if filename == "":
                filename = "finance_report.pdf"
            tracker.export_to_pdf(filename)
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
