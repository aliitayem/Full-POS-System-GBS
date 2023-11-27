def draw_slits(self):
    # Clear the canvas
    self.canvas.delete("all")

    # Draw the slits
    for slit in self.slits:
        x1, y1, x2, y2 = slit

        # Check if the slit collides with any obstructions
        if self.check_obstruction_collision(x1, y1, x2, y2):
            # Split the slit into multiple segments if it collides with an obstruction
            segments = self.split_slit(slit)
            for segment in segments:
                segment_x1, segment_y1, segment_x2, segment_y2 = segment
                self.canvas.create_line(segment_x1, segment_y1, segment_x2, segment_y2, fill="red", width=2)
        else:
            # Draw a black line for the slit if it doesn't collide with any obstructions
            self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    # Draw the obstructions
    for obstacle in self.obstructions:
        x1, y1, x2, y2 = obstacle

        # Draw a blue rectangle for each obstruction
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)