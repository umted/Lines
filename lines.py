"""Файл реализующий графическую версию программы"""
import sys

from core import Field, FieldFullException
from driver import *
from PyQt5 import QtWidgets, QtCore, QtGui



class MainMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.setWindowTitle('Lines')
        self.setFixedSize(200, 100)
        self.central_widget = QtWidgets.QWidget()
        self.window = None
        self.rules = None
        self.setCentralWidget(self.central_widget)
        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.central_widget.setLayout(self.buttons_layout)
        self.start_game_button = QtWidgets.QPushButton()
        self.start_game_button.setText('Начать игру')
        self.start_game_button.clicked.connect(self.start_game)
        self.rules_button = QtWidgets.QPushButton()
        self.rules_button.setText('Правила игры')
        self.rules_button.clicked.connect(self.show_rules)
        self.exit_button = QtWidgets.QPushButton()
        self.exit_button.setText('Выход')
        self.exit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.buttons_layout.addWidget(self.start_game_button)
        self.buttons_layout.addWidget(self.rules_button)
        self.buttons_layout.addWidget(self.exit_button)

    def start_game(self):
        self.hide()
        self.window = Window()
        self.window.show()

    def show_rules(self):
        self.rules = RulesDialog()
        self.hide()
        self.rules.exec_()
        self.show()


class RulesDialog(QtWidgets.QDialog):

    def __init__(self):
        super(RulesDialog, self).__init__()
        self.setWindowTitle('Правила')
        self.widget = QtWidgets.QLabel(self)
        self.widget.setStyleSheet('''color:white;''')
        self.widget.setText('''        На поле размером 9x9 (стандартный размер) каждый ход появляются 3\n
        шара разных цветов (всего девять цветов). Из них нужно составлять линии\n
        одного цвета в пять и более штук по горизонтали, вертикали\n
        или диагонали. За один ход можно переместить\n
        только один шар и путь между начальной и конечной\n
        позициями должен быть свободен. Путь считается\n
        свободным, если состоит из одного или нескольких\n
        перемещений шара на одну клетку по вертикали или\n
        горизонтали, но не диагонали. Если после\n
        перемещения шара образуется линия одного цвета\n
        длиной 5 и более шаров, то она уничтожается, игроку\n
        начисляются очки и появление трёх следующих\n
        шаров откладывается до следующего хода.\n''')
        back_button = QtWidgets.QPushButton("Назад", self)
        back_button.setToolTip("Вернуться в главное меню")
        back_button.setFocusPolicy(QtCore.Qt.NoFocus)
        back_button.clicked.connect(self.close)
        back_button.move(350, 250)
        self.setFixedSize(500, 350)
        



class StartDialog(QtWidgets.QDialog):
    """Начать диалог для настройки"""

    def __init__(self):
        super().__init__()
        self.parameters = {'size':9}
        self._init_dialog()

    def _init_dialog(self):
        """Диалоговое окно инициализации"""
        self.setWindowTitle("Настройки")
        layout = QtWidgets.QVBoxLayout(self)
        self.name_label = self._create_label("Введите своё имя:")
        self.name_label.setStyleSheet('''color:white;''')
        self.name_line_edit = QtWidgets.QLineEdit(self)
        self.name_line_edit.textChanged[str].connect(self.set_player_name)
        self.name_line_edit.setText("Игрок")
        self.name_line_edit.setMaxLength(10)
        self.button_ok = QtWidgets.QPushButton("Ок", self)
        self.empty_label = self._create_label("")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.button_ok)
        self.setLayout(layout)

    def _create_label(self, text):
        """Создание текстовой метки"""
        label = QtWidgets.QLabel(text, self)
        label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        return label

    def set_player_name(self):
        """Установка имени игрока"""
        self.parameters["name"] = self.name_line_edit.text()



