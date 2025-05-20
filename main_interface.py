from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QApplication, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import subprocess
import sys


class SalvagingUI(QWidget):
    def __init__(self):
        self.selected_areas = {
            "area1": None,
            "area2": None,
            "area3": None
        }
        self.selected_areas = {}

        super().__init__()
        self.setWindowTitle("Controle de Salvaging")
        self.setGeometry(100, 100, 350, 320)
        self.setStyleSheet("background-color: #f4f4f4;")

        self.running = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Título
        title = QLabel("Painel de Controle")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(10)

        # Quantidade de Módulos
        self.module_spin = QSpinBox()
        self.module_spin.setRange(1, 10)
        layout.addLayout(self._build_labeled_input("Quantidade de Módulos:", self.module_spin))

        # Quantidade de Targets
        self.target_spin = QSpinBox()
        self.target_spin.setRange(1, 10)
        layout.addLayout(self._build_labeled_input("Quantidade de Targets:", self.target_spin))

        # Linha separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Botões para selecionar áreas
        button_layout = QHBoxLayout()
        self.area1_btn = QPushButton("Selecionar Área 1")
        self.area2_btn = QPushButton("Selecionar Área 2")
        self.area3_btn = QPushButton("Selecionar Área 3")

        for btn in [self.area1_btn, self.area2_btn, self.area3_btn]:
            btn.setStyleSheet("background-color: #d0e8ff; padding: 5px; font-weight: bold;")

        self.area1_btn.clicked.connect(lambda: self.select_area("area1"))
        self.area2_btn.clicked.connect(lambda: self.select_area("area2"))
        self.area3_btn.clicked.connect(lambda: self.select_area("area3"))

        button_layout.addWidget(self.area1_btn)
        button_layout.addWidget(self.area2_btn)
        button_layout.addWidget(self.area3_btn)
        layout.addLayout(button_layout)

        layout.addSpacing(15)

        # Status
        self.status_label = QLabel("Status: 🔴 Parado")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def _build_labeled_input(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(150)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def select_area(self, area_name):
        print(f"Iniciando seleção para {area_name}")
        result = subprocess.run(
            ["python", "seletor_area.py"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            try:
                x, y, w, h = map(int, result.stdout.strip().split(","))
                self.selected_areas[area_name] = {"x": x, "y": y, "width": w, "height": h}
                print(f"Área {area_name} definida:", self.selected_areas[area_name])
            except Exception as e:
                print("Erro ao interpretar coordenadas:", e)
        else:
            print("Erro ao executar seletor_area.py")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F8:
            self.running = not self.running
            if self.running:
                self.status_label.setText("Status: 🟢 Executando")
                self.status_label.setStyleSheet("color: green;")
            else:
                self.status_label.setText("Status: 🔴 Parado")
                self.status_label.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SalvagingUI()
    window.show()
    sys.exit(app.exec_())
