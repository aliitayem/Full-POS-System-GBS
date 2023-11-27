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

def check_obstruction_collision(self, x1, y1, x2, y2):
    # Check if the line collides with any obstructions
    for obstacle in self.obstacles:
        if x1 < obstacle[0] and x2 > obstacle[2] and y1 == obstacle[1] and y2 == obstacle[3]:
            return True
    return False