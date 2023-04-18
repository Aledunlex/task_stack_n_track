import json
import os
from collections import defaultdict
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from db_handler import DATABASE
from quest import Quest


def get_quests(url):
    quests = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for li in soup.select('ul.liste-default-jv li'):
        region_url = li.find('a')['href']
        region = li.text \
            .replace('Quêtes annexes d\'', '') \
            .replace('Quêtes annexes des ', '') \
            .replace('Quêtes annexes de ', '') \
            .replace(' ', '_').replace('-', '_') \
            .strip()
        print(region)

        region_response = requests.get(region_url)
        region_soup = BeautifulSoup(region_response.text, 'html.parser')

        for h2 in region_soup.find_all('h2', class_='h2-default-jv'):
            title = h2.text.strip()
            # reward is the next p tag after the h2 that starts with "Récompense", but it's not always present
            reward = ''
            for p in h2.find_next_siblings('p'):
                if p.text.startswith('Récompense'):
                    reward = p.text
                    break
            # if there is a reward, solution is the p tag after that, otherwise it's the p tag immediately after the h2
            if reward:
                solution = h2.find_next_sibling('p').find_next_sibling('p').text.strip()
            else:
                solution = h2.find_next_sibling('p').text.strip()
            quest = Quest(region=region, title=title, reward=reward, solution=solution, done=False)
            quests.append(quest)

    return quests


def populate_db():
    # Check if the DATABASE directory exists and contains 8 JSON files.
    if not (os.path.exists(DATABASE) and len(os.listdir(DATABASE)) == 8):
        # Create the DATABASE directory if it doesn't exist.
        os.makedirs(DATABASE, exist_ok=True)
        print(f"Creating {DATABASE} folder")

        url = 'https://www.jeuxvideo.com/wikis-soluce-astuces/1716911/quetes-annexes.htm'
        print(f"Scraping data from {url}")
        quests = get_quests(url)

        # Group the quests by region.
        quests_by_region = defaultdict(list)
        for quest in quests:
            quests_by_region[quest.region].append(quest.to_dict())

        print(f"Found {len(quests)} elements")

        # Save the quests for each region to a separate JSON file.
        for region, quests in quests_by_region.items():
            filename = f'DATABASE/{region}_quests.json'
            if Path(filename).exists():
                print(f"{filename} already exists, skipping it")
                continue
            with open(filename, 'w') as f:
                json.dump(quests, f, indent=4)
                print(f"Wrote file {filename}")
