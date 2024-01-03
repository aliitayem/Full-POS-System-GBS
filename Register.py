from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import colorchooser
import tkinter.font as tkFont
import tkinter as tk
import mysql.connector
from decimal import Decimal
import os

tab = Tk()
tab.title('Gena Beauty Supply')
tab.geometry("1500x1000")

my_notebook = ttk.Notebook(tab)
my_notebook.pack(pady=15)

my_frame1 = Frame(my_notebook, width=1500, height=1000, bg="white")
my_frame2 = Frame(my_notebook, width=1500, height=1000, bg="white")
my_frame3 = Frame(my_notebook, width=1500, height=1000, bg="white")

my_frame1.pack(fill="both", expand=1)
my_frame2.pack(fill="both", expand=1)
my_frame3.pack(fill="both", expand=1)

my_notebook.add(my_frame1, text="Inventory")
my_notebook.add(my_frame2, text="Cart")
my_notebook.add(my_frame3, text="Customer")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="inventory"
)

mycursor = db.cursor()

Cart = tk.Frame(my_frame2, width=800, height=635, bg="White")
Cart.grid(row=0, column=0, padx=(15, 80))

Register = tk.Frame(my_frame2, width=635, height=635, bg="White", highlightthickness=5, highlightbackground="black")
Register.grid(row=0, column=1)

# Create a Treeview Frame
tree_frame = tk.Frame(Cart)
tree_frame.grid(row=0, column=0, columnspan=2)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree2 = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree2.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree2.yview)

# Define Our Columns
my_tree2['columns'] = (
    "ID", "Barcode", "Name", "Price", "Quantity")

# Format Our Columns
my_tree2.column("#0", width=0, stretch=NO)
my_tree2.column("ID", anchor=CENTER, width=50)
my_tree2.column("Price", anchor=CENTER, width=140)
my_tree2.column("Quantity", anchor=CENTER, width=280)
my_tree2.column("Barcode", anchor=CENTER, width=80)
my_tree2.column("Name", anchor=CENTER, width=60)

# Create Headings
my_tree2.heading("#0", text="", anchor=W)
my_tree2.heading("ID", text="ID", anchor=CENTER)
my_tree2.heading("Price", text="Barcode", anchor=CENTER)
my_tree2.heading("Quantity", text="Name", anchor=CENTER)
my_tree2.heading("Barcode", text="Price", anchor=CENTER)
my_tree2.heading("Name", text="Quantity", anchor=CENTER)

TaxedReturnTotal = 0

def ManualEntry():
    pass


def query_database2():
    for record in my_tree2.get_children():
        my_tree2.delete(record)

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="inventory"
    )

    mycursor = db.cursor()

    mycursor.execute("SELECT * FROM carts")
    records = mycursor.fetchall()

    # Add our data to the screen
    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree2.insert(parent='', index='end', iid=count, text='',
                            values=(
                                record[0], record[1], record[2], record[3], record[4]))
        else:
            my_tree2.insert(parent='', index='end', iid=count, text='',
                            values=(
                                record[0], record[1], record[2], record[3], record[4]))
        count += 1
    db.commit()
    db.close()


# Create a function to fetch customer data from the "customers" table
def fetch_customer_data(phone_number):
    # Connect to your MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="inventory"
    )

    mycursor = db.cursor()

    global TaxedReturnsTotal

    # Fetch the "discount" and "points" columns based on the phone number
    query = "SELECT discount, points FROM customers WHERE phone_number = %s"
    mycursor.execute(query, (phone_number,))
    result = mycursor.fetchone()

    mycursor.close()
    db.close()

    return result


# Determine the discount based on the fetched customer data
def determine_discount(phone_number):
    customer_data = fetch_customer_data(phone_number)

    global manual_discount
    global TaxedReturnsTotal

    if customer_data:
        discount, points = customer_data

        if discount == "Stylist":
            return "10%"
        elif discount == "Employee" or points == "100":
            return "20%"

    manual_discount = float(Cash_number_label.cget("text"))

    return "None"


def Return():
    # Establish a connection to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="inventory"
    )

    mycursor = db.cursor()

    global TaxedReturnsTotal

    mycursor.execute("UPDATE inventory.carts SET Status = 'Return' WHERE Status = 'Sale'")
    mycursor.execute("UPDATE inventory.carts SET price = -price WHERE Status = 'Return'")
    mycursor.execute("SELECT * FROM inventory.carts WHERE price < 0")
    return_results = mycursor.fetchall()
    mycursor.execute("SELECT (price * quantity) * 1.092 AS ReturnSubtotal FROM inventory.carts WHERE price < 0")
    taxed_return_results = mycursor.fetchall()

    TaxedReturnsSubtotal = sum(row[0] for row in taxed_return_results)
    TaxedReturnsFloat = float(TaxedReturnsSubtotal)
    TaxedReturnsTotal = round(TaxedReturnsFloat, 2)

    db.commit()

    mycursor.close()
    db.close()

    update_discount_label(phone_entry.get())
    query_database2()


