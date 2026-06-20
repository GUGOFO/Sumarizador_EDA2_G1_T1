#!/bin/bash
echo "Analisando ambiente e configurando o projeto de EDA 2..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 -m spacy download pt_core_news_sm
echo "Tudo pronto! Para rodar, use: source venv/bin/activate && python src/main.py --arquivo <nome_do_arquivo>.txt"