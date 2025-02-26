from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QPushButton, QLabel, QHBoxLayout, QTimeEdit
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QTextCharFormat, QColor

class MyCalendar(QCalendarWidget):
    """ 날짜 범위를 선택할 수 있는 QCalendarWidget (하이라이트 포함) """
    def __init__(self):
        super().__init__()
        self.begin_date = None
        self.end_date = None
        self.click_count = 0
        self.default_format = QTextCharFormat()

        self.clicked.connect(self.date_is_clicked)

    def date_is_clicked(self, date):
        """ 날짜 클릭 시 동작 정의 (시작 날짜와 끝 날짜를 선택) """
        self.click_count += 1

        if self.click_count % 2 == 1:  # 첫 번째 클릭 (시작 날짜 선택)
            self.begin_date = date
            self.end_date = None
            self.highlight_range()
        else:  # 두 번째 클릭 (종료 날짜 선택)
            self.end_date = date
            self.highlight_range()

    def highlight_range(self):
        """ 선택한 날짜 범위를 하이라이트로 표시 """
        self.clear_highlight()

        if self.begin_date and not self.end_date:
            # 시작 날짜만 선택된 경우 (해당 날짜만 강조)
            fmt = QTextCharFormat()
            fmt.setBackground(QColor("lightblue"))
            self.setDateTextFormat(self.begin_date, fmt)

        elif self.begin_date and self.end_date:
            # 두 날짜 사이의 모든 날짜를 하이라이트
            start = min(self.begin_date, self.end_date)
            end = max(self.begin_date, self.end_date)

            fmt = QTextCharFormat()
            fmt.setBackground(QColor("lightblue"))

            current_date = start
            while current_date <= end:
                self.setDateTextFormat(current_date, fmt)
                current_date = current_date.addDays(1)

    def clear_highlight(self):
        """ 이전 하이라이트 제거 """
        self.setDateTextFormat(self.begin_date, self.default_format)
        if self.end_date:
            start = min(self.begin_date, self.end_date)
            end = max(self.begin_date, self.end_date)
            current_date = start
            while current_date <= end:
                self.setDateTextFormat(current_date, self.default_format)
                current_date = current_date.addDays(1)

class MyCalendarDialog(QDialog):
    """ 달력 창을 띄우고 선택한 날짜 및 시간을 반환하는 다이얼로그 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("날짜 선택")
        self.resize(400, 350)

        self.calendar = MyCalendar()

        # 시간 선택 위젯 추가
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        self.start_time_edit.setTime(QTime(0, 0, 0))

        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        self.end_time_edit.setTime(QTime(23, 59, 59))

        self.ok_button = QPushButton("확인")
        self.ok_button.clicked.connect(self.accept)

        # 레이아웃 설정
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("시작 시간:"))
        time_layout.addWidget(self.start_time_edit)
        time_layout.addWidget(QLabel("종료 시간:"))
        time_layout.addWidget(self.end_time_edit)

        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addLayout(time_layout)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_selected_datetime(self):
        """ 선택된 날짜 및 시간 반환 """
        if self.calendar.begin_date and self.calendar.end_date:
            start_date = self.calendar.begin_date.toString("yyyy-MM-dd")
            end_date = self.calendar.end_date.toString("yyyy-MM-dd")
            start_time = self.start_time_edit.time().toString("HH:mm:ss")
            end_time = self.end_time_edit.time().toString("HH:mm:ss")
            return f"{start_date} {start_time}", f"{end_date} {end_time}"
        return None, None
