# seletor_area.py
import tkinter as tk
import sys
import json

class SeletorArea:
    def __init__(self, output_file):
        self.output_file = output_file
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.config(bg='black')
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.canvas = tk.Canvas(self.root, cursor="cross", bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        x1 = int(min(self.start_x, end_x))
        y1 = int(min(self.start_y, end_y))
        x2 = int(max(self.start_x, end_x))
        y2 = int(max(self.start_y, end_y))

        coords = {
            "x": x1,
            "y": y1,
            "width": x2 - x1,
            "height": y2 - y1
        }

        with open(self.output_file, "w") as f:
            json.dump(coords, f, indent=4)

        print(f"Coordenadas salvas em {self.output_file}")
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    output_file = sys.argv[1] if len(sys.argv) > 1 else "area_default.json"
    seletor = SeletorArea(output_file)
    seletor.run()
