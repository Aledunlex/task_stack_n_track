from flask import Flask, render_template
import os
import threading
from flask import request

from db import db_handler as db



def web_main(elems_by_categ: dict):
  app = Flask(__name__)

  def get_all_elements():
    return [element for elements in elems_by_categ.values() for element in elements]


  def get_element_by_title_and_category(title, category_value):
    for elements in elems_by_categ.values():
      for element in elements:
        if element.title.value == title and element.category.value == category_value:
          
          return element
    return None

  @app.route('/')
  def index():
    all_elements = get_all_elements()
    return render_template('index.html', all_elements=all_elements)

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
