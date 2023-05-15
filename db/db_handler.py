import json
import os
from collections import defaultdict
from pathlib import Path
from interface.displayable import Category

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

    specific_element = (
      (one_elem := all_elements[0].__class__.__name__.lower()) +
      ('ies' if one_elem.endswith('y') else 's'))

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

def get_supercategories():
    supercategories = []
    for entry in os.scandir(DATABASE):
        if entry.is_dir():
            supercategory = Category(entry.name)
            supercategories.append(supercategory)
    return supercategories


def create_elements_from_json(element_class, supercategory_name, category_name):
    elements = []
    path = os.path.join(DATABASE, supercategory_name, f"{category_name}.json")
    with open(path, 'r') as f:
        data = json.load(f)
        result = element_class.get_element_instances_from(data)
        elements.extend(result)
    return elements



def update_element_check(element, state):
    element.done = state
    # Iterate over each supercategory folder
    for supercat_folder in os.listdir(DATABASE):
        supercat_path = os.path.join(DATABASE, supercat_folder)
        if os.path.isdir(supercat_path):
            # Find the JSON file corresponding to the element
            for filename in os.listdir(supercat_path):
                if element.category.value in filename:
                    # Update the matching JSON file
                    joined_filepath = os.path.join(supercat_path, filename)
                    with open(joined_filepath, 'r') as f:
                        data = json.load(f)
                    for element_data in data:
                        if element_data['title'] == element.title.value:
                            element_data['done'] = str(element.done).capitalize()
                            print(f"{element.title} is {'not ' if not element.done else ''}done.")
                            break
                    with open(joined_filepath, 'w') as f:
                        json.dump(data, f)


def remove_from_json(element_title: str, element_category: str):
    # Iterate over each supercategory folder
    for supercat_folder in os.listdir(DATABASE):
        supercat_path = os.path.join(DATABASE, supercat_folder)
        if os.path.isdir(supercat_path):
            for filename in os.listdir(supercat_path):
                if element_category in filename:
                    with open(os.path.join(supercat_path, filename), 'r+') as file:
                        data = json.load(file)
                        data = [item for item in data if item['title'] != element_title]
                        file.seek(0)
                        json.dump(data, file)
                        file.truncate()


def insert_new_element(element, supercategory_name):
    supercat_path = os.path.join(DATABASE, supercategory_name)
    os.makedirs(supercat_path, exist_ok=True)  # Create the supercategory directory if it doesn't exist

    filename = f"{element.category.value}.json"
    file_path = os.path.join(supercat_path, filename)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

    with open(file_path, 'r+') as file:
        data = json.load(file)
        new_item = element.to_dict()
        data.append(new_item)
        file.seek(0)
        json.dump(data, file)
        file.truncate()