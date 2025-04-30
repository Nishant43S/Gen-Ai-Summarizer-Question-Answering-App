# 🧠 Generative AI Question Answering & Summarizer App

This is a Generative AI-powered application for extracting insights from various types of content using **Question Answering** and **Summarization** capabilities. The app is built with **Streamlit** and hosted on **Hugging Face Spaces**. It supports multiple input types (text, PDF, web URLs) and is powered by advanced models such as:

- 🧾 **Summarizer**: `facebook/bart-large-cnn`
- ❓ **Question Answering**: `deepset/roberta-base-squad2`

---

## 🚀 Features

### 🔍 1. Web Scraper + Q&A + Summarizer
- Enter a URL to extract content
- Ask custom questions or summarize the webpage content

### 📝 2. Text Mode
- Input plain text
- Generate summaries or ask questions

### 📄 3. PDF & TXT Upload
- Upload `.pdf` or `.txt` files
- Summarize or ask questions from the file content

---

## 🛠️ Custom Controls (Q&A Mode)
- **N-Best Size**: Number of best predictions to return
- **Max Answer Length**: Maximum length of the answer in tokens

---

## 🧠 Models Used
- **Summarization**: `facebook/bart-large-cnn`
- **Q&A**: `deepset/roberta-base-squad2`

---

## 🌐 Hosted On
[Hugging Face Spaces](https://huggingface.co/spaces/)  
(Search for your app name there or add the direct link if available.)

---

## 💻 Run Locally

### 🔧 Requirements

Ensure Python 3.7+ is installed.

To run this project locally, use the following commands:

```bash
  git clone https://github.com/Nishant43S/file-link-Generator.git
```

```bash
  pip install -r requirements.txt
```
to run

```bash
  python -m streamlit run app.py
```