def UpdateCashToZero():
    Cash_number_label.config(text = "0.00")


# Update the Discount label in your tkinter GUI
def update_discount_label(phone_number):
    discount = determine_discount(phone_number)
    Discount_number.config(text=discount)

    UpdateCashToZero()

    # Establish a connection to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="inventory"
    )

    mycursor = db.cursor()

    # Execute the query to multiply price by quantity for each record

    mycursor.execute("SELECT barcode, price * quantity AS total FROM carts WHERE price > 0")

    # Fetch all the results

    results = mycursor.fetchall()

    global manual_discount
    global TaxedReturnsTotal

    mycursor.execute("SELECT (price * quantity) * 1.092 AS ReturnSubtotal FROM inventory.carts WHERE price < 0")
    taxed_return_results = mycursor.fetchall()

    TaxedReturnsSubtotal = sum(row[0] for row in taxed_return_results)
    TaxedReturnsFloat = float(TaxedReturnsSubtotal)
    TaxedReturnsTotal = round(TaxedReturnsFloat, 2)


    if discount == "20%":

        discount = 0.2

        subtotal = sum(row[1] for row in results)
        subtotal_float = float(subtotal)
        discounted_subtotal = subtotal_float - (subtotal_float * discount)
        return_applied_subtotal = discounted_subtotal + TaxedReturnsTotal
        displayed_subtotal = round(return_applied_subtotal, 2)
        tax = discounted_subtotal * 0.092
        rounded_tax = round(tax, 2)
        total = discounted_subtotal + tax
        rounded_total = round(total, 2)
        return_applied_total = rounded_total + TaxedReturnsTotal
        displayed_total = round(return_applied_total, 2)
    elif discount == "10%":

        discount = 0.1

        subtotal = sum(row[1] for row in results)
        subtotal_float = float(subtotal)
        discounted_subtotal = subtotal_float - (subtotal_float * discount)
        return_applied_subtotal = discounted_subtotal + TaxedReturnsTotal
        displayed_subtotal = round(return_applied_subtotal, 2)
        tax = discounted_subtotal * 0.092
        rounded_tax = round(tax, 2)
        total = discounted_subtotal + tax
        rounded_total = round(total, 2)
        return_applied_total = rounded_total + TaxedReturnsTotal
        displayed_total = round(return_applied_total, 2)
    elif manual_discount != 0.00:

        discount = manual_discount

        subtotal = sum(row[1] for row in results)
        subtotal_float = float(subtotal)
        discounted_subtotal = subtotal_float - (subtotal_float * discount)
        return_applied_subtotal = discounted_subtotal + TaxedReturnsTotal
        displayed_subtotal = round(return_applied_subtotal, 2)
        tax = discounted_subtotal * 0.092
        rounded_tax = round(tax, 2)
        total = discounted_subtotal + tax
        rounded_total = round(total, 2)
        return_applied_total = rounded_total + TaxedReturnsTotal
        displayed_total = round(return_applied_total, 2)
    else:

        discount = 0

        subtotal = sum(row[1] for row in results)
        subtotal_float = float(subtotal)
        discounted_subtotal = subtotal_float - (subtotal_float * discount)
        return_applied_subtotal = discounted_subtotal + TaxedReturnsTotal
        displayed_subtotal = round(return_applied_subtotal, 2)
        tax = discounted_subtotal * 0.092
        rounded_tax = round(tax, 2)
        total = discounted_subtotal + tax
        rounded_total = round(total, 2)
        return_applied_total = rounded_total + TaxedReturnsTotal
        displayed_total = round(return_applied_total, 2)

    # Print the total sum

    discount_percentage_int = int(discount * 100)
    discount_percentage_string = str(discount_percentage_int)
    discount_percentage = discount_percentage_string + "%"

    Subtotal_number.config(text=displayed_subtotal)
    Tax_number.config(text=rounded_tax)
    Discount_number.config(text=discount_percentage)
    Total_number.config(text=displayed_total)

    # Close the cursor and database connection

    mycursor.close()
    db.commit()
    db.close()


def update_label(digit):
    global TaxedReturnsTotal

    current_text = Cash_number_label.cget("text")

    # Remove the decimal point if it exists
    current_text = current_text.replace(".", "")

    # Remove one of the initial three zeros
    if current_text.startswith("0") and len(current_text) > 1:
        current_text = current_text[1:]

    # Concatenate the clicked digit to the current text
    current_text += str(digit)

    # Insert the decimal point two characters from the last character
    decimal_index = len(current_text) - 2
    current_text = current_text[:decimal_index] + "." + current_text[decimal_index:]

    # Update the label text
    Cash_number_label.config(text=current_text)


