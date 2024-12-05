#pip install PyQt5
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QSlider, QCheckBox, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class CrosshairApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Crosshair | Sommer")
        self.setGeometry(100, 100, 400, 150)

        self.set_discord_theme()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.size_label = QLabel(f"Størrelse: 16")
        self.size_label.setFont(QFont("Arial", 12))
        self.size_label.setStyleSheet("color: #ffffff;")
        self.size_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.size_label)

        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(100)
        self.size_slider.setValue(16)
        self.size_slider.setTickInterval(1)
        self.size_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                height: 4px;
                background: #5e626b;
                border: none;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                width: 16px;
                height: 16px;
                background: #36a0c9;
                border: none;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #0055ff;
                border-radius: 2px;
            }
            """
        )
        self.size_slider.valueChanged.connect(self.update_crosshair_size)
        self.layout.addWidget(self.size_slider)

        self.checkbox = QCheckBox("Tænd/sluk Crosshair")
        self.checkbox.setChecked(True)
        self.checkbox.setFont(QFont("Arial", 10))
        self.checkbox.setStyleSheet(
            """
            QCheckBox {
                color: #ffffff;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid ad262d;
                background: #ad262d;
            }
            QCheckBox::indicator:checked {
                background: #26ad36;
                border: 1px solid #26ad36;
            }
            """
        )
        self.checkbox.stateChanged.connect(self.toggle_crosshair)
        self.layout.addWidget(self.checkbox)

        self.crosshair = QLabel()
        self.crosshair.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.crosshair.setAttribute(Qt.WA_TranslucentBackground)

        self.crosshair_size = 16
        crosshair_path = resource_path("crosshair.png")
        self.pixmap = QPixmap(crosshair_path)
        if self.pixmap.isNull():
            print(f"Fejl: Kunne ikke indlæse billedet fra {crosshair_path}")
        else:
            self.update_crosshair_size(self.crosshair_size)

        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_rect = screen.geometry()
        self.x_pos = (screen_rect.width() - self.crosshair_size) // 2
        self.y_pos = (screen_rect.height() - self.crosshair_size) // 2
        self.update_crosshair_geometry()

        self.crosshair.show()

    def set_discord_theme(self):
        self.setStyleSheet(
        """
        QMainWindow {
            background-color: #2f3136;
        }
        QLabel {
            color: #ffffff;
            font-size: 14px;
        }
        """
    )

    def update_crosshair_size(self, size):
        if isinstance(size, int):
            self.crosshair_size = size
        else:
            self.crosshair_size = self.size_slider.value()

        if not self.pixmap.isNull():
            self.crosshair.setPixmap(self.pixmap.scaled(self.crosshair_size, self.crosshair_size))

        self.size_label.setText(f"Størrelse: {self.crosshair_size}")

        self.update_crosshair_geometry()

    def update_crosshair_geometry(self):
        self.x_pos = (QApplication.instance().primaryScreen().geometry().width() - self.crosshair_size) // 2
        self.y_pos = (QApplication.instance().primaryScreen().geometry().height() - self.crosshair_size) // 2
        self.crosshair.setGeometry(self.x_pos, self.y_pos, self.crosshair_size, self.crosshair_size)

    def toggle_crosshair(self, state):
        if state == Qt.Checked:
            self.crosshair.show()
        else:
            self.crosshair.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CrosshairApp()
    window.show()
    sys.exit(app.exec_())
