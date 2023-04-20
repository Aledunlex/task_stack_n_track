from db import db_handler
from interface import gui
from db.db_handler import populate_db
from scraping.scraper import QuestScraper


def create_quests_by_region():
    all_elements = db_handler.create_quests_from_json()
    elements_by_category = {}
    for element in all_elements:
        category = element.category
        if category not in elements_by_category:
            elements_by_category[category] = []
        elements_by_category[category].append(element)
    print(len(all_elements))
    return elements_by_category


def main():
    try:
        elems_by_category = create_quests_by_region()
    except FileNotFoundError as e:
        print(f"Error: {e}. Creating new database...")
        quest_scraper = QuestScraper()
        element_dics = quest_scraper.parse_elements_from()
        all_data = quest_scraper.get_element_instances_from(element_dics)
        populate_db(all_data)
        elems_by_category = create_quests_by_region()

    gui.App(elems_by_category)


if __name__ == '__main__':
    main()
