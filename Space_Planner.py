import tkinter as tk
from tkinter import ttk

class WallGUI:
    def __init__(self):
        self.obstructions = []
        self.root = tk.Tk()
        self.root.title("Beauty Supply Store Organizer")

        self.conversion_rate = 4  # Conversion rate from inches to pixels

        obstructions =[]

        # Create frame for Obstruction dimensions
        obstruction_frame = ttk.LabelFrame(self.root, text="Add Obstruction")
        obstruction_frame.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        tk.Label(obstruction_frame, text="Right:").grid(row=0, column=0)
        self.right_entry = tk.Entry(obstruction_frame)
        self.right_entry.grid(row=0, column=1, padx=5)

        tk.Label(obstruction_frame, text="Left:").grid(row=0, column=2)
        self.left_entry = tk.Entry(obstruction_frame)
        self.left_entry.grid(row=0, column=3, padx=5)

        tk.Label(obstruction_frame, text="Top:").grid(row=0, column=4)
        self.top_entry = tk.Entry(obstruction_frame)
        self.top_entry.grid(row=0, column=5, padx=5)

        tk.Label(obstruction_frame, text="Bottom:").grid(row=0, column=6)
        self.bottom_entry = tk.Entry(obstruction_frame)
        self.bottom_entry.grid(row=0, column=7, padx=5)

        # Create frame for wall dimensions
        dimensions_frame = ttk.LabelFrame(self.root, text="Wall Dimensions")
        dimensions_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")

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
        product_frame.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        tk.Label(product_frame, text="Product Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(product_frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(product_frame, text="Brand:").grid(row=0, column=2)
        self.brand_entry = tk.Entry(product_frame)
        self.brand_entry.grid(row=0, column=3, padx=5)

        tk.Label(product_frame, text="Color:").grid(row=0, column=4)
        self.color_entry = tk.Entry(product_frame)
        self.color_entry.grid(row=0, column=5, padx=5)

        tk.Label(product_frame, text="Width:").grid(row=0, column=6)
        self.prod_width_entry = tk.Entry(product_frame)
        self.prod_width_entry.grid(row=0, column=7, padx=5)

        tk.Label(product_frame, text="Height:").grid(row=0, column=8)
        self.prod_height_entry = tk.Entry(product_frame)
        self.prod_height_entry.grid(row=0, column=9, padx=5)

        # Create buttons to add product and obstruction
        action_frame = ttk.Frame(self.root)
        action_frame.grid(row=4, column=0, pady=10)

        add_product_button = tk.Button(product_frame, text="Add Product", command=self.add_product)
        add_product_button.grid(row=0, column=10, padx=5)

        add_obstruction_button = tk.Button(obstruction_frame, text="Add Obstruction", command=self.add_obstruction)
        add_obstruction_button.grid(row=0, column=8, padx=5)

        wall_canvas_frame = ttk.Frame(self.root)
        wall_canvas_frame.grid(row=0, column=0, columnspan=2, padx=(50, 0))

        # Create canvas for wall representation
        self.canvas = tk.Canvas(wall_canvas_frame, width=200, height=150, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def draw_slits(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Clear existing slits
        self.canvas.delete("slits")

        # Get wall dimensions
        wall_width = int(self.convert_to_inches(self.width_entry.get())) * self.conversion_rate
        wall_height = int(self.convert_to_inches(self.height_entry.get())) * self.conversion_rate

        # Calculate number of slits
        num_slits = wall_height // (3 * self.conversion_rate)

        # Define slit thickness
        slit_thickness = int(0.5 * self.conversion_rate)

        # Draw slits
        for i in range(num_slits):
            y = i * 3 * self.conversion_rate
            x1 = 0
            x2 = wall_width

            while x1 < wall_width:
                # Check for obstruction collision
                if self.check_obstruction_collision(x1, y, x2, y):
                    x1 += self.conversion_rate
                    x2 += self.conversion_rate
                    continue

                # Check for canvas boundary collision
                if x2 > canvas_width:
                    x2 = canvas_width

                # Draw slit line
                self.canvas.create_line(x1, y, x2, y, fill="black", width=slit_thickness, tags="slits")

                x1 += self.conversion_rate
                x2 += self.conversion_rate


    def add_obstruction(self):
        width = int(self.convert_to_inches(self.width_entry.get())) * self.conversion_rate
        height = int(self.convert_to_inches(self.height_entry.get())) * self.conversion_rate

        right_length = int(self.convert_to_inches(self.right_entry.get())) * self.conversion_rate
        left_length = int(self.convert_to_inches(self.left_entry.get())) * self.conversion_rate
        top_length = int(self.convert_to_inches(self.top_entry.get())) * self.conversion_rate
        bottom_length = int(self.convert_to_inches(self.bottom_entry.get())) * self.conversion_rate

        x1 = width - right_length
        y1 = height - bottom_length
        x2 = left_length
        y2 = top_length

        self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray")

        obstruction = [x1, y1, x2, y2]

        self.obstructions.append(obstruction)

        self.draw_slits()


    def check_obstruction_collision(self, x1, y1, x2, y2):
        # Check if the line collides with any obstructions
        for obstruction in self.obstructions:
            obstruction[0], obstruction[1], obstruction[2], obstruction[3] = obstruction
            if x1 < obstruction[0] and x2 > obstruction[2] and y1 == obstruction[1] and y2 == obstruction[3]:
                return True
        return False


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

        self.draw_slits()

    def add_product(self):
        name = self.name_entry.get()
        brand = self.brand_entry.get()
        color = self.color_entry.get()
        width = int(self.prod_width_entry.get())
        height = int(self.prod_height_entry.get())

        # Add product logic goes here


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WallGUI()
    app.run()
