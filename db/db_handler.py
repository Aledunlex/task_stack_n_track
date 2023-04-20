import json
import os
from collections import defaultdict
from pathlib import Path

from PyQt5 import QtCore

from model.element import Quest

DATABASE = 'DATABASE'


def populate_db(all_elements):
    # Check if the DATABASE directory exists and isn't empty.
    print("populating?")
    if not os.path.exists(DATABASE) or not os.listdir(DATABASE):
        os.makedirs(DATABASE, exist_ok=True)
        print(f"Creating {DATABASE} folder")

        element_dictionaries = [elem.to_dict() for elem in all_elements]
        elements_by_category = defaultdict(list)
        for element_dic in element_dictionaries:
            elements_by_category[element_dic['category']].append(element_dic)

        specific_element = ((one_elem := all_elements[0].__class__.__name__.lower())
                            + ('ies' if one_elem.endswith('y') else 's'))

        # Save the elements for category to a separate JSON file
        for category, elements in elements_by_category.items():
            filename = f'{DATABASE}/{category}_{specific_element}.json'
            if Path(filename).exists() and Path(filename).stat().st_size > 0:
                print(f"{filename} already exists, skipping it")
                continue

            try:
                with open(filename, 'w') as f:
                    json.dump(elements, f, indent=2)
            except:
                print(f"Error while saving {filename} to disk")
                if os.path.exists(filename):
                    os.remove(filename)
                raise


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


def update_element_check(element, state):
    element.done = state == QtCore.Qt.Checked
    # Find the JSON file corresponding to the element
    for filename in os.listdir(DATABASE):
        if element.category.value in filename:
            # Update the matching JSON file
            joined_filepath = os.path.join(DATABASE, filename)
            with open(joined_filepath, 'r') as f:
                data = json.load(f)
            for element_data in data:
                if element_data['title'] == element.title:
                    element_data['done'] = element.done
                    print(f"{element.title} is {'not ' if not element.done else ''}done.")
                    break
            with open(joined_filepath, 'w') as f:
                json.dump(data, f)
                break
