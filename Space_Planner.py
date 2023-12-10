import tkinter as tk
import math

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

    def on_drag_release(self, event):
        self.snap_to_closest_label()
        self.drag_data['widget'] = None

    def snap_to_closest_label(self):
        closest_label = None
        min_distance = float('inf')

        for label in self.labels:
            if label == self.drag_data['widget']:
                continue

            x1, y1, _, _ = self.get_widget_bbox(label)
            x2, y2, _, _ = self.get_widget_bbox(self.drag_data['widget'])

            dx = x1 - x2
            dy = y1 - y2
            distance = math.sqrt(dx**2 + dy**2)

            if distance < min_distance:
                min_distance = distance
                closest_label = label

        if closest_label:
            x1, y1, _, _ = self.get_widget_bbox(closest_label)
            x2, y2, _, _ = self.get_widget_bbox(self.drag_data['widget'])

            # Calculate the distances from the current label to the closest label's borders
            distances = {
                'top': abs(y1 - y2),
                'bottom': abs(y1 - (y2 + closest_label.winfo_height())),
                'left': abs(x1 - x2),
                'right': abs(x1 - (x2 + closest_label.winfo_width()))
            }

            # Find the minimum distance and snap to the corresponding border
            min_distance = min(distances.values())

            if min_distance == distances['top']:
                self.drag_data['widget'].place(x=x2, y=y1)
            elif min_distance == distances['bottom']:
                self.drag_data['widget'].place(x=x2, y=y1 + closest_label.winfo_height() - self.drag_data['widget'].winfo_height())
            elif min_distance == distances['left']:
                self.drag_data['widget'].place(x=x1, y=y2)
            else:
                self.drag_data['widget'].place(x=x1 + closest_label.winfo_width() - self.drag_data['widget'].winfo_width(), y=y2)

    def get_widget_bbox(self, widget):
        x = widget.winfo_x()
        y = widget.winfo_y()
        width = widget.winfo_width()
        height = widget.winfo_height()
        return x, y, x + width, y + height

if __name__ == '__main__':
    root = tk.Tk()
    app = DragDropApp(root)
    root.mainloop()