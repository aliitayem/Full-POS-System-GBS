import tkinter as tk
from tkinter import ttk
import mysql.connector

# Set up the main window
window = tk.Tk()
window.title("Drag and Drop Program")
canvas_width = 1900
canvas_height = 1000
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
canvas.pack()

# Set up the database connection
db = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = db.cursor()

# Retrieve data from the MySQL table
cursor.execute("SELECT width, height, name, color FROM productDimensions")
rows = cursor.fetchall()

# Conversion rate from inches to pixels
conversion_rate = 10  # Adjust this value based on your desired ratio

# Create frames for each row in the table
frames = []
for row in rows:
    width_in_inches, height_in_inches, name, color = row
    width_in_pixels = width_in_inches * conversion_rate
    height_in_pixels = height_in_inches * conversion_rate

    frame = ttk.Frame(canvas, width=width_in_pixels, height=height_in_pixels, relief="solid", borderwidth=1)
    label = ttk.Label(frame, text=f"{name}\n{color}", justify="center")
    label.pack(fill="both", expand=True)
    frame.pack_propagate(0)  # Prevent the frame from resizing based on label content
    frames.append(frame)

# Place the frames inside a larger frame underneath the wall canvas
frame_container = ttk.Frame(window)
frame_container.pack()

for frame in frames:
    frame.grid(row=0, column=frames.index(frame))

# Slit dimensions
slit_width = 3  # Width of each slit in inches
slit_interval = 3  # Distance between each slit in inches
slit_start_y = canvas_height - conversion_rate  # Starting y-coordinate of the slits, 1 inch from the bottom

# Calculate the number of slits based on the canvas width
num_slits = canvas_width // conversion_rate

# Draw the slits on the wall canvas
for i in range(num_slits):
    x = i * conversion_rate
    canvas.create_line(x, slit_start_y, x, canvas_height, fill="black", width=1)

# TODO: Implement drag and drop functionality

# Run the main event loop
window.mainloop()

# Close the database connection
cursor.close()
db.close()