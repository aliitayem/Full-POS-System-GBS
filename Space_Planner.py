import tkinter as tk

class DragDropApp:
    def __init__(self, root):
        self.root = root
        self.drag_data = {'x': 0, 'y': 0, 'widget': None}
        self.labels = []

        self.create_widgets()

    def create_widgets(self):
        self.create_label('Label 1', 'lightblue', 50, 50)
        self.create_label('Label 2', 'lightgreen', 200, 200)

    def create_label(self, text, color, x, y):
        label = tk.Label(self.root, text=text, bg=color, padx=10, pady=5)
        label.place(x=x, y=y)

        # Bind mouse events to the label
        label.bind('<Button-1>', self.on_drag_start)
        label.bind('<B1-Motion>', self.on_drag_motion)
        label.bind('<ButtonRelease-1>', self.on_drag_release)

        self.labels.append(label)

    def on_drag_start(self, event):
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['widget'] = event.widget

    def on_drag_motion(self, event):
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']

        widget = self.drag_data['widget']
        widget.place(x=widget.winfo_x() + dx, y=widget.winfo_y() + dy)

        self.check_collisions()

    def on_drag_release(self, event):
        self.drag_data['widget'] = None

    def check_collisions(self):
        for label in self.labels:
            if label == self.drag_data['widget']:
                continue

            # Get the bounding box coordinates of the labels
            x1, y1, x2, y2 = self.get_widget_bbox(label)
            x3, y3, x4, y4 = self.get_widget_bbox(self.drag_data['widget'])

            # Check for collision between labels
            if x1 < x4 < x2 and y1 < y4 < y2:
                self.stop_movement()

            # Check for collision with GUI borders
            if x3 < 0 or y3 < 0 or x4 > self.root.winfo_width() or y4 > self.root.winfo_height():
                self.stop_movement()

    def get_widget_bbox(self, widget):
        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()
        return x, y, x + width, y + height

    def stop_movement(self):
        self.drag_data['widget'].place(x=self.drag_data['widget'].winfo_x(), y=self.drag_data['widget'].winfo_y())

if __name__ == '__main__':
    root = tk.Tk()
    app = DragDropApp(root)
    root.mainloop()