import tkinter as tk

# Janela para seleção da área
class SeletorArea:
    def __init__(self):
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
        print(f"Área selecionada: ({x1}, {y1}) até ({x2}, {y2})")

        self.root.destroy()

    def run(self):
        self.root.mainloop()

# Janela principal com botão
def abrir_janela_selecao():
    root.destroy()  # Fecha a janela principal
    seletor = SeletorArea()
    seletor.run()

# Janela principal
root = tk.Tk()
root.title("Ferramenta de Seleção de Área")
root.geometry("300x150")

label = tk.Label(root, text="Clique no botão para selecionar uma área:", font=("Arial", 10))
label.pack(pady=20)

botao = tk.Button(root, text="Selecionar Área", command=abrir_janela_selecao, font=("Arial", 12))
botao.pack(pady=10)

root.mainloop()
