import csv
import pdfplumber
import re

def extract_terms_and_descriptions(pdf_path):
    # Открываем PDF файл
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        # Извлекаем текст из всех страниц
        for page in pdf.pages:
            all_text += page.extract_text()

    # Очистка текста от лишних символов и переносов
    clean_lines = []
    for line in all_text.splitlines():
        # Убираем лишние пробелы, табуляции, объединяем переносы строк
        clean_line = ' '.join(line.split()).strip()
        if clean_line:
            clean_lines.append(clean_line)

    # Инициализируем массив словарей
    terms_descriptions = []
    seen_terms = set()

    # Регулярное выражение для удаления содержимого в скобках
    remove_parentheses = re.compile(r'\(.*?\)')

    # Обрабатываем каждую строку
    for line in clean_lines:
        # Проверяем, содержит ли строка разделитель "~"
        if '~' in line:
            # Разделяем строку на термин и описание
            term, description = map(str.strip, line.split('~', 1))
            # Удаляем содержимое в скобках из термина
            term = remove_parentheses.sub('', term).strip()
            # Пропускаем строки, где термин отсутствует или неправильно извлечен
            if term and term not in seen_terms:
                terms_descriptions.append({"term": term, "description": description})
                seen_terms.add(term)

    return terms_descriptions

# Пример использования
pdf_path = "/home/makarov/PycharmProjects/ML/27_02_2025/data/Dictionary_of_Computer_and_Internet_Terms_Words-450-530.pdf"
terms_and_descriptions = extract_terms_and_descriptions(pdf_path)

# Запись в CSV
csv_output_path = "data/it_turns_Makarov.csv"
source_url = "https://damanhour.edu.eg/"

with open(csv_output_path, mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    # Записываем заголовки
    csv_writer.writerow(["Term", "Definition", "Source"])
    # Записываем данные
    for item in terms_and_descriptions:
        csv_writer.writerow([item["term"], item["description"], source_url])
