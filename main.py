# This project is a simple expense tracker(web app), with an add, remove and many other functions.
# Overall Idea of the project is to:
# - Add new expenses with details such as date, description, amount, and category.
# - Remove or edit existing expenses.
# - View all expenses or just today's expenses.
# - Calculate the total expenses, sum by category, or sum by description.
# - Search for expenses based on description or category.
# - Export expenses to a CSV file.
# - Display expenses visually using bar and pie charts.
# - Manage and save expenses in a JSON file.
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
from datetime import datetime
import json
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkcalendar import DateEntry
class Expense:
    def __init__(self, date, description, amount, category="Uncategorized"):
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

class ExpenseTracker:
    def __init__(self):
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def sum_by_category(self, category):
        return sum(expense.amount for expense in self.expenses if expense.category.lower() == category.lower())

    def sum_by_description(self, description):
        return sum(expense.amount for expense in self.expenses if description.lower() in expense.description.lower())

    def remove_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            return True
        return False

    def view_expenses(self):
        return [vars(expense) for expense in self.expenses]

    def total_expenses(self):
        return sum(expense.amount for expense in self.expenses)

    def save_expenses(self, filename):
        with open(filename, 'w') as file:
            json.dump([vars(expense) for expense in self.expenses], file)

    def load_expenses(self, filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.expenses = [Expense(**expense) for expense in data]
        except FileNotFoundError:
            self.expenses = []

    def filter_expenses(self, search_term):
        return [expense for expense in self.expenses if search_term.lower() in expense.description.lower() or search_term.lower() in expense.category.lower()]

    def get_today_expenses(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return [expense for expense in self.expenses if expense.date == today]

    def add_expenses_from_bank(self, transactions):
        for transaction in transactions:
            expense = Expense(
                date=transaction['date'],
                description=transaction['name'],
                amount=transaction['amount'],
                category=transaction.get('category', 'Uncategorized')
            )
            self.add_expense(expense)

class ExpenseTrackerApp(tk.Tk):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.tracker = ExpenseTracker()
        self.tracker.load_expenses(self.filename)
        self.create_widgets()

    def create_widgets(self):
        self.title("Expense Tracker App")
        self.geometry("1200x800")

        # Header
        header = tk.Frame(self, bg="#4a90e2", padx=10, pady=10)
        header.pack(fill=tk.X)
        title_label = tk.Label(header, text="Expense Tracker", font=("Arial", 24, "bold"), bg="#4a90e2", fg="white")
        title_label.pack()

        # Form for adding expenses
        form_frame = tk.Frame(self, pady=10)
        form_frame.pack(fill=tk.X, padx=20)

        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
        self.date_entry = DateEntry(form_frame, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5)
        self.desc_entry = tk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Amount:").grid(row=2, column=0, padx=5)
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5)

        tk.Label(form_frame, text="Category:").grid(row=3, column=0, padx=5)
        self.category_var = tk.StringVar()
        self.category_combobox = ttk.Combobox(form_frame, textvariable=self.category_var)
        self.category_combobox['values'] = ("Food", "Rent", "Utilities", "Transportation", "Healthcare", "Leisure/Fun")
        self.category_combobox.grid(row=3, column=1, padx=5)

        # Buttons for actions
        button_frame = tk.Frame(self, pady=10)
        button_frame.pack(fill=tk.X, padx=20)

        ttk.Button(button_frame, text="Add Expense", command=self.add_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Expense", command=self.remove_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Edit Expense", command=self.edit_expense).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Expenses", command=self.view_expenses).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="View Today's Expenses", command=self.view_today_expenses).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Total Expenses", command=self.total_expenses).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search Expenses", command=self.search_expenses).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sum by Category", command=self.sum_by_category).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Sum by Description", command=self.sum_by_description).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Expense Chart", command=self.show_expense_chart).pack(side=tk.LEFT, padx=5)

        # Expense Listbox
        self.expense_listbox = tk.Listbox(self, height=20, width=150)
        self.expense_listbox.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

    def add_expense(self):
        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        description = self.desc_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return
        category = self.category_var.get() or "Uncategorized"
        expense = Expense(date, description, amount, category)
        self.tracker.add_expense(expense)
        self.tracker.save_expenses(self.filename)
        self.view_today_expenses()
        messagebox.showinfo("Expense Tracker", "Expense added successfully.")

    def remove_expense(self):
        index = self.get_selected_index()
        if index is not None:
            confirm = messagebox.askyesno("Confirm Removal", "Are you sure you want to remove this expense?")
            if confirm:
                if self.tracker.remove_expense(index):
                    self.tracker.save_expenses(self.filename)
                    self.view_today_expenses()
                    messagebox.showinfo("Expense Tracker", "Expense removed successfully.")
                else:
                    messagebox.showerror("Expense Tracker", "Failed to remove expense.")
        else:
            messagebox.showerror("Expense Tracker", "Please select an expense to remove.")

    def edit_expense(self):
        index = self.get_selected_index()
        if index is not None:
            expense = self.tracker.expenses[index]
            self.date_entry.set_date(expense.date)
            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(tk.END, expense.description)
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(tk.END, str(expense.amount))
            self.category_combobox.set(expense.category)
            self.tracker.remove_expense(index)
        else:
            messagebox.showerror("Expense Tracker", "Please select an expense to edit.")

    def view_expenses(self):
        self.expense_listbox.delete(0, tk.END)
        expenses = self.tracker.view_expenses()
        for i, expense in enumerate(expenses, start=1):
            self.expense_listbox.insert(tk.END, f"{i}. Date: {expense['date']}, Description: {expense['description']}, Amount: ${expense['amount']:.2f}, Category: {expense['category']}")

    def view_today_expenses(self):
        self.expense_listbox.delete(0, tk.END)
        today_expenses = self.tracker.get_today_expenses()
        if len(today_expenses) == 0:
            self.expense_listbox.insert(tk.END, "No expenses for today.")
        else:
            for i, expense in enumerate(today_expenses, start=1):
                self.expense_listbox.insert(tk.END, f"{i}. Date: {expense.date}, Description: {expense.description}, Amount: ${expense.amount:.2f}, Category: {expense.category}")

    def total_expenses(self):
        total = self.tracker.total_expenses()
        messagebox.showinfo("Total Expenses", f"Total Expenses: ${total:.2f}")

    def search_expenses(self):
        search_term = simpledialog.askstring("Search Expenses", "Enter description or category to search:")
        if search_term:
            results = self.tracker.filter_expenses(search_term)
            self.expense_listbox.delete(0, tk.END)
            if len(results) == 0:
                self.expense_listbox.insert(tk.END, "No matching expenses found.")
            else:
                for i, expense in enumerate(results, start=1):
                    self.expense_listbox.insert(tk.END, f"{i}. Date: {expense.date}, Description: {expense.description}, Amount: ${expense.amount:.2f}, Category: {expense.category}")

    def sum_by_category(self):
        category = simpledialog.askstring("Sum by Category", "Enter category:")
        if category:
            total = self.tracker.sum_by_category(category)
            messagebox.showinfo("Sum by Category", f"Total for category '{category}': ${total:.2f}")

    def sum_by_description(self):
        description = simpledialog.askstring("Sum by Description", "Enter description:")
        if description:
            total = self.tracker.sum_by_description(description)
            messagebox.showinfo("Sum by Description", f"Total for description '{description}': ${total:.2f}")

    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Description", "Amount", "Category"])
                for expense in self.tracker.expenses:
                    writer.writerow([expense.date, expense.description, expense.amount, expense.category])
            messagebox.showinfo("Export to CSV", "Expenses exported successfully.")

    def show_expense_chart(self):
        if not self.tracker.expenses:
            messagebox.showinfo("No Data", "No expenses to display.")
            return
        
        # Aggregate expenses by category
        categories = {}
        for expense in self.tracker.expenses:
            categories[expense.category] = categories.get(expense.category, 0) + expense.amount

        # Here is bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(categories.keys(), categories.values(), color="#4a90e2", edgecolor='black')

        # The data labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'${height:.2f}', ha='center', va='bottom', fontsize=10, color='black')

        plt.xlabel('Categories', fontsize=14, fontweight='bold')
        plt.ylabel('Total Amount ($)', fontsize=14, fontweight='bold')
        plt.title('Expenses by Category', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Create pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', colors=plt.cm.Paired(range(len(categories))), startangle=140)
        plt.title('Expenses Distribution by Category', fontsize=16, fontweight='bold')
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

    def get_selected_index(self):
        try:
            return self.expense_listbox.curselection()[0]
        except IndexError:
            messagebox.showerror("Expense Tracker", "Please select an expense.")
            return None

if __name__ == "__main__":
    app = ExpenseTrackerApp("expenses.json")
    app.mainloop()
