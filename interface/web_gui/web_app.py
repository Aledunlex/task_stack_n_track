from flask import Flask, render_template, jsonify
import os
import threading
from flask import request

from interface.displayable import Displayable

from db import db_handler as db


def web_main(elems_by_categ: dict):
  app = Flask(__name__)

  def get_all_elements():
    return [
      element for elements in elems_by_categ.values() for element in elements
    ]

  def create_blank_element(element_class, element_attributes):
    blank_element = element_class(**element_attributes, category="Category")
    blank_element.category.background_color = "#808080"
    return blank_element

  def get_element_by_title_and_category(title, category_value):
    for elements in elems_by_categ.values():
      for element in elements:
        if element.title.value == title and element.category.value == category_value:

          return element
    return None

  @app.route('/create_element', methods=['POST'])
  def create_element():
    try:
      attributes = request.form
      # Create a new Element object and set its attributes
      first_elem = get_all_elements()[0]
      element_class = type(first_elem)
      element_attributes = {
        attr_name: attr_value
        for attr_name, attr_value in attributes.items()
      }
      print(element_attributes)
      new_element = element_class(**element_attributes)

      # Add the new element to the list
      current_elems_in_cat = elems_by_categ.get(new_element.category)
      if current_elems_in_cat is None:
        elems_by_categ[new_element.category] = [new_element]
      else:
        current_elems_in_cat.append(new_element)
      db.insert_new_element(new_element)
      return jsonify({'success': True})
    except Exception as e:
      return jsonify({'success': False, 'error': str(e)})

  @app.route('/remove_element', methods=['POST'])
  def remove_element():
    element_title = request.form.get('element_title')
    element_category = request.form.get('element_category')
    print(f'Element title: {element_title}, Element category: {element_category}')

    try:
      for key in elems_by_categ:
        if key.value == element_category:
            # update the list of elements for this category
            elems_by_categ[key] = [
                elem for elem in elems_by_categ[key]
                if elem.title.value != element_title
            ]
            break  # exit the loop once the correct category is found
      db.remove_from_json(element_title, element_category)
      return jsonify({'success': True})
    except Exception as e:
      raise e
      return jsonify({'success': False, 'error': str(e)})

  @app.route('/')
  def index():
    all_elements = get_all_elements()
    categories = list(set([element.category for element in all_elements]))

    element_class = type(all_elements[0])
    element_attributes = {
      attr: attr.capitalize()
      for attr in all_elements[0].get_displayable_attributes()
    }

    blank_element = create_blank_element(element_class, element_attributes)
    blank_element.is_editable = True
    all_elements.insert(0, blank_element)

    return render_template('index.html',
                           all_elements=all_elements,
                           categories=categories)

  @app.route('/update_done', methods=['POST'])
  def update_done():
    element_title = request.form.get('element_title')
    element_category = request.form.get('element_category')
    is_done = request.form.get('is_done') == 'true'
    element = get_element_by_title_and_category(element_title,
                                                element_category)
    if element:

      db.update_element_check(element, is_done)
      return "OK"
    else:
      return "Element not found", 404

  def run_app():
    app.run(host='0.0.0.0',
            port=int(os.environ.get('PORT', 8080)),
            debug=True,
            use_reloader=False)

  t = threading.Thread(target=run_app)
  t.start()
