# ChatPDF LangChain HR App

![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-informational?style=for-the-badge&logo=streamlit)
![LangChain](https://img.shields.io/badge/Powered%20by-LangChain-blue?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/Uses-OpenAI%20API-ff7f00?style=for-the-badge)

## Overview

The ChatPDF LangChain HR App is a language model-powered chatbot designed for Human Resources professionals. It allows you to upload a candidate's resume in PDF format and ask questions about the candidate's qualifications. The app leverages LangChain for text processing and the OpenAI API for question answering.

## Getting Started

Follow these steps to set up and use the app:

1. Clone the project repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/chatpdf-langchain-hr-app.git
   cd chatpdf-langchain-hr-app

1. Install the required dependencies using [Poetry](https://python-poetry.org/):
``` bash
poetry install
```
2. Create a virtual environment and activate it:
```bash
poetry shell
```
3. Create a file named `.env` in the project directory to store your OpenAI API key. Add your OpenAI API key to this file:
```bash
OPENAI_API_KEY=your_api_key_here
```
4. Run the app:
```bash
streamlit run src/app.py
```
5. Access the app in your web browser by following the URL displayed in your terminal.

# Usage

1. Upload a candidate's resume in PDF format.
2. In the text input field, ask questions about the candidate's qualifications in English.
3. The app will process the resume, answer your questions, and display the HR evaluation.

# Why This Project?

- **Efficient Candidate Evaluation**: HR professionals can quickly evaluate candidates' qualifications by asking specific questions about their resumes, saving time in the hiring process.

- **Language Model-Powered**: The app leverages OpenAI's language model and `LangChain` for advanced text processing, making it highly accurate in understanding and answering questions.
- **User-Friendly**: The interface is designed to be user-friendly, allowing HR professionals to upload resumes and ask questions with ease.
- **Customization**: You can further customize the app's appearance and functionality according to your HR team's needs.

Give it a try and make your candidate evaluation process more efficient and data-driven!

# License

This project is licensed under the [MIT](https://opensource.org/license/mit/) License

Made with ❤️ by [Pedro Alves](https://www.linkedin.com/in/pedro-a-d-s/)