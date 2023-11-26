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