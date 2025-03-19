import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Загрузка данных из файла Excel
file_path = "./data/it_terms_all.xlsx"
xls = pd.ExcelFile(file_path)

# Чтение первого листа
df = pd.read_excel(xls, sheet_name='Лист1')

# Фильтрация терминов по категории "Cybersecurity English"
cybersecurity_terms = df[df['Category'].str.contains('Cybersecurity', case=False, na=False)]

# Получение списка терминов
terms = cybersecurity_terms['Term'].dropna().tolist()

# Векторизация терминов с помощью TF-IDF
vectorizer = TfidfVectorizer()
term_vectors = vectorizer.fit_transform(terms)

# Преобразование результатов в DataFrame
tfidf_df = pd.DataFrame(term_vectors.toarray(),
                         columns=vectorizer.get_feature_names_out(),
                         index=terms)

# Сохранение результата в файл
output_file = "./data/cybersecurity_tfidf.csv"
tfidf_df.to_csv(output_file, encoding='utf-8')

print(f"Файл с векторизованными терминами сохранен как {output_file}")
