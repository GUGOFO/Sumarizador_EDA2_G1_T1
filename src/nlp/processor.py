import os
import spacy

class TextProcessor:
    def __init__(self):
        """Inicializa o motor do spaCy para a língua portuguesa."""
        try:
            # Carrega o modelo leve de português
            self.nlp = spacy.load("pt_core_news_sm")
        except IOError:
            raise IOError(
                "O modelo 'pt_core_news_sm' não foi encontrado. "
                "Certifique-se de rodar o script de setup (setup.sh ou setup.bat) antes."
            )

    def load_text_from_file(self, folder_path: str, filename: str) -> str:
        """Lê o arquivo .txt dentro da pasta especificada."""
        full_path = os.path.join(folder_path, filename)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"O arquivo {filename} não foi encontrado na pasta {folder_path}.")
        
        with open(full_path, "r", encoding="utf-8") as file:
            return file.read()

    def process_contract(self, raw_text: str):
        """
        Processa o texto do contrato.
        Retorna uma lista de dicionários contendo a frase original 
        e a lista de palavras limpas e lematizadas.
        """
        # O spaCy faz a mágica de tokenizar, separar frases e taguear gramaticalmente de uma vez
        doc = self.nlp(raw_text)
        
        processed_sentences = []
        
        # Iteramos sobre as frases detectadas pelo spaCy
        for sentence in doc.sents:
            # Removemos espaços em branco extras do início e fim da frase original
            cleaned_sentence_text = sentence.text.strip()
            
            # Pula linhas vazias ou quebras de texto sem conteúdo real
            if not cleaned_sentence_text:
                continue
                
            cleaned_tokens = []
            
            # Filtramos palavra por palavra dentro da frase
            for token in sentence:
                # 1. Forçamos o minúsculo (.lower()) através do token.lemma_.lower()
                # 2. Ignoramos Stop Words (artigos, preposições, "e", "o", "de")
                # 3. Ignoramos pontuações (pontos, vírgulas, exclamações)
                # 4. Mantemos apenas caracteres alfabéticos (evita números isolados e símbolos)
                if not token.is_stop and not token.is_punct and token.is_alpha:
                    # Usamos o lemma_ (forma canônica da palavra). Ex: "obrigações" vira "obrigação"
                    lemma_word = token.lemma_.lower()
                    cleaned_tokens.append(lemma_word)
            
            # Só adicionamos a frase se ela contiver alguma palavra relevante após o filtro
            if cleaned_tokens:
                processed_sentences.append({
                    "original_text": cleaned_sentence_text,
                    "tokens": cleaned_tokens
                })
                
        return processed_sentences