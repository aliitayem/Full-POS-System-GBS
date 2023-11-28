import tkinter as tk

# Conversion rate: 1 inch = 10 pixels
conversion_rate = 10

# Wall dimensions in inches
wall_width_inches = 189.5
wall_height_inches = 116

# Convert wall dimensions to pixels
wall_width = wall_width_inches * conversion_rate
wall_height = wall_height_inches * conversion_rate

# Slit dimensions in inches
slit_width_inches = 0.5
slit_spacing_inches = 3

# Convert slit dimensions to pixels
slit_width = slit_width_inches * conversion_rate
slit_spacing = slit_spacing_inches * conversion_rate

# Obstruction dimensions in inches
obstruction1_width_inches = 66
obstruction1_height_inches = 51
obstruction1_x_inches = 66
obstruction1_y_inches = 51

obstruction2_width_inches = 7
obstruction2_height_inches = 98
obstruction2_x_inches = 7
obstruction2_y_inches = 32

# Convert obstruction dimensions to pixels
obstruction1_width = obstruction1_width_inches * conversion_rate
obstruction1_height = obstruction1_height_inches * conversion_rate
obstruction1_x = obstruction1_x_inches * conversion_rate
obstruction1_y = obstruction1_y_inches * conversion_rate

obstruction2_width = obstruction2_width_inches * conversion_rate
obstruction2_height = obstruction2_height_inches * conversion_rate
obstruction2_x = obstruction2_x_inches * conversion_rate
obstruction2_y = obstruction2_y_inches * conversion_rate

root = tk.Tk()
canvas = tk.Canvas(root, width=wall_width, height=wall_height)
canvas.pack()

# Draw the wall
canvas.create_rectangle(0, 0, wall_width, wall_height, fill='gray')

# Draw the slits
y = wall_height - conversion_rate  # Starting position of the first slit
while y >= conversion_rate:
    if (
        y > obstruction1_y + obstruction1_height or
        y < obstruction1_y or
        y > obstruction2_y + obstruction2_height or
        y < obstruction2_y
    ):
        canvas.create_rectangle(0, y, wall_width, y + slit_width, fill='white')
    y -= slit_spacing

# Draw the obstructions
canvas.create_rectangle(obstruction1_x, obstruction1_y, obstruction1_x + obstruction1_width, obstruction1_y + obstruction1_height, fill='blue')
canvas.create_rectangle(obstruction2_x, obstruction2_y, obstruction2_x + obstruction2_width, obstruction2_y + obstruction2_height, fill='blue')

root.mainloop()