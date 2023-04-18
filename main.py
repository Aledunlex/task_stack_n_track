import db_handler
import gui
from scraper import populate_db


def create_quests_by_region():
    quests = db_handler.create_quests_from_json()
    quests_by_region = {}
    for quest in quests:
        region = quest.region
        if region not in quests_by_region:
            quests_by_region[region] = []
        quests_by_region[region].append(quest)
    return quests_by_region


def main():
    populate_db()
    quests_by_region = create_quests_by_region()
    app = gui.App(quests_by_region)


if __name__ == '__main__':
    main()
