import sys
import win32gui, win32ui, win32con, win32api
from PIL import ImageGrab, Image
from PyQt5 import QtWidgets, QtGui, QtCore
import ctypes
from ctypes import wintypes

# Constants do Win32
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
LWA_ALPHA = 0x00000002


def make_window_clickthrough(hwnd):
    # adiciona WS_EX_LAYERED | WS_EX_TRANSPARENT
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ex_style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style)
    # mantém opacidade original (se você quiser ajustar só aqui)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA)


# Captura de janelas RDP via BitBlt com fallback

def capture_window(hwnd):
    try:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        w, h = right - left, bottom - top
        if w == 0 or h == 0:
            return None
        hdc = win32gui.GetWindowDC(hwnd)
        mfc = win32ui.CreateDCFromHandle(hdc)
        save_dc = mfc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(mfc, w, h)
        save_dc.SelectObject(bmp)
        save_dc.BitBlt((0, 0), (w, h), mfc, (0, 0), win32con.SRCCOPY)
        bits = bmp.GetBitmapBits(True)
        info = bmp.GetInfo()
        img = Image.frombuffer('RGB', (info['bmWidth'], info['bmHeight']), bits, 'raw', 'BGRX', 0, 1)
        win32gui.DeleteObject(bmp.GetHandle());
        save_dc.DeleteDC();
        mfc.DeleteDC();
        win32gui.ReleaseDC(hwnd, hdc)
        return img
    except:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        return ImageGrab.grab().crop((left, top, right, bottom))


# Lista janelas RDP ativas pelos títulos

def get_rdp_windows():
    wins = []

    def cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if any(sub in title for sub in ['Área de Trabalho Remota', 'Conexão', 'Remote Desktop']):
                wins.append((hwnd, title))

    win32gui.EnumWindows(cb, None)
    return wins


# Traz janela para frente

def bring_to_front(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    except:
        pass


# Obtém área de trabalho do monitor primário

def get_primary_monitor_work_area():
    work = None
    MONPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HMONITOR, wintypes.HDC,
                                 ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)

    def _cb(hMon, hdcMon, lprcMon, lParam):
        info = win32api.GetMonitorInfo(hMon)
        if info.get('Flags', 0) & 1:
            nonlocal work
            work = info['Work']
        return True

    ctypes.windll.user32.EnumDisplayMonitors(0, 0, MONPROC(_cb), 0)
    if work:
        return work
    return (0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))


class RDPPreviewWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # Configurações da janela: sem bordas, sempre no topo, tool window
        flags = QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Opacidade e tornar clique-through todo o widget
        self.setWindowOpacity(0.90)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        # Layout em grid
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setSpacing(5)
        self.labels = {}

        # Timer de atualização
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_previews)
        self.timer.start(2000)

        self.update_previews()

    def update_previews(self):
        windows = get_rdp_windows()
        # Remove fechadas
        for hwnd in list(self.labels):
            if hwnd not in [h for h, _ in windows]:
                lbl = self.labels.pop(hwnd)
                lbl.deleteLater()
        # Atualiza/cria
        for idx, (hwnd, title) in enumerate(windows):
            if idx >= 9: break
            img = capture_window(hwnd)
            if not img: continue
            thumb = img.resize((200, 120))
            data = thumb.convert('RGB').tobytes()
            qimg = QtGui.QImage(data, thumb.width, thumb.height, thumb.width * 3, QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap.fromImage(qimg)
            if hwnd in self.labels:
                lbl = self.labels[hwnd]
                lbl.setPixmap(pix)
            else:
                row, col = divmod(idx, 3)

                class ClickableLabel(QtWidgets.QLabel):
                    def __init__(self, hwnd, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        self.hwnd = hwnd

                    def mousePressEvent(self, event):
                        bring_to_front(self.hwnd)

                # Dentro de update_previews:
                lbl = ClickableLabel(hwnd, self)
                lbl.setPixmap(pix)
                lbl.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))  # opcional
                self.layout.addWidget(lbl, row, col)
                self.labels[hwnd] = lbl

        # Posiciona no canto superior direito do monitor primário
        left, top, right, bottom = get_primary_monitor_work_area()
        w = 3 * 200 + 2 * 5
        h = ((len(windows) + 2) // 3) * 120 + (((len(windows) + 2) // 3) - 1) * 5
        x = right - w - 10
        y = top + 10
        self.setGeometry(x, y, w, h)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = RDPPreviewWidget()
    widget.show()

    sys.exit(app.exec_())