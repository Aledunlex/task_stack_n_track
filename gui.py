import re

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QToolBar

from db_handler import update_quest_done

# One color per game region
BACKGROUND_COLORS = ['#e6194b', '#3cb44b', '#ffe119', '#0082c8',
                     '#f58231', '#911eb4', '#46f0f0', '#f032e6']


def get_text_color(bg_color):
    r, g, b = int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16)
    luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    return '#000000' if luminance > 0.5 else '#ffffff'


def highlight_search_text(text, search_text):
    if search_text is None:
        return text
    return re.sub(f'({re.escape(search_text)})', r'<span style="background-color: yellow;">\1</span>', text,
                  flags=re.IGNORECASE)


class App:
    def __init__(self, quests_by_region):
        super().__init__()
        self.dones_filter_checkbox = None
        self.window = None
        self.ui_colors = {}
        self.quests_by_region = quests_by_region
        self.init_ui()

    def init_ui(self):
        app = QtWidgets.QApplication([])
        window = self.window = QtWidgets.QMainWindow()
        window.setWindowTitle('Quest Viewer')
        window.showMaximized()

        # Create toolbar for the search functionality
        self.create_search_bar()

        # Toolbar for region buttons
        self.create_region_toolbar()

        # Create central widget
        central_widget = QtWidgets.QWidget()
        window.setCentralWidget(central_widget)

        # Show window
        window.show()
        app.exec_()

    def create_search_bar(self):
        window = self.window
        toolbar = window.addToolBar('Toolbar')
        # Create search bar
        search_bar = QtWidgets.QLineEdit()
        search_bar.setPlaceholderText('Search quests...')
        toolbar.addWidget(search_bar)
        # Create tag combo box
        tag_combo_box = QtWidgets.QComboBox()
        tag_combo_box.addItems(['title', 'reward', 'solution'])
        toolbar.addWidget(tag_combo_box)
        # Create dones filter checkbox
        self.dones_filter_checkbox = dones_filter_checkbox = QtWidgets.QCheckBox('Filter completed')
        dones_filter_checkbox.setChecked(True)
        toolbar.addWidget(dones_filter_checkbox)
        # Connect search bar and tag combo box signals
        search_bar.textChanged.connect(
            lambda text: self.search_quests(self.quests_by_region, text, tag_combo_box.currentText(),
                                            dones_filter_checkbox.isChecked()))
        tag_combo_box.currentTextChanged.connect(
            lambda text: self.search_quests(self.quests_by_region, search_bar.text(), text,
                                            dones_filter_checkbox.isChecked()))
        dones_filter_checkbox.stateChanged.connect(
            lambda state: self.search_quests(self.quests_by_region, search_bar.text(), tag_combo_box.currentText(),
                                             state == QtCore.Qt.Checked))

    def create_region_toolbar(self):
        window = self.window
        region_toolbar = QToolBar()
        region_toolbar.setIconSize(QSize(32, 32))
        window.addToolBarBreak()
        window.addToolBar(Qt.TopToolBarArea, region_toolbar)
        # Create a horizontal layout to hold the buttons
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)

        # Add the buttons to the layout
        for i, region in enumerate(sorted(self.quests_by_region.keys())):
            self.ui_colors[region] = BACKGROUND_COLORS[i]
            quests = self.quests_by_region[region]
            button = QtWidgets.QPushButton(region.replace('_', ' ').upper())
            btn_text_color = get_text_color(BACKGROUND_COLORS[i])
            button_style = """
            QPushButton {
                background-color: #COLOR;
                color: #TEXT;
                padding: 10px 20px;
                border-radius: 5px;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 16px;
            }""".replace('#COLOR', BACKGROUND_COLORS[i]).replace('#TEXT', btn_text_color)
            button.setStyleSheet(button_style.replace('#COLOR', BACKGROUND_COLORS[i]).replace('#TEXT', btn_text_color))
            button.clicked.connect(
                lambda checked, q=quests: self.view_quests_from(q, self.dones_filter_checkbox.isChecked()))
            hbox.addWidget(button)
        hbox.addStretch(1)
        # Create a widget to hold the layout and add it to the toolbar
        widget = QtWidgets.QWidget()
        widget.setLayout(hbox)
        region_toolbar.addWidget(widget)

    def view_quests_from(self, quests, filter_dones, search_text=None):
        central_widget = self.window.centralWidget()
        old_layout = central_widget.layout()
        if old_layout is not None:
            QtWidgets.QWidget().setLayout(old_layout)
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        scroll_area_widget = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_area_widget)
        scroll_area_layout = QtWidgets.QVBoxLayout()
        scroll_area_widget.setLayout(scroll_area_layout)

        for quest in quests:
            if filter_dones and quest.done:
                continue
            quest_widget = QtWidgets.QGroupBox()
            quest_widget.setStyleSheet('QGroupBox {background-color: beige; border-radius: 5px;}')
            quest_layout = QtWidgets.QHBoxLayout()
            quest_widget.setLayout(quest_layout)

            done_checkbox = QtWidgets.QCheckBox()
            done_checkbox.setFixedSize(32, 32)
            done_checkbox.setChecked(quest.done)
            done_checkbox.stateChanged.connect(lambda state, q=quest: update_quest_done(q, state))
            quest_layout.addWidget(done_checkbox)

            text_layout = QtWidgets.QVBoxLayout()
            quest_layout.addLayout(text_layout)

            title_label = QtWidgets.QLabel()
            title_label.setStyleSheet('font-size: 18px; font-weight: bold;')
            title_label.setAlignment(QtCore.Qt.AlignCenter)
            title_label.setWordWrap(True)
            title_label.setTextFormat(QtCore.Qt.RichText)
            title_label.setText(highlight_search_text(quest.title, search_text))
            text_layout.addWidget(title_label)

            reward_label = QtWidgets.QLabel()
            reward_label.setStyleSheet('font-style: italic;')
            reward_label.setWordWrap(True)
            reward_label.setTextFormat(QtCore.Qt.RichText)
            reward_label.setText(highlight_search_text(quest.reward, search_text))
            text_layout.addWidget(reward_label)

            solution_label = QtWidgets.QLabel()
            solution_label.setWordWrap(True)
            solution_label.setTextFormat(QtCore.Qt.RichText)
            solution_label.setText(highlight_search_text(quest.solution, search_text))
            text_layout.addWidget(solution_label)

            scroll_area_layout.addWidget(quest_widget)

        spacer_item = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        scroll_area_layout.addItem(spacer_item)

        central_widget.update()

    def search_quests(self, quests_by_region, search_text, search_tag, filter_dones):
        if not search_text:
            # quests by region is a dictionary of lists, so we need to flatten it
            all_quests = [quest for quests in quests_by_region.values() for quest in quests]
            self.view_quests_from(all_quests, filter_dones)
            return

        search_text = search_text.lower()
        matching_quests = []
        pattern = re.compile(search_text)
        for region, quests in quests_by_region.items():
            for quest in quests:
                if filter_dones and quest.done:
                    continue
                quest_text = getattr(quest, search_tag).lower()
                if pattern.search(quest_text):
                    matching_quests.append(quest)

        self.view_quests_from(matching_quests, filter_dones, search_text)