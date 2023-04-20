from db import db_handler
from db.db_handler import populate_db
from interface import gui
from scraping.scraper import QuestScraper


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
    quest_scraper = QuestScraper()
    try:
        elems_by_category = create_elements_by_category(quest_scraper.element_class)
    except FileNotFoundError as e:
        print(f"Error: {e}. Creating new database...")
        element_dics = quest_scraper.scrape()
        all_data = quest_scraper.get_element_instances_from(element_dics)
        populate_db(all_data)
        elems_by_category = create_elements_by_category(quest_scraper.element_class)
    try:
        gui.App(elems_by_category)
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main()
