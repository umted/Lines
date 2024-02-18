"""Файл реализующий графическую версию программы"""

from PyQt5 import QtCore, QtGui, QtWidgets

from core_mp import Field, FieldFullException
from driver import *


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
        self.name_label = self._create_label("Введите имя первого игрока:")
        self.name_label.setStyleSheet('''color:white;''')
        self.name_line_edit = QtWidgets.QLineEdit(self)
        self.name_line_edit.textChanged[str].connect(self.set_player_name)
        self.name_line_edit.setText("Игрок")
        self.name_line_edit.setMaxLength(10)

        self.name_label2 = self._create_label("Введите имя второго игрока:")
        self.name_label2.setStyleSheet('''color:white;''')
        self.name_line_edit2 = QtWidgets.QLineEdit(self)
        self.name_line_edit2.textChanged[str].connect(self.set_player_name2)
        self.name_line_edit2.setText("Игрок 2")
        self.name_line_edit2.setMaxLength(10)

        self.button_ok = QtWidgets.QPushButton("Ок", self)
        self.empty_label = self._create_label("")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_line_edit)
        layout.addWidget(self.name_label2)
        layout.addWidget(self.name_line_edit2)
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
    
    def set_player_name2(self):
        """Установка имени игрока"""
        self.parameters["name2"] = self.name_line_edit2.text()



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

        score_lcd2 = QtWidgets.QLCDNumber(self)
        score_lcd2.setSegmentStyle(QtWidgets.QLCDNumber.Filled)

        self.game_board.score_changed[int].connect(score_lcd.display)
        self.game_board.score2_changed[int].connect(score_lcd2.display)
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
        
        player_score = self._create_label(f"Счёт {self.game_board.game_field.player}")
        self.game_board.player_name[str].connect(lambda x: player_score.setText(f"Счёт {x}"))
        layout.addWidget(player_score, 4, 51, 1, 15)
        layout.addWidget(score_lcd, 6, 51, 7, 15)
        
        player2_score = self._create_label(f"Счёт {self.game_board.game_field.player2}")
        self.game_board.player2_name[str].connect(lambda x: player2_score.setText(f"Счёт {x}"))
        layout.addWidget(player2_score, 14, 51, 1, 15)
        layout.addWidget(score_lcd2, 16, 51, 7, 15)

        player_turn_text = self._create_label("")
        layout.addWidget(player_turn_text, 28, 51, 3, 15)
        self.game_board.player_changed[str].connect(lambda x: player_turn_text.setText(f"Ход: {x}"))

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
        player_name2 = self.parameters["name2"]
        if player_name is not None or player_name != "":
            if player_name2 is not None or player_name2 != "":
                self.game_board.game_field = Field(size, player=player_name, player2=player_name2)
            else:
                self.game_board.game_field = Field(size, player=player_name)
        else:
            if player_name2 is not None or player_name2 != "":
                self.game_board.game_field = Field(size, player2=player_name2)
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
        except GetRecordsError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", " Невозможно показать таблицу рекордов ", QtWidgets.QMessageBox.Ok)
        else:
            self.record_table.show()


class GameBoard(QtWidgets.QWidget):
    """Игровое поле в приложении"""
    score_changed = QtCore.pyqtSignal(int)
    score2_changed = QtCore.pyqtSignal(int)
    player_changed = QtCore.pyqtSignal(str)
    player_name = QtCore.pyqtSignal(str)
    player2_name = QtCore.pyqtSignal(str)

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
        self.score2_changed.emit(self.game_field.score2)
        self.player_changed.emit(self.game_field.player if self.game_field.first_player_move else self.game_field.player2)
        self.player_name.emit(self.game_field.player)
        self.player2_name.emit(self.game_field.player2)

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
                                    self.score2_changed.emit(self.game_field.score2)
                                    self.player_changed.emit(self.game_field.player if self.game_field.first_player_move else self.game_field.player2)

                        else:
                            self.game_field.delete_full_lines(find_lines)
                            self.score_changed.emit(self.game_field.score)
                            self.score2_changed.emit(self.game_field.score2)
                            self.player_changed.emit(self.game_field.player if self.game_field.first_player_move else self.game_field.player2)
                        self.coordinates = None
                        self.player_changed.emit(self.game_field.player if self.game_field.first_player_move else self.game_field.player2)

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
            add_record(self.game_field.player2, self.game_field.score2)
            win_text = (f"Победил: {self.game_field.player if self.game_field.score > self.game_field.score2 else self.game_field.player2}\n" \
                        if self.game_field.score != self.game_field.score2 else "Ничья\n")+\
                            f"{self.game_field.player} набрал: {self.game_field.score} очков.\n{self.game_field.player2} набрал: {self.game_field.score2} очков.\n"
            QtWidgets.QMessageBox.information(self, "Game Over",
                                              win_text+
                                              "Игра будет перезапущена",
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