def add_To_Cart(self):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="inventory"
    )

    mycursor = db.cursor()

    global TaxedReturnsTotal

    barcode = barcode_entry2.get()

    mycursor.execute("SELECT id, price, barcode, name FROM inventory.products WHERE barcode = %s", (barcode,))
    result = mycursor.fetchone()

    if result:
        id, price, barcode, name = result

        mycursor.execute(
            "INSERT INTO inventory.carts (id, price, quantity, barcode, name) VALUES (%s, %s, 1, %s, %s)  ON DUPLICATE KEY UPDATE quantity = quantity + 1",
            (id, price, barcode, name))
        print("Item Added To Cart Successfully")
    else:
        print("Item Not Found")

    db.commit()
    db.close()

    barcode_entry2.delete(0, END)

    global phone_entry
    value = phone_entry
    update_discount_label(phone_number=phone_entry.get())

    query_database2()


def clear_label():
    Cash_number_label.config(text="0.00")


def Cancel():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="inventory"
    )

    mycursor = db.cursor()

    mycursor.execute("DELETE FROM inventory.carts")

    mycursor.close()
    db.commit()
    db.close()

    query_database2()
    update_discount_label(phone_entry.get())


# Create a label to display the entered amount
Cash_label = tk.Label(Register, text="Cash", bg="White", font=("Arial", 24))
Cash_label.grid(row=0, column=0, sticky="w")

# Create a label to display the entered amount
Cash_number_label = tk.Label(Register, text="0.00", bg="White", font=("Arial", 24))
Cash_number_label.grid(row=0, column=0, sticky="e")

# Create a label to display the entered amount
Change_label = tk.Label(Register, text="Change", bg="White", font=("Arial", 24))
Change_label.grid(row=1, column=0, sticky="w")

# Create a label to display the entered amount
Change_number_label = tk.Label(Register, text="0.00", bg="White", font=("Arial", 24))
Change_number_label.grid(row=1, column=0, sticky="e")

Barcode_Frame = Frame(Cart, bg="White")
Barcode_Frame.grid(row=2, column=0, sticky="w", pady=(10, 0))

Phone_Frame = Frame(Cart, bg="White")
Phone_Frame.grid(row=3, column=0, columnspan=4, sticky="w", pady=(10, 0))


def on_entry_click_phone(event):
    if phone_entry.get() == "Enter Phone Number Here":
        phone_entry.delete(0, tk.END)
        phone_entry.configure(foreground='black')


def on_focus_out_phone(event):
    if phone_entry.get() == "":
        phone_entry.insert(0, "Enter Phone Number Here")
        phone_entry.configure(foreground='gray')


def on_entry_click_barcode(event):
    if barcode_entry2.get() == "Press Here To Scan Barcode":
        barcode_entry2.delete(0, tk.END)
        barcode_entry2.configure(foreground='black')


def on_focus_out_barcode(event):
    if barcode_entry2.get() == "":
        barcode_entry2.insert(0, "Press Here To Scan Barcode")
        barcode_entry2.configure(foreground='gray')


# Create an Entry widget
phone_entry = tk.Entry(Phone_Frame, highlightbackground="black", highlightthickness=1, width=30, fg='gray')
phone_entry.insert(0, "Enter Phone Number Here")
phone_entry.bind("<FocusIn>", on_entry_click_phone)
phone_entry.bind("<FocusOut>", on_focus_out_phone)
phone_entry.grid(row=0, column=0)

barcode_entry2 = tk.Entry(Barcode_Frame, highlightbackground="black", highlightthickness=1, width=30, fg='gray')
barcode_entry2.insert(0, "Press Here To Scan Barcode")
barcode_entry2.bind("<FocusIn>", on_entry_click_barcode)
barcode_entry2.bind("<FocusOut>", on_focus_out_barcode)
barcode_entry2.grid(row=0, column=0, sticky="w")

# Example button to trigger the discount update
update_button = tk.Button(Phone_Frame, text="Apply", width=10, height=3,
                          command=lambda: update_discount_label(phone_entry.get()))
update_button.grid(row=1, column=0, pady=(10, 230))

Checkout_Totals_Frame = Frame(Cart, bg="White")
Checkout_Totals_Frame.grid(row=1, column=0, sticky="w")

Subtotal = tk.Label(Checkout_Totals_Frame, text="Subtotal ", bg="White", font=("Arial", 18))
Subtotal.grid(row=0, column=0, sticky="w")

Discount = tk.Label(Checkout_Totals_Frame, text="Discount ", bg="White", font=("Arial", 18))
Discount.grid(row=1, column=0, sticky="w")

Tax = tk.Label(Checkout_Totals_Frame, text="Tax ", bg="White", font=("Arial", 18))
Tax.grid(row=2, column=0, sticky="w")

