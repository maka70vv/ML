from transformers import MarianMTModel, MarianTokenizer

model_name = 'Helsinki-NLP/opus-mt-en-ru'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_to_russian(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

sentences = [
    "Hello! How are you?",
    "This is a test of the English to Russian translation system.",
    "I am learning Python and natural language processing.",
]

for s in sentences:
    print(f"EN: {s}")
    print(f"RU: {translate_to_russian(s)}\n")
