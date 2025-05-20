from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QSpinBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controle de Salvaging")
        self.setGeometry(100, 100, 320, 280)

        self.running = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Quantidade de Módulos
        self.module_spin = QSpinBox()
        self.module_spin.setRange(1, 10)
        layout.addLayout(self._build_labeled_input("Quantidade de Módulos:", self.module_spin))

        # Quantidade de Targets
        self.target_spin = QSpinBox()
        self.target_spin.setRange(1, 10)
        layout.addLayout(self._build_labeled_input("Quantidade de Targets:", self.target_spin))

        # Botões para selecionar áreas
        self.area1_btn = QPushButton("Selecionar Área 1")
        self.area2_btn = QPushButton("Selecionar Área 2")
        self.area3_btn = QPushButton("Selecionar Área 3")

        self.area1_btn.clicked.connect(lambda: self.select_area("area1"))
        self.area2_btn.clicked.connect(lambda: self.select_area("area2"))
        self.area3_btn.clicked.connect(lambda: self.select_area("area3"))

        layout.addWidget(self.area1_btn)
        layout.addWidget(self.area2_btn)
        layout.addWidget(self.area3_btn)

        # Status
        self.status_label = QLabel("Status: 🔴 Parado")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def _build_labeled_input(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def select_area(self, area_name):
        # Aqui você integrará seu script para capturar coordenadas
        print(f"Selecionando coordenadas para: {area_name}")
        # Exemplo de coordenadas simuladas
        coords = {"x": 100, "y": 100, "width": 300, "height": 200}
        # Salva em um arquivo separado
        with open(f"{area_name}.json", "w") as f:
            import json
            json.dump(coords, f, indent=4)
        print(f"Coordenadas salvas em {area_name}.json")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F8:
            self.running = not self.running
            if self.running:
                self.status_label.setText("Status: 🟢 Executando")
            else:
                self.status_label.setText("Status: 🔴 Parado")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
