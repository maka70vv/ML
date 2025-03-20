import requests
import csv
import re
from bs4 import BeautifulSoup
from collections import Counter

# URL страницы
url = "https://peterjamesthomas.com/data-and-analytics-dictionary/"

# Запрос к сайту
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

# Проверка успешного запроса
if response.status_code != 200:
    print("Ошибка загрузки страницы")
    exit()

# Разбираем HTML
soup = BeautifulSoup(response.text, "html.parser")

# Поиск всех элементов <tr> с терминами
rows = soup.find_all("tr")

data = []
text_definitions = []

# Извлечение информации
for row in rows:
    strong_tag = row.find("strong")
    if strong_tag:
        term = strong_tag.text.strip()
        definition_tag = row.find("p")
        if definition_tag:
            definition = definition_tag.text.strip()
            text_definitions.append(definition)  # Добавляем определение в анализ

            # Поиск источника (если есть)
            source_tag = row.find("textarea")
            source = source_tag.text.strip() if source_tag else "None"

            # Временная категория (можно улучшить)
            category = "Analytics"

            # Добавление в список
            data.append([term, definition, category, source])

# Подсчёт наиболее частых слов в определениях
all_words = re.findall(r'\b\w+\b', " ".join(text_definitions).lower())
common_words = Counter(all_words).most_common(10)

# Сохранение в CSV
csv_filename = "./data/Colloquium_AIN-2-22_Makarov.csv"
with open(csv_filename, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Термин", "Определение", "Категория", "Источник"])
    writer.writerows(data)

# Вывод результата
print(f"✅ Данные успешно сохранены в {csv_filename}")
print("\n📊 10 самых частых слов в определениях:")
for word, count in common_words:
    print(f"{word}: {count} раз(а)")