Total = tk.Label(Checkout_Totals_Frame, text="Total ", bg="White", font=("Arial", 18))
Total.grid(row=3, column=0, sticky="w")

Checkout_Totals_Numbers_Frame = Frame(Cart, bg="White")
Checkout_Totals_Numbers_Frame.grid(row=1, column=1, sticky="w", padx=(340, 0))

Subtotal_number = tk.Label(Checkout_Totals_Numbers_Frame, text="", bg="White", font=("Arial", 18))
Subtotal_number.grid(row=0, column=0, sticky="e")

Discount_number = tk.Label(Checkout_Totals_Numbers_Frame, text="", bg="White", font=("Arial", 18))
Discount_number.grid(row=1, column=0, sticky="e")

Tax_number = tk.Label(Checkout_Totals_Numbers_Frame, text="", bg="White", font=("Arial", 18))
Tax_number.grid(row=2, column=0, sticky="e")

Total_number = tk.Label(Checkout_Totals_Numbers_Frame, text="", bg="White", font=("Arial", 18))
Total_number.grid(row=3, column=0, sticky="e")

Register_Button_Frame = Frame(Register)
Register_Button_Frame.grid(row=2, column=0)

# Create button0 for digit 0
button0 = tk.Button(Register_Button_Frame, text="0", width=13, height=7, command=lambda: update_label('0'))
button0.grid(row=6, column=0)

button00 = tk.Button(Register_Button_Frame, text="00", width=13, height=7, command=lambda: update_label('00'))
button00.grid(row=6, column=1)

button99 = tk.Button(Register_Button_Frame, text="99", width=13, height=7, command=lambda: update_label('99'))
button99.grid(row=6, column=2)

# Create buttons for digits 1 through 9
button1 = tk.Button(Register_Button_Frame, text="1", width=13, height=7, command=lambda: update_label('1'))
button1.grid(row=5, column=0)

button2 = tk.Button(Register_Button_Frame, text="2", width=13, height=7, command=lambda: update_label('2'))
button2.grid(row=5, column=1)

button3 = tk.Button(Register_Button_Frame, text="3", width=13, height=7, command=lambda: update_label('3'))
button3.grid(row=5, column=2)

button4 = tk.Button(Register_Button_Frame, text="4", width=13, height=7, command=lambda: update_label('4'))
button4.grid(row=4, column=0)

button5 = tk.Button(Register_Button_Frame, text="5", width=13, height=7, command=lambda: update_label('5'))
button5.grid(row=4, column=1)

button6 = tk.Button(Register_Button_Frame, text="6", width=13, height=7, command=lambda: update_label('6'))
button6.grid(row=4, column=2)

button7 = tk.Button(Register_Button_Frame, text="7", width=13, height=7, command=lambda: update_label('7'))
button7.grid(row=3, column=0)

button8 = tk.Button(Register_Button_Frame, text="8", width=13, height=7, command=lambda: update_label('8'))
button8.grid(row=3, column=1)

button9 = tk.Button(Register_Button_Frame, text="9", width=13, height=7, command=lambda: update_label('9'))
button9.grid(row=3, column=2)

button9 = tk.Button(Register_Button_Frame, text="9", width=13, height=7, command=lambda: update_label('9'))
button9.grid(row=3, column=2)

button_cash = tk.Button(Register_Button_Frame, text="Cash", width=28, height=7, command=lambda: update_label('9'))
button_cash.grid(row=6, column=3, columnspan=2)

button_return = tk.Button(Register_Button_Frame, text="Return", width=13, height=7, command=lambda: Return())
button_return.grid(row=4, column=3)

button_discount = tk.Button(Register_Button_Frame, text="Discount", width=13, height=7,
                            command=lambda: update_discount_label(phone_entry.get()))
button_discount.grid(row=4, column=4)

button_Cancel = tk.Button(Register_Button_Frame, text="Cancel", width=13, height=7, command=lambda: Cancel())
button_Cancel.grid(row=3, column=3)

button_No_Sale = tk.Button(Register_Button_Frame, text="#/NS", width=13, height=7, command=lambda: update_label('9'))
button_No_Sale.grid(row=3, column=4)

button_clear = tk.Button(Register_Button_Frame, text="Clear", width=28, height=7, command=clear_label)
button_clear.grid(row=5, column=3, columnspan=2)

button_manual_entry = tk.Button(Register_Button_Frame, text="Manual Entry", width=71, height=7,
                                command=lambda: update_label('9'))
button_manual_entry.grid(row=2, column=0, columnspan=5)

button_membership = tk.Button(Register_Button_Frame, text="Placeholder", width=71, height=4)
button_membership.grid(row=1, column=0, columnspan=5)

tab.bind("<Return>", add_To_Cart)

query_database2()

tab.mainloop()
