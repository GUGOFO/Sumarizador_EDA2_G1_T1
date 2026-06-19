@echo off
echo Configurando o ambiente virtual e instalando dependencias de EDA 2...
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
echo Tudo pronto! Para rodar, use: venv\Scripts\activate && python src/main.py --arquivo <nome_do_arquivo>.txt
pause