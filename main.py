import subprocess
import tkinter as tk
from tkinter import messagebox

def conectar_rdp():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    hosts = [entry_host1.get(), entry_host2.get(), entry_host3.get(), entry_host4.get()]

    if not all([usuario, senha] + hosts):
        messagebox.showerror("Erro", "Preencha todos os campos.")
        return

    for host in hosts:
        # Salva a credencial temporariamente
        subprocess.call(f'cmdkey /generic:{host} /user:{usuario} /pass:{senha}', shell=True)
        # Abre o RDP
        subprocess.Popen(["mstsc", "/v:" + host])

# --- Interface gráfica ---
root = tk.Tk()
root.title("Conexões RDP")

tk.Label(root, text="Usuário:").grid(row=0, column=0)
entry_usuario = tk.Entry(root, width=30)
entry_usuario.grid(row=0, column=1)

tk.Label(root, text="Senha:").grid(row=1, column=0)
entry_senha = tk.Entry(root, width=30, show="*")
entry_senha.grid(row=1, column=1)

tk.Label(root, text="Endereço RDP 1:").grid(row=2, column=0)
entry_host1 = tk.Entry(root, width=30)
entry_host1.grid(row=2, column=1)

tk.Label(root, text="Endereço RDP 2:").grid(row=3, column=0)
entry_host2 = tk.Entry(root, width=30)
entry_host2.grid(row=3, column=1)

tk.Label(root, text="Endereço RDP 3:").grid(row=4, column=0)
entry_host3 = tk.Entry(root, width=30)
entry_host3.grid(row=4, column=1)

tk.Label(root, text="Endereço RDP 4:").grid(row=5, column=0)
entry_host4 = tk.Entry(root, width=30)
entry_host4.grid(row=5, column=1)

btn_conectar = tk.Button(root, text="Conectar RDPs", command=conectar_rdp)
btn_conectar.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
