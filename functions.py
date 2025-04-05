# creating function file
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from cleantext import clean
import streamlit.components.v1 as component

def Copy_Text(text):
    """
    copy button to copy text
    """
    Html_Code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Copy Button</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <style>            
            p {{
                font-size: 18px;
                margin-bottom: 10px;
            }}
            .copy-link {{
                color: #6643b5;
                text-decoration: none;
                margin-top: 32px;
                margin-left: 13px;
                font-size: 20px;
                display: inline-flex;
                align-items: center;
                gap: 5px;
                position: relative;
                transition: background 0.3s;
                cursor: pointer;
            }}
            .copy-link:hover {{
                color: #8594e4;
            }}
            .tooltip {{
                position: absolute;
                top: -30px;
                left: 50%;
                transform: translateX(-50%);
                background: black;
                color: white;
                padding: 5px 10px;
                font-size: 12px;
                border-radius: 5px;
                opacity: 0;
                transition: opacity 0.3s, transform 0.3s;
            }}
            .show-tooltip {{
                opacity: 1;
                transform: translate(-50%, -10px);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <a href="#" class="copy-link" onclick="copyText(event)">
                <i class="fa-regular fa-copy"></i>
                <span class="tooltip" id="tooltip">Copied!</span>
            </a>
            <br>
            <br>
            <p id="text">{text}</p>
        </div>
        <script>
            function copyText(event) {{
                event.preventDefault();
                const text = document.getElementById("text").innerText;
                const textarea = document.createElement("textarea");
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand("copy");
                document.body.removeChild(textarea);
                
                const tooltip = document.getElementById("tooltip");
                tooltip.classList.add("show-tooltip");
                setTimeout(() => {{
                    tooltip.classList.remove("show-tooltip");
                }}, 1000);
            }}
        </script>
    </body>
    </html>
    """
    component.html(Html_Code,height=60,width=60)




def scrape_paragraphs(url, num_paragraphs):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, 'lxml')
        paragraphs = [p.get_text() for p in soup.find_all('p')[:num_paragraphs]]
        return paragraphs
    except Exception as e:
        st.warning(f"Error...\n{e}",icon="⚠️")
        return []


### text cleaning 
def Text_Cleaning(text:str)->str:
    """
    this function gives clean 
    text of the paragraphs , etc
    which makes easy to understand of the text
    """
    pattern = r'[`^]'
    cleaned_paragraph = re.sub(pattern, '', text)

    clean_text = clean(
        text=cleaned_paragraph,fix_unicode=True,
        to_ascii=True,
        no_line_breaks=False,
        keep_two_line_breaks=True
    )

    pattern = r'\[\d+\]'
    cleaned_text_output = re.sub(pattern, '', clean_text)
    return cleaned_text_output
