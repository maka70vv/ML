import requests
import csv
import re
from bs4 import BeautifulSoup
from collections import Counter

url = "https://peterjamesthomas.com/data-and-analytics-dictionary/"

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("Ошибка загрузки страницы")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr")

data = []
text_definitions = []

for row in rows:
    strong_tag = row.find("strong")
    if strong_tag:
        term = strong_tag.text.strip()
        definition_tag = row.find("p")
        if definition_tag:
            definition = definition_tag.text.strip()
            text_definitions.append(definition)

            source = "Peter James Thomas"

            category = "Analytics"

            data.append([term, definition, category, source])

all_words = re.findall(r'\b\w+\b', " ".join(text_definitions).lower())
common_words = Counter(all_words).most_common(10)

csv_filename = "./data/Colloquium_AIN-2-22_Makarov.csv"
with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Term", "Definition", "Категория", "Источник"])
    writer.writerows(data)

print(f"Данные успешно сохранены в {csv_filename}")
print("\n10 самых частых слов в определениях:")
for word, count in common_words:
    print(f"{word}: {count} раз")
