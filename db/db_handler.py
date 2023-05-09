import json
import os
from collections import defaultdict
from pathlib import Path

from PyQt5 import QtCore

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DATABASE")


def populate_db(all_elements):
    # Check if the DATABASE directory exists and isn't empty.
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


def create_elements_from_json(element_class):
    quests = []
    for filename in os.listdir(DATABASE):
        if filename.endswith('.json'):
            with open(os.path.join(DATABASE, filename), 'r') as f:
                data = json.load(f)
                result = element_class.get_element_instances_from(data)
                quests.extend(result)
    return quests


def update_element_check(element, state):
    print(f"Getting {element.title.value} which is {'done' if element.done else 'not done'}")
    element.done = state
    print(f"Updated (?) : {element.title.value} is {'done' if element.done else 'not done'}")
    # Find the JSON file corresponding to the element
    for filename in os.listdir(DATABASE):
        if element.category.value in filename:
            # Update the matching JSON file
            joined_filepath = os.path.join(DATABASE, filename)
            with open(joined_filepath, 'r') as f:
                data = json.load(f)
            for element_data in data:
                if element_data['title'] == element.title.value:
                    element_data['done'] = str(element.done).capitalize()
                    print(f"{element.title} is {'not ' if not element.done else ''}done.")
                    break
            with open(joined_filepath, 'w') as f:
                json.dump(data, f)

            with open(joined_filepath, 'r') as f:
                updated_data = json.load(f)
                break
    print("Updated data in JSON file:", updated_data)
