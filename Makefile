init:
        poetry env use python3.10
        poetry shell
        poetry install

run:
        streamlit run src/app.py