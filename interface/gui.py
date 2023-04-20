import re

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QToolBar

from db_handler import update_element_check
from model.displayable import Category
from model.element import Element


def highlight_search_text(text, search_text):
    if search_text is None:
        return text
    return re.sub(f'({re.escape(search_text)})', r'<span style="background-color: yellow;">\1</span>', text,
                  flags=re.IGNORECASE)


class App:
    def __init__(self, elems_by_categ: dict[Category, list[Element]]):
        super().__init__()
        self._counter = None
        self.dones_filter_checkbox = None
        self.window = None
        # Sorting the elems_by_categ dict by the 'value' of their Category keys
        self.elems_by_categ = {k: v for k, v in sorted(elems_by_categ.items(), key=lambda item: item[0].value)}
        self.init_ui()

    # self.counter will also update the counter label in the toolbar when its value is updated
    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value
        # Update the counter label in the toolbar
        counter_label = self.window.findChild(QtWidgets.QLabel)
        # Get the name of the specific implementation of Element in the elems_by_categ dict
        element_str = next(iter(self.elems_by_categ.values()))[0].__class__.__name__.lower() + 's'
        counter_label.setText(f'Displaying {self.counter} {element_str}')

    def init_ui(self):
        app = QtWidgets.QApplication([])
        window = self.window = QtWidgets.QMainWindow()
        window.setWindowTitle('Quest Viewer')
        # showMaximized may not work on all platforms
        if hasattr(window, 'showMaximized'):
            window.showMaximized()

        # Create toolbar for the search functionality
        self.create_search_bar()

        window.addToolBarBreak()

        # Create a toolbar that only shows the value of the counter
        counter_toolbar = window.addToolBar('Counter')
        counter_label = QtWidgets.QLabel()
        counter_toolbar.addWidget(counter_label)

        window.addToolBarBreak()

        # Toolbar for region buttons
        self.create_region_toolbar()

        # Create central widget
        central_widget = QtWidgets.QWidget()
        window.setCentralWidget(central_widget)

        all_quests = [quest for quests in self.elems_by_categ.values() for quest in quests]
        self.view_elements_in(all_quests, self.dones_filter_checkbox.isChecked())

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
            lambda text: self.search(self.elems_by_categ, text, tag_combo_box.currentText(),
                                     dones_filter_checkbox.isChecked()))
        tag_combo_box.currentTextChanged.connect(
            lambda text: self.search(self.elems_by_categ, search_bar.text(), text,
                                     dones_filter_checkbox.isChecked()))
        dones_filter_checkbox.stateChanged.connect(
            lambda state: self.search(self.elems_by_categ, search_bar.text(), tag_combo_box.currentText(),
                                      state == QtCore.Qt.Checked))

    def create_region_toolbar(self):
        window = self.window
        region_toolbar = QToolBar()
        region_toolbar.setIconSize(QSize(32, 32))

        window.addToolBar(Qt.TopToolBarArea, region_toolbar)
        # Create a horizontal layout to hold the buttons
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)

        # Add the buttons to the layout
        for i, category in enumerate(self.elems_by_categ.keys()):
            quests = self.elems_by_categ[category]
            button = QtWidgets.QPushButton(category.value.replace('_', ' ').upper())
            button_style = """
            QPushButton {
                background-color: #COLOR;
                color: #TEXT;
                padding: 10px 20px;
                border-radius: 5px;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 16px;
            }""".replace('#COLOR', category.background_color).replace('#TEXT', category.get_text_color())
            button.setStyleSheet(button_style)
            button.clicked.connect(
                lambda checked, q=quests: self.view_elements_in(q, self.dones_filter_checkbox.isChecked()))
            hbox.addWidget(button)
        hbox.addStretch(1)
        # Create a widget to hold the layout and add it to the toolbar
        widget = QtWidgets.QWidget()
        widget.setLayout(hbox)
        region_toolbar.addWidget(widget)

    def view_elements_in(self, elements, filter_dones, search_text=None):
        central_widget = self.window.centralWidget()
        self.counter = 0
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

        for element in elements:
            if filter_dones and element.done:
                continue
            self.counter += 1
            category_color = element.category.background_color
            element_widget = QtWidgets.QGroupBox()
            element_widget.setStyleSheet(
                'background-color: #COLOR; color: #TEXT; border-radius: 5px;'.replace('#COLOR', category_color).replace(
                    '#TEXT', element.category.get_text_color())
            )
            element_layout = QtWidgets.QHBoxLayout()
            element_widget.setLayout(element_layout)

            done_checkbox = QtWidgets.QCheckBox()
            done_checkbox.setFixedSize(32, 32)
            done_checkbox.setChecked(element.done)
            done_checkbox.stateChanged.connect(lambda state, e=element: update_element_check(e, state))
            element_layout.addWidget(done_checkbox)

            text_layout = QtWidgets.QVBoxLayout()
            element_layout.addLayout(text_layout)

            # Iterating over the attributes of the element that inherit the Displayable class
            for attribute in element.get_displayable_attributes():
                attribute = element.__getattribute__(attribute)
                attribute_label = QtWidgets.QLabel()
                attribute_label.setWordWrap(attribute.word_wrap)
                attribute_label.setTextFormat(QtCore.Qt.RichText if attribute.text_format.lower() == "richtext"
                                              else QtCore.Qt.PlainText)
                style_sheet_content = ''
                if attribute.font_size:
                    style_sheet_content += 'font-size: {}px;'.format(attribute.font_size)
                if attribute.font_style:
                    style_sheet_content += 'font-style: {};'.format(attribute.font_style)
                if attribute.font:
                    style_sheet_content += 'font-family: {};'.format(attribute.font)
                if attribute.background_color:
                    style_sheet_content += 'background-color: {};'.format(attribute.background_color)
                if attribute.alignment:
                    style_sheet_content += 'text-align: {};'.format(attribute.alignment)
                attribute_label.setStyleSheet(style_sheet_content)
                attribute_label.setText(highlight_search_text(attribute.value, search_text))
                text_layout.addWidget(attribute_label)

            scroll_area_layout.addWidget(element_widget)

        spacer_item = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        scroll_area_layout.addItem(spacer_item)

        central_widget.update()

    def search(self, elements_by_category, search_text, search_tag, filter_dones):
        if not search_text:
            all_elements = [element for elements in elements_by_category.values() for element in elements]
            self.view_elements_in(all_elements, filter_dones)
            return

        search_text = search_text.lower()
        matching_elements = []
        pattern = re.compile(search_text)
        for category, elements in elements_by_category.items():
            for element in elements:
                if filter_dones and element.done:
                    continue
                element_text = getattr(element, search_tag).value.lower()
                if pattern.search(element_text):
                    matching_elements.append(element)

        self.view_elements_in(matching_elements, filter_dones, search_text)
