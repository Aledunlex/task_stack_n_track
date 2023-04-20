import db_handler
from interface import gui
from db_handler import populate_db
from scraping.scraper import QuestScraper


def create_quests_by_region():
    all_elements = db_handler.create_quests_from_json()
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
        populate_db(quest_scraper.get_element_instances_from())
    except FileNotFoundError:
        quest_scraper = QuestScraper()
        populate_db(quest_scraper.parse_elements_from())
    elems_by_category = create_quests_by_region()
    gui.App(elems_by_category)


if __name__ == '__main__':
    main()
