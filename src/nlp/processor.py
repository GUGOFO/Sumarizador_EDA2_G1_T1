import os
import spacy

from ..structures.hash_table import contar_palavras

class TextProcessor:
    """Processa texto bruto, separando frases e criando HashTable por frase."""
    def __init__(self):
        """Inicializa o motor do spaCy para a língua portuguesa."""
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except IOError:
            raise IOError(
                "O modelo 'pt_core_news_sm' não foi encontrado. "
                "Certifique-se de rodar o script de setup (setup.sh ou setup.bat) antes."
            )

    def load_text_from_file(self, folder_path: str, filename: str) -> str:
        """Lê o conteúdo de um arquivo .txt na pasta especificada."""
        full_path = os.path.join(folder_path, filename)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"O arquivo {filename} não foi encontrado na pasta {folder_path}.")

        with open(full_path, "r", encoding="utf-8") as file:
            return file.read()

    def process_contract(self, raw_text: str):
        """Processa o texto e retorna lista de dicts com frase, tokens e HashTable.

        Cada dict contém:
            - "original_text": frase original limpa
            - "tokens": lista de lemas normalizados (sem stopwords/pontuação)
            - "hash_table": HashTable com contagem de palavras da frase
        """
        doc = self.nlp(raw_text)

        processed_sentences = []

        for sentence in doc.sents:
            cleaned_sentence_text = sentence.text.strip()

            if not cleaned_sentence_text:
                continue

            cleaned_tokens = []

            for token in sentence:
                if not token.is_stop and not token.is_punct and token.is_alpha:
                    lemma_word = token.lemma_.lower()
                    cleaned_tokens.append(lemma_word)

            if cleaned_tokens:
                hash_table = contar_palavras(sentence)
                processed_sentences.append({
                    "original_text": cleaned_sentence_text,
                    "tokens": cleaned_tokens,
                    "hash_table": hash_table
                })

        return processed_sentences