class Window(QtWidgets.QWidget):
    """Главное окно"""

    def __init__(self):
        super().__init__()
        self.start_dialog = StartDialog()
        self.game_board = GameBoard(self)
        self.start_dialog.button_ok.clicked.connect(self._new_game)
        self.record_table = RecordTable()
        self.record_table.ok_button.clicked.connect(self.record_table.hide)
        self.record_table.hide()
        self._init_window()
        self.start_dialog.exec_()

    def _init_window(self):
        """Инициализация окна приложения"""
        self.setWindowTitle('Lines')
        self.setFixedSize(700, 520)
        self._center()
        self.game_board.move(0, 0)
        layout = QtWidgets.QGridLayout()
        score_lcd = QtWidgets.QLCDNumber(self)
        score_lcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.game_board.score_changed[int].connect(score_lcd.display)
        quit_button = QtWidgets.QPushButton("Выход", self)
        quit_button.setToolTip("Quit the game")
        quit_button.setFocusPolicy(QtCore.Qt.NoFocus)
        quit_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        restart_button = QtWidgets.QPushButton("Перезапустить", self)
        restart_button.setToolTip("Restart the game with start parameters")
        restart_button.setFocusPolicy(QtCore.Qt.NoFocus)
        restart_button.clicked.connect(self._restart_game)
        record_button = QtWidgets.QPushButton("Рекорды", self)
        record_button.setToolTip("Show table of records")
        record_button.setFocusPolicy(QtCore.Qt.NoFocus)
        record_button.clicked.connect(self._show_record)
        layout.addWidget(self._create_label("Счёт"), 4, 51, 1, 15)
        layout.addWidget(score_lcd, 6, 51, 7, 15)
        layout.addWidget(restart_button, 44, 51, 3, 15)
        layout.addWidget(quit_button, 47, 51, 3, 15)
        layout.addWidget(record_button, 24, 51, 3, 15)
        layout.addWidget(self.game_board, 0, 0, 50, 50)
        self.setLayout(layout)

    def _create_label(self, text):
        """Создание текстовой метки"""
        label = QtWidgets.QLabel(text, self)
        label.setStyleSheet('''color:white;''')
        label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        return label

    def _center(self):
        """Установка приложения по центру"""
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def _new_game(self):
        """Создание новой игры"""
        self.hide()
        self.start_dialog.close()
        self.parameters = self.start_dialog.parameters
        size = self.parameters["size"]
        player_name = self.parameters["name"]
        if player_name is not None or player_name != "":
            self.game_board.game_field = Field(size, player_name)
        else:
            self.game_board.game_field = Field(size)
        self.game_board.new_game()
        self.update()
        self.show()

    def _restart_game(self):
        """Перезапуск игры с равными параметрами"""
        self.game_board.new_game()
        self.update()

    def _show_record(self):
        try:
            self.record_table.fill_record_table()
        except GetRecordsError as exception:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f" Невозможно показать таблицу рекордов ", QtWidgets.QMessageBox.Ok)
        else:
            self.record_table.show()


class GameBoard(QtWidgets.QWidget):
    """Игровое поле в приложении"""
    score_changed = QtCore.pyqtSignal(int)

    def __init__(self, perent, *params):
        """Инициализация объекта Игровое поле"""
        super().__init__(perent)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFixedSize(500, 500)
        self.game_field = Field(*params)
        self.coordinates = None  # Used in Mouse Event

    def get_square_width(self):
        """Получение ширины клетки игрового поля"""
        return self.width() // self.game_field.width

    def get_square_height(self):
        """Получение высоты клетки игрового поля"""
        return self.height() // self.game_field.height

    def new_game(self):
        """Начать новую игру"""
        self.game_field.refresh_field()
        self.score_changed.emit(self.game_field.score)

    def draw_blank_cell(self, painter, x, y):
        """Нарисуйте пустую ячейку"""
        painter.fillRect(x + 1, y + 1, self.get_square_width() - 2,
                         self.get_square_height() - 2, QtGui.QColor('#686868'))

    def draw_ball(self, painter, x, y, ball):
        """Рисуем цветной шар"""
        color_table = [0x14D100, 0xFFFF00, 0xFFAE00, 0xFF1800, 0xD0006E,
                       0x3016B0, 0x01939A, 0xCD0074, 0x00AC6B, 0xAEF100]
        color_table_2 = [0x4AE83A, 0xFBFE72, 0xFFC340, 0xFF5240, 0xE73A95,
                         0x624AD8, 0x34C6CD, 0xE6399B, 0x35D699, 0xC4F83E]
        if not ball.selected:
            color_1 = QtGui.QColor(color_table[ball.color - 1])
            color_2 = QtGui.QColor(color_table_2[ball.color - 1])
        else:
            color_1 = QtGui.QColor(color_table_2[ball.color - 1])
            color_2 = QtGui.QColor(color_table[ball.color - 1])
        pen = QtGui.QPen()
        pen.setColor(color_1)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(color_2)
        painter.drawEllipse(x + 4, y + 4, self.get_square_width() - 8, self.get_square_height() - 8)

    def paintEvent(self, event):
        """Событие рисования"""
        painter = QtGui.QPainter(self)
        rect = self.contentsRect()
        board_top = rect.bottom() - self.game_field.height * self.get_square_height()
        for x in range(self.game_field.height):
            for y in range(self.game_field.width):
                self.draw_blank_cell(painter, rect.left() + y * self.get_square_width(),
                                     board_top + x * self.get_square_height())
                ball = self.game_field.field[x][y]
                if ball is not None:
                    self.draw_ball(painter, rect.left() + y * self.get_square_width(),
                                   board_top + x * self.get_square_height(), ball)

    def mousePressEvent(self, event):
        """Событие нажатия мышки"""
        try:
            y = event.y() // self.get_square_width()
            x = event.x() // self.get_square_height()
            if x < 0 or x >= self.game_field.height or y < 0 or y >= self.game_field.width:
                return

            if self.game_field.get_ball(x, y) is None:
                if self.coordinates is not None:
                    if self.game_field.try_move(self.coordinates[0], self.coordinates[1], x, y):
                        self.game_field.make_step(self.coordinates[0], self.coordinates[1], x, y)
                        find_lines = self.game_field.find_full_lines(x, y)
                        if find_lines is None:
                            self.game_field.set_next_balls()
                            for coordinates in self.game_field.set_balls:
                                array = self.game_field.find_full_lines(coordinates[0], coordinates[1])
                                if array is not None:
                                    self.game_field.delete_full_lines(array)
                                    self.score_changed.emit(self.game_field.score)
                        else:
                            self.game_field.delete_full_lines(find_lines)
                            self.score_changed.emit(self.game_field.score)
                        self.coordinates = None
            else:
                if self.coordinates is None:
                    self.game_field.get_ball(x, y).selected = True
                    self.coordinates = (x, y)
                else:
                    if self.coordinates == (x, y):
                        self.game_field.get_ball(x, y).selected = False
                        self.coordinates = None
                    else:
                        self.game_field.get_ball(x, y).selected = True
                        self.game_field.get_ball(self.coordinates[0], self.coordinates[1]).selected = False
                        self.coordinates = (x, y)
            self.update()
        except FieldFullException:
            add_record(self.game_field.player, self.game_field.score)
            QtWidgets.QMessageBox.information(self, "Game Over",
                                              f"{self.game_field.player}, ты набрал: {self.game_field.score} очков.\n"
                                              f"Игра будет перезапущена",
                                              QtWidgets.QMessageBox.Ok)
            self.coordinates = None
            self.new_game()


class RecordTable(QtWidgets.QWidget):
    """Запись класса таблицы"""

    def __init__(self):
        """Инициализация класса"""
        super().__init__()
        self._init_table()

    def _init_table(self):
        """Инициализация виджетов в таблице записей"""
        self.setWindowTitle('Рекорды')
        self.setFixedSize(240, 335)
        layout = QtWidgets.QVBoxLayout(self)
        self.title_label = QtWidgets.QLabel("Таблица рекордов", self)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.record_table = QtWidgets.QTableWidget(self)
        self.record_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.record_table.setRowCount(8)
        self.record_table.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem("Имя игрока")
        self.record_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem("Счёт")
        self.record_table.setHorizontalHeaderItem(1, item)
        self.record_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ok_button = QtWidgets.QPushButton("Ок", self)
        self.ok_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        layout.addWidget(self.title_label)
        layout.addWidget(self.record_table)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def fill_record_table(self):
        """Заполнение таблицы рекордов"""
        records = get_records()
        counter = 0
        for record in records.items():
            text_item = QtWidgets.QTableWidgetItem(record[0])
            text_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.record_table.setItem(counter, 0, text_item)
            number_item = QtWidgets.QTableWidgetItem(f"{record[1]}")
            number_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.record_table.setItem(counter, 1, number_item)
            counter += 1


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    palette = QtGui.QPalette()
    palette.setColor(QtWidgets.QWidget().backgroundRole(), QtGui.QColor('#4a4a4a'))
    app.setPalette(palette)
    lines = MainMenu()
    lines.show()
    sys.exit(app.exec_())
