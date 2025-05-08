import flet as ft
import subprocess
import sys
import time

def main(page: ft.Page):
    page.title = "Selecionar Área"
    page.window_maximized = True

    def iniciar_captura(e):
        # Minimiza a janela do Flet
        page.window_minimized = True
        page.update()

        time.sleep(0.5)  # Aguarda um pouco para garantir que a janela minimizou

        try:
            result = subprocess.run(
                [sys.executable, "captura_area.py"],  # Execute o script de captura
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            output = result.stdout.strip() if result.stdout else "Erro: saída vazia"
            print(output)
        except Exception as err:
            print(f"Erro ao capturar área: {err}")

        time.sleep(0.5)  # A pausa após o processo de captura

        # Restaura a janela do Flet após a captura
        page.window_minimized = False
        page.update()

    page.add(
        ft.Column(
            [
                ft.Text("Clique abaixo para selecionar uma área da tela:"),
                ft.ElevatedButton("Selecionar Área", on_click=iniciar_captura),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.app(target=main)
