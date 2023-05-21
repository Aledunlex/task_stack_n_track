from db import db_handler


#     from interface import pyqt_gui


def create_elements_by_category(element_class):
    all_elements = db_handler.create_elements_from_json(element_class)
    elements_by_category = {}
    for element in all_elements:
        category = element.category
        if category not in elements_by_category:
            elements_by_category[category] = []
        elements_by_category[category].append(element)
    return elements_by_category


def main():
    from interface.web_gui.web_app import main as web_main
    web_main()


if __name__ == '__main__':
    main()
