import tkinter as tk

def selecionar_area():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)
    root.config(cursor="cross")

    coords = {}

    def on_mouse_down(event):
        coords['x1'] = event.x
        coords['y1'] = event.y

    def on_mouse_up(event):
        coords['x2'] = event.x
        coords['y2'] = event.y
        print(f"Área selecionada: ({coords['x1']}, {coords['y1']}) até ({coords['x2']}, {coords['y2']})")
        root.destroy()

    canvas = tk.Canvas(root, bg='black')
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.bind("<Button-1>", on_mouse_down)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

if __name__ == "__main__":
    selecionar_area()
