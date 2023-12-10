import tkinter as tk

class DragDropApp:
    def __init__(self, root):
        self.root = root
        self.drag_data = {'x': 0, 'y': 0, 'widget': None}

        self.create_widgets()

    def create_widgets(self):
        self.draggable_label = tk.Label(
            self.root, text='Drag me!', bg='lightblue', padx=10, pady=5
        )
        self.draggable_label.pack()

        # Bind mouse events to the draggable label
        self.draggable_label.bind('<Button-1>', self.on_drag_start)
        self.draggable_label.bind('<B1-Motion>', self.on_drag_motion)
        self.draggable_label.bind('<ButtonRelease-1>', self.on_drag_release)

    def on_drag_start(self, event):
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['widget'] = event.widget

    def on_drag_motion(self, event):
        # Calculate the distance moved by the mouse
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']

        # Move the widget based on the mouse movement
        widget = self.drag_data['widget']
        widget.place(x=widget.winfo_x() + dx, y=widget.winfo_y() + dy)

    def on_drag_release(self, event):
        self.drag_data['widget'] = None

if __name__ == '__main__':
    root = tk.Tk()
    app = DragDropApp(root)
    root.mainloop()