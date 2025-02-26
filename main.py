import sys
from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow  # ✅ views 패키지 확인

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  # ✅ PyQt5에서는 exec()가 아니라 exec_() 사용
