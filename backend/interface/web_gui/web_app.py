import json
import os

from db import db_handler as db
from flask import Flask, jsonify, send_from_directory
from flask import request
from flask_cors import CORS
from interface.displayable import Category
from model.element import Element


class MyFlaskApp(Flask):

    def __init__(self, import_name, **options):
        super().__init__(import_name, **options)
        self.categories_by_supercategories = {}
        self.elements_by_category = {}

        self.route('/api/addElement', methods=['POST'])(self.create_element)
        self.route('/api/removeElement', methods=['DELETE'])(self.remove_element)
        self.route('/api/supercategories')(self.supercategories)
        self.route('/api/<supercategory>')(self.index)
        self.route('/api/updateElement', methods=['PUT'])(self.update_done)
        self.route('/<path:path>', defaults={'path': ''})(self.serve)


    def serve(self, path):
        if path != "" and os.path.exists(os.path.join(self.static_folder, path)):
            return send_from_directory(self.static_folder, path)
        else:
            return send_from_directory(self.static_folder, 'index.html')

    def load_data(self, supercategory):
        """Load data for a specific supercategory."""
        path = os.path.join(db.DATABASE, supercategory.value)
        self.categories_by_supercategories[supercategory] = {}
        # on itère sur chaque fichier dans "path", les ouvrir, et récupérer les éléments json qu'ils contiennent
        for filename in os.listdir(path):

            category_name = filename.split('.json')[0]
            category = Category(category_name)
            with open(os.path.join(path, filename), 'r') as f:
                data = json.load(f)
                for content in data:
                    # A Stackable's properties are handled with a special attribute
                    if content.get("_stackable_properties") is not None:
                        content["stackable_properties"] = content.pop("_stackable_properties")

                    element_class = Element.get_class_from_attributes(content)
                    created_element = element_class(**content)

                    if category not in self.categories_by_supercategories[supercategory]:
                        self.categories_by_supercategories[supercategory][category] = [created_element]
                    else:
                        self.categories_by_supercategories[supercategory][category].extend([created_element])

                    if category not in self.elements_by_category:
                        self.elements_by_category[category] = [created_element]
                    elif created_element not in self.elements_by_category[category]:
                        self.elements_by_category[category].extend([created_element])
                    else:
                        print(f"Element {created_element.title} already exists in category {category}")

    def get_all_elements(self, supercategory):
        return [
            element for elements in self.categories_by_supercategories.get(
                supercategory).values() for element in elements
        ]

    def create_blank_element(self, element_class, element_attributes):
        blank_element = element_class(**element_attributes, category="Category")
        blank_element.category.background_color = "#808080"
        return blank_element

    def get_element_by_title_and_category(self, title, category_value):
        for elements in self.elements_by_category.values():
            for element in elements:
                if element.title.value == title and element.category.value == category_value:
                    return element
        return None

    def create_element(self):
        try:
            form_data = request.get_json()
            print(form_data)
            supercategory = form_data.get('supercategory')
            attributes = {k: v for k, v in form_data.items() if k != 'supercategory'}

            # Create a new Element object and set its attributes
            element_attributes = {
                attr_name: attr_value
                for attr_name, attr_value in attributes.items()
                if (attr_name != "done" and attr_name != "type")
            }
            # A Stackable's properties are handled with a special attribute
            if element_attributes.get("_stackable_properties") is not None:
                element_attributes["stackable_properties"] = element_attributes.pop("_stackable_properties")

            element_class = Element.get_class_from_attributes(element_attributes)
            new_element = element_class(**element_attributes)

            # Add the new element to the list
            current_elems_in_cat = self.elements_by_category.get(new_element.category)
            if current_elems_in_cat is None or len(current_elems_in_cat) == 0:
                self.elements_by_category[new_element.category] = [new_element]
            else:
                new_element.category = current_elems_in_cat[0].category
                current_elems_in_cat.append(new_element)
                element_attributes.update({"background_color": new_element.category.background_color})
            db.insert_new_element(new_element, supercategory)
            response = {'success': True, 'element': element_attributes}
            print(f"Response: {response}")
            return jsonify(response)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    def remove_element(self):
        requested_json = request.get_json()
        element_title = requested_json.get('title')
        element_category = requested_json.get('category')

        try:
            if self.get_element_by_title_and_category(element_title, element_category) is None:
                raise Exception(
                    f'Could not find element with title "{element_title}" and category "{element_category}"'
                )
            for key in self.elements_by_category:
                if key.value == element_category:
                    self.elements_by_category[key] = [
                        elem for elem in self.elements_by_category[key]
                        if elem.title.value != element_title
                    ]
            db.remove_from_json(element_title, element_category)
            print(f"{element_title} removed")
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    def supercategories(self):
        supercategories = db.get_supercategories()
        return jsonify(supercategories=[supercat.to_dict() for supercat in supercategories])

    def index(self, supercategory):
        supercategory = Category(supercategory)
        self.load_data(supercategory)
        all_elements = self.get_all_elements(supercategory)
        categories = list(set([element.category for element in all_elements]))

        print(f"{len(all_elements)} elements loaded")
        return jsonify(all_elements=[e.to_dict() for e in all_elements],
                       categories=[str(category) for category in categories],
                       supercategory=str(supercategory))

    def update_done(self):
        print(request.get_json())
        element_title = request.get_json()['title']
        element_category = request.get_json()['category']
        is_done = request.get_json()['done']
        element = self.get_element_by_title_and_category(element_title,
                                                         element_category)
        if element:
            db.update_element_check(element, is_done)
            return "OK", 200
        else:
            return "Element not found", 404


def main():
    app = MyFlaskApp(__name__, static_folder='../frontend/build')
    CORS(app)
    app.run(host='localhost',
            port=int(os.environ.get('PORT', 8080)),
            debug=False,
            use_reloader=False)
