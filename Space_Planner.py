import tkinter as tk
from tkinter import ttk

class WallGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Beauty Supply Store Organizer")

        self.conversion_rate = 20  # Conversion rate from inches to pixels

        # Create frame for wall dimensions
        dimensions_frame = ttk.LabelFrame(self.root, text="Wall Dimensions")
        dimensions_frame.pack(padx=10, pady=10)

        tk.Label(dimensions_frame, text="Wall Width:").grid(row=0, column=0)
        self.width_entry = tk.Entry(dimensions_frame)
        self.width_entry.grid(row=0, column=1, padx=5)

        tk.Label(dimensions_frame, text="Wall Height:").grid(row=0, column=2)
        self.height_entry = tk.Entry(dimensions_frame)
        self.height_entry.grid(row=0, column=3, padx=5)

        apply_button = tk.Button(dimensions_frame, text="Apply", command=self.update_wall)
        apply_button.grid(row=0, column=4, padx=5)

        # Create Label Frame for product details
        product_frame = ttk.LabelFrame(self.root, text="Product")
        product_frame.pack(padx=10, pady=10)

        tk.Label(product_frame, text="Product Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(product_frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(product_frame, text="Brand:").grid(row=0, column=2)
        self.brand_entry = tk.Entry(product_frame)
        self.brand_entry.grid(row=0, column=3, padx=5)

        tk.Label(product_frame, text="Color:").grid(row=1, column=0)
        self.color_entry = tk.Entry(product_frame)
        self.color_entry.grid(row=1, column=1, padx=5)

        tk.Label(product_frame, text="Width:").grid(row=1, column=2)
        self.prod_width_entry = tk.Entry(product_frame)
        self.prod_width_entry.grid(row=1, column=3, padx=5)

        tk.Label(product_frame, text="Height:").grid(row=1, column=4)
        self.prod_height_entry = tk.Entry(product_frame)
        self.prod_height_entry.grid(row=1, column=5, padx=5)

        # Create buttons to add product and obstruction
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=10)

        add_product_button = tk.Button(action_frame, text="Add Product", command=self.add_product)
        add_product_button.grid(row=0, column=0, padx=5)

        add_obstruction_button = tk.Button(action_frame, text="Add Obstruction", command=self.add_obstruction)
        add_obstruction_button.grid(row=0, column=1, padx=5)

        # Create canvas for wall representation
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

    def convert_to_inches(self, dimension):
        total_inches = 0

        feet, inches = dimension.split(",")
        feet = feet.strip()
        inches = inches.strip()

        if feet:
            total_inches += int(feet) * 12

        if inches:
            total_inches += int(inches)

        return total_inches

    def update_wall(self):
        width = self.convert_to_inches(self.width_entry.get())
        height = self.convert_to_inches(self.height_entry.get())

        width_pixels = width * self.conversion_rate
        height_pixels = height * self.conversion_rate

        self.canvas.config(width=width_pixels, height=height_pixels)

    def add_product(self):
        name = self.name_entry.get()
        brand = self.brand_entry.get()
        color = self.color_entry.get()
        width = int(self.prod_width_entry.get())
        height = int(self.prod_height_entry.get())

        # Add product logic goes here

    def add_obstruction(self):
        # Add obstruction logic goes here
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WallGUI()
    app.run()