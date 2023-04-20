import json
import os
from collections import defaultdict
from pathlib import Path

from PyQt5 import QtCore

from model.element import Quest
from scraping.scraper import get_quests

DATABASE = 'DATABASE'


def create_quests_from_json():
    quests = []
    for filename in os.listdir(DATABASE):
        if filename.endswith('.json'):
            with open(os.path.join(DATABASE, filename), 'r') as f:
                data = json.load(f)
                for quest_data in data:
                    category = quest_data['category']
                    title = quest_data['title']
                    reward = quest_data['reward']
                    solution = quest_data['solution']
                    done = quest_data.get('done') == 'True'
                    quest = Quest(category=category, title=title, reward=reward, solution=solution, done=done)
                    quests.append(quest)
    return quests


def update_quest_done(quest, state):
    quest.done = state == QtCore.Qt.Checked
    # Find the JSON file corresponding to the quest
    for filename in os.listdir(DATABASE):
        if quest.category.value in filename:
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
                break


def populate_db():
    # Check if the DATABASE directory exists and contains 8 JSON files.
    if not (os.path.exists(DATABASE) and len(os.listdir(DATABASE)) == 8):
        # Create the DATABASE directory if it doesn't exist.
        os.makedirs(DATABASE, exist_ok=True)
        print(f"Creating {DATABASE} folder")

        url = 'https://www.jeuxvideo.com/wikis-soluce-astuces/1716911/quetes-annexes.htm'
        print(f"Scraping data from {url}")
        quest_dicts = [quest.to_dict() for quest in get_quests(url)]

        # Group the quests by region.
        quests_by_region = defaultdict(list)
        for quest in quest_dicts:
            quests_by_region[quest['category']].append(quest)

        print(f"Found {len(quest_dicts)} elements")

        # Save the quests for each region to a separate JSON file.
        for region, quests in quests_by_region.items():
            print(quests)
            filename = f'{DATABASE}/{region}_quests.json'
            if Path(filename).exists():
                print(f"{filename} already exists, skipping it")
                continue

            # If write fails, delete the file.
            try:
                with open(filename, 'w') as f:
                    json.dump(quests, f, indent=2)
            except:
                os.remove(filename)
                raise


