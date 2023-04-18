import json
import os

from PyQt5 import QtCore

from quest import Quest

DATABASE = 'DATABASE'


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
                break
