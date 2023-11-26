import tkinter as tk

class WallGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Beauty Supply Store Organizer")

        # Create frame for wall dimensions
        dimensions_frame = tk.Frame(self.root)
        dimensions_frame.pack()

        tk.Label(dimensions_frame, text="Wall Width:").grid(row=0, column=0)
        self.width_entry = tk.Entry(dimensions_frame)
        self.width_entry.grid(row=0, column=1)

        tk.Label(dimensions_frame, text="Wall Height:").grid(row=1, column=0)
        self.height_entry = tk.Entry(dimensions_frame)
        self.height_entry.grid(row=1, column=1)

        update_button = tk.Button(dimensions_frame, text="Update", command=self.update_wall)
        update_button.grid(row=2, columnspan=2)

        # Create labels and entry boxes for product details
        product_frame = tk.Frame(self.root)
        product_frame.pack()

        tk.Label(product_frame, text="Product Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(product_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(product_frame, text="Brand:").grid(row=1, column=0)
        self.brand_entry = tk.Entry(product_frame)
        self.brand_entry.grid(row=1, column=1)

        tk.Label(product_frame, text="Color:").grid(row=2, column=0)
        self.color_entry = tk.Entry(product_frame)
        self.color_entry.grid(row=2, column=1)

        tk.Label(product_frame, text="Width:").grid(row=3, column=0)
        self.prod_width_entry = tk.Entry(product_frame)
        self.prod_width_entry.grid(row=3, column=1)

        tk.Label(product_frame, text="Height:").grid(row=4, column=0)
        self.prod_height_entry = tk.Entry(product_frame)
        self.prod_height_entry.grid(row=4, column=1)

        # Create buttons to add product and obstruction
        action_frame = tk.Frame(self.root)
        action_frame.pack()

        add_product_button = tk.Button(action_frame, text="Add Product", command=self.add_product)
        add_product_button.grid(row=0, column=0)

        add_obstruction_button = tk.Button(action_frame, text="Add Obstruction", command=self.add_obstruction)
        add_obstruction_button.grid(row=0, column=1)

        # Create canvas for wall representation
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

    def update_wall(self):
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())

        self.canvas.config(width=width, height=height)

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