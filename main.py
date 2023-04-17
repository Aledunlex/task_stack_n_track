import os
import json
import re
from pathlib import Path
from PyQt5 import QtWidgets, QtCore

import requests
from collections import defaultdict
from bs4 import BeautifulSoup

DATABASE = 'DATABASE'


class Quest:
    def __init__(self, region, title, reward, solution, done=False):
        self.region = region
        self.title = title
        self.reward = reward
        self.solution = solution
        self.done = done

    def to_dict(self):
        return {
            'region': self.region,
            'title': self.title,
            'reward': self.reward,
            'solution': self.solution
        }

    def __str__(self):
        return f'Quest(region={self.region}, title={self.title}, reward={self.reward}, solution={self.solution})'


def get_quests(url):
    quests = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for li in soup.select('ul.liste-default-jv li'):
        region_url = li.find('a')['href']
        region = li.text \
            .replace('Quêtes annexes d\'', '') \
            .replace('Quêtes annexes des ', '') \
            .replace('Quêtes annexes de ', '') \
            .replace(' ', '_').replace('-', '_') \
            .strip()
        print(region)

        region_response = requests.get(region_url)
        region_soup = BeautifulSoup(region_response.text, 'html.parser')

        for h2 in region_soup.find_all('h2', class_='h2-default-jv'):
            title = h2.text.strip()
            # reward is the next p tag after the h2 that starts with "Récompense", but it's not always present
            reward = ''
            for p in h2.find_next_siblings('p'):
                if p.text.startswith('Récompense'):
                    reward = p.text
                    break
            # if there is a reward, solution is the p tag after that, otherwise it's the p tag immediately after the h2
            if reward:
                solution = h2.find_next_sibling('p').find_next_sibling('p').text.strip()
            else:
                solution = h2.find_next_sibling('p').text.strip()
            quest = Quest(region=region, title=title, reward=reward, solution=solution, done=False)
            quests.append(quest)

    return quests


def create_quests_from_json():
    quests = []
    for filename in os.listdir(DATABASE):
        if filename.endswith('.json'):
            with open(os.path.join(DATABASE, filename), 'r') as f:
                data = json.load(f)
                for quest_data in data:
                    region = quest_data['region']
                    title = quest_data['title']
                    reward = quest_data['reward']
                    solution = quest_data['solution']
                    done = quest_data.get('done', False)
                    quest = Quest(region=region, title=title, reward=reward, solution=solution, done=done)
                    quests.append(quest)
    return quests


def create_quests_by_region():
    quests = create_quests_from_json()
    quests_by_region = {}
    for quest in quests:
        region = quest.region
        if region not in quests_by_region:
            quests_by_region[region] = []
        quests_by_region[region].append(quest)
    return quests_by_region


def search_quests(window, quests_by_region, search_text, search_tag, filter_dones):
    if not search_text:
        view_quests_from(list(quests_by_region.values())[0], window, filter_dones, search_text)
        return

    search_text = search_text.lower()
    matching_quests = []
    for region, quests in quests_by_region.items():
        for quest in quests:
            if filter_dones and quest.done:
                continue
            quest_text = getattr(quest, search_tag).lower()
            if search_text in quest_text:
                matching_quests.append(quest)

    view_quests_from(matching_quests, window, filter_dones, search_text)


def view_quests_from(quests, window, filter_dones, search_text=None):
    central_widget = window.centralWidget()
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


def highlight_search_text(text, search_text):
    if search_text is None:
        return text
    return re.sub(f'({re.escape(search_text)})', r'<span style="background-color: yellow;">\1</span>', text, flags=re.IGNORECASE)


def update_quest_done(quest, state):
    quest.done = state == QtCore.Qt.Checked
    # Find the JSON file corresponding to the quest
    for filename in os.listdir(DATABASE):
        if quest.region in filename:
            # Update the matching JSON file
            joined_filepath = os.path.join(DATABASE, filename)
            with open(joined_filepath, 'r') as f:
                data = json.load(f)
            for quest_data in data:
                if quest_data['title'] == quest.title:
                    quest_data['done'] = quest.done
                    print(f"{quest.title} is {'not ' if not quest.done else ''}done.")
                    break
            with open(joined_filepath, 'w') as f:
                json.dump(data, f)


def create_main_window(quests_by_region):
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    window.setWindowTitle('Quest Viewer')
    window.showMaximized()

    # Create toolbar
    toolbar = window.addToolBar('Toolbar')

    # Create search bar
    search_bar = QtWidgets.QLineEdit()
    search_bar.setPlaceholderText('Search quests...')
    toolbar.addWidget(search_bar)

    # Create tag combo box
    tag_combo_box = QtWidgets.QComboBox()
    tag_combo_box.addItems(['title', 'reward', 'solution'])
    toolbar.addWidget(tag_combo_box)

    # Create done only checkbox
    done_only_checkbox = QtWidgets.QCheckBox('Filter completed')
    done_only_checkbox.setChecked(True)
    toolbar.addWidget(done_only_checkbox)

    # Connect search bar and tag combo box signals
    search_bar.textChanged.connect(
        lambda text: search_quests(window, quests_by_region, text, tag_combo_box.currentText(), done_only_checkbox.isChecked()))
    tag_combo_box.currentTextChanged.connect(
        lambda text: search_quests(window, quests_by_region, search_bar.text(), text, done_only_checkbox.isChecked()))
    done_only_checkbox.stateChanged.connect(
        lambda state: search_quests(window, quests_by_region, search_bar.text(), tag_combo_box.currentText(), state == QtCore.Qt.Checked))

    # Create buttons for each region
    for region in sorted(quests_by_region.keys()):
        quests = quests_by_region[region]
        button = QtWidgets.QPushButton(region.replace('_', ' '))
        button.clicked.connect(lambda checked, q=quests: view_quests_from(q, window, done_only_checkbox.isChecked()))
        toolbar.addWidget(button)

    # Create central widget
    central_widget = QtWidgets.QWidget()
    window.setCentralWidget(central_widget)

    # Show window
    window.show()
    app.exec_()


def main():
    # Check if the DATABASE directory exists and contains 8 JSON files.
    if not (os.path.exists(DATABASE) and len(os.listdir(DATABASE)) == 8):
        # Create the DATABASE directory if it doesn't exist.
        os.makedirs(DATABASE, exist_ok=True)
        print(f"Creating {DATABASE} folder")

        url = 'https://www.jeuxvideo.com/wikis-soluce-astuces/1716911/quetes-annexes.htm'
        print(f"Scraping data from {url}")
        quests = get_quests(url)

        # Group the quests by region.
        quests_by_region = defaultdict(list)
        for quest in quests:
            quests_by_region[quest.region].append(quest.to_dict())

        print(f"Found {len(quests)} elements")

        # Save the quests for each region to a separate JSON file.
        for region, quests in quests_by_region.items():
            filename = f'DATABASE/{region}_quests.json'
            if Path(filename).exists():
                print(f"{filename} already exists, skipping it")
                continue
            with open(filename, 'w') as f:
                json.dump(quests, f, indent=4)
                print(f"Wrote file {filename}")

    quests_by_region = create_quests_by_region()
    create_main_window(quests_by_region)


if __name__ == '__main__':
    main()
