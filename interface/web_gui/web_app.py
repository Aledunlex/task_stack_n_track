from flask import Flask, render_template, jsonify
import os
from flask import request

from db import db_handler as db
from interface.displayable import Category
from model.element import Quest, Stackable


class MyFlaskApp(Flask):

  def __init__(self, import_name, **options):
    super().__init__(import_name, **options)
    print("Initializing Flask app...")
    self.categories_by_supercategories = {}
    self.elements_by_category = {}

    self.route('/create_element', methods=['POST'])(self.create_element)
    self.route('/remove_element', methods=['POST'])(self.remove_element)
    self.route('/')(self.supercategories)
    self.route('/<supercategory>')(self.index)
    self.route('/update_done', methods=['POST'])(self.update_done)

  def load_data(self, supercategory, element_class):
    """Load data for a specific supercategory."""
    if supercategory not in self.categories_by_supercategories:  # load data only if not already loaded
      path = os.path.join(db.DATABASE, supercategory.value)
      self.categories_by_supercategories[supercategory] = {}
      for filename in os.listdir(path):
        category_name = filename.split('.json')[0]
        category = Category(category_name)
        elements = db.create_elements_from_json(element_class,
                                                supercategory.value,
                                                category_name)
        self.categories_by_supercategories[supercategory][category] = elements
        self.elements_by_category[category] = elements

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
    for elements in self.categories_by_supercategories.values():
      for element in elements:
        if element.title.value == title and element.category.value == category_value:
          return element
    return None

  def create_element(self):
    try:
      form_data = request.form
      supercategory = form_data.get('supercategory')
      attributes = {k: v for k, v in form_data.items() if k != 'supercategory'}

      # Determine the class of the new element based on a query parameter
      element_type = 'Quest'  #request.args.get('element_type')
      if element_type == 'Quest':
        element_class = Quest
      elif element_type == 'Stackable':
        element_class = Stackable
      else:
        # Default to creating a Quest if no valid element type is specified
        element_class = Quest

      # Create a new Element object and set its attributes
      element_attributes = {
        attr_name: attr_value
        for attr_name, attr_value in attributes.items() if attr_name != "done"
      }
      new_element = element_class(**element_attributes)

      # Add the new element to the list
      current_elems_in_cat = self.elements_by_category.get(
        new_element.category)
      if current_elems_in_cat is None:
        self.elements_by_category[new_element.category] = [new_element]
      else:
        new_element.category = current_elems_in_cat[0].category
        current_elems_in_cat.append(new_element)
        element_attributes.update(
          {"background_color": new_element.category.background_color})
      db.insert_new_element(new_element, supercategory)
      response = {'success': True, 'element': element_attributes}
      print(f"Response: {response}")
      return jsonify(response)
    except Exception as e:
      raise
      return jsonify({'success': False, 'error': str(e)})

  def remove_element(self):
    element_title = request.form.get('element_title')
    element_category = request.form.get('element_category')
    print(
      f'Element title: {element_title}, Element category: {element_category}')

    try:
      for key in self.elements_by_category:
        if key.value == element_category:
          self.elements_by_category[key] = [
            elem for elem in self.elements_by_category[key]
            if elem.title.value != element_title
          ]
          break
      db.remove_from_json(element_title, element_category)
      return jsonify({'success': True})
    except Exception as e:
      return jsonify({'success': False, 'error': str(e)})

  def supercategories(self):
    supercategories = db.get_supercategories()
    return render_template('supercategories.html',
                           supercategories=supercategories)

  def index(self, supercategory):
    supercategory = Category(supercategory)
    self.load_data(supercategory, Quest)
    # Get the elements belonging to the supercategory
    all_elements = self.get_all_elements(supercategory)

    categories = list(set([element.category for element in all_elements]))
    if all_elements:
      element_class = type(all_elements[0])
      element_attributes = {
        attr: attr.capitalize()
        for attr in all_elements[0].get_displayable_attributes()
      }

      blank_element = self.create_blank_element(element_class,
                                                element_attributes)
      blank_element.is_editable = True
      all_elements.insert(0, blank_element)

    return render_template('index.html',
                           all_elements=all_elements,
                           categories=categories,
                           supercategory=supercategory.value)

  def update_done(self):
    element_title = request.form.get('element_title')
    element_category = request.form.get('element_category')
    is_done = request.form.get('is_done') == 'true'
    element = self.get_element_by_title_and_category(element_title,
                                                     element_category)
    if element:
      db.update_element_check(element, is_done)
      return "OK"
    else:
      return "Element not found", 404


def main():
  app = MyFlaskApp(__name__)
  app.run(host='0.0.0.0',
          port=int(os.environ.get('PORT', 8080)),
          debug=False,
          use_reloader=False)
