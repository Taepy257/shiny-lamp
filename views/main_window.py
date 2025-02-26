import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QSplitter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject
from views.calendar_dialog import MyCalendarDialog  # ✅ 달력 다이얼로그 추가

class WebBridge(QObject):
    """ Python과 JavaScript 간 데이터 통신을 위한 브릿지 """
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot(float, float, float, float)
    def sendRectangleCoords(self, lat1, lng1, lat2, lng2):
        """ JavaScript에서 전달받은 좌표를 출력 """
        print(f"선택된 영역 좌표: ({lat1}, {lng1}) ~ ({lat2}, {lng2})")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sentinel SAR 데이터 분석 GUI")
        self.setGeometry(100, 100, 1200, 800)
        
         # 현재 파일(main_window.py)의 절대 경로에서 map.html의 절대 경로를 계산
        current_dir = os.path.dirname(os.path.abspath(__file__))  # main_window.py가 위치한 폴더
        map_path = os.path.join(current_dir, "map.html")  # map.html의 절대경로
        map_url = QUrl.fromLocalFile(map_path)  # QWebEngineView에서 로드할 URL

        # 전체 레이아웃을 위한 중앙 위젯 및 스플리터
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_splitter = QSplitter(Qt.Vertical)  # 상단(9)과 하단(1) 구분
        top_splitter = QSplitter(Qt.Horizontal)  # 좌(3)와 우(7) 구분

        # 좌측 프레임 (메뉴 버튼)
        left_frame = QWidget()
        left_layout = QVBoxLayout()
        self.create_menu_buttons(left_layout)
        left_frame.setLayout(left_layout)

        # 우측 프레임 (지도)
        self.right_frame = QWebEngineView()
        self.right_frame.setUrl(map_url)  # OpenStreetMap 로드
        
        # JavaScript와 Python을 연결할 WebChannel 설정
        self.channel = QWebChannel()
        self.bridge = WebBridge()
        self.channel.registerObject("pyBridge", self.bridge)
        self.right_frame.page().setWebChannel(self.channel)

        # 하단 프레임 (이벤트 로그)
        self.bottom_frame = QTextEdit()
        self.bottom_frame.setReadOnly(True)
        self.bottom_frame.setPlaceholderText("여기에 이벤트 메시지가 표시됩니다.")

        # 프레임을 스플리터에 추가
        top_splitter.addWidget(left_frame)
        top_splitter.addWidget(self.right_frame)
        top_splitter.setSizes([360, 840])  # 초기 비율 (3:7)

        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.bottom_frame)
        main_splitter.setSizes([720, 80])  # 초기 비율 (9:1)

        # 전체 레이아웃 적용
        layout = QVBoxLayout(central_widget)
        layout.addWidget(main_splitter)

    def create_menu_buttons(self, layout):
        """메뉴 버튼 생성"""
        buttons = [
            ("달력 실행", self.run_calendar),
            ("영역 선택", self.select_area),
            ("Sentinel SAR 다운로드", self.download_sar),
            ("AIS 데이터 다운로드", self.download_ais),
            ("선박 탐지 실행", self.detect_ships),
            ("AIS vs 탐지 데이터 비교", self.compare_data),
        ]

        for text, function in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(function)
            layout.addWidget(btn)

    def run_calendar(self):
        """ 달력 실행 버튼을 눌렀을 때 다이얼로그 표시 """
        dialog = MyCalendarDialog(self)
        if dialog.exec_():  # 다이얼로그 실행 후 결과 반환
            start_datetime, end_datetime = dialog.get_selected_datetime()
            if start_datetime and end_datetime:
                self.bottom_frame.append(f"선택된 기간: {start_datetime} ~ {end_datetime}")
            else:
                self.bottom_frame.append("날짜를 올바르게 선택하세요.")

    def select_area(self):
        """ JavaScript에 메시지를 보내어 영역 선택 기능을 활성화 """
        script = "alert('영역 선택 모드 활성화: 지도에서 두 지점을 클릭하세요.');"
        self.right_frame.page().runJavaScript(script)

    def download_sar(self):
        print("Sentinel SAR 다운로드")

    def download_ais(self):
        print("AIS 데이터 다운로드")

    def detect_ships(self):
        print("선박 탐지 실행")

    def compare_data(self):
        print("AIS vs 탐지 데이터 비교")
