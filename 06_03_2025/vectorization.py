import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from gensim.parsing.preprocessing import remove_stopwords

file_path = './data/terms.xlsx'
data = pd.read_excel(file_path)

data = data.dropna(subset=['Term']).copy()

print(data['Meaning'].head())

def clean_text(text):
    if pd.isna(text):
        return []
    filtered_text = remove_stopwords(str(text).lower())
    return filtered_text.split()

text_corpus = [clean_text(row['Meaning']) for _, row in data.iterrows()]

word2vec_model = Word2Vec(sentences=text_corpus, vector_size=100, window=5, min_count=1, workers=4)

term_embeddings = {}
for term in data['Term'].dropna().unique():
    term_embeddings[term] = word2vec_model.wv[term] if term in word2vec_model.wv else np.zeros(word2vec_model.vector_size)

print(f"Уникальных терминов: {len(term_embeddings)}")
print(f"Размерность векторного пространства: {word2vec_model.vector_size}")

for idx, (term, vec) in enumerate(term_embeddings.items()):
    if idx < 5:
        print(f"Термин: {term}\nВектор: {vec}\n")

np.save('./data/term_vectors.npy', term_embeddings)
loaded_vectors = np.load('./data/term_vectors.npy', allow_pickle=True).item()

if set(term_embeddings.keys()) == set(loaded_vectors.keys()):
    print("Все термины загружены.")
else:
    print("Несоответствие терминов!")

if all(np.array_equal(term_embeddings[t], loaded_vectors[t]) for t in term_embeddings):
    print("Все векторы совпадают.")
else:
    print("Обнаружены расхождения в векторах.")
