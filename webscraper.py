import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from cleantext import clean
import streamlit.components.v1 as component
from transformers import pipeline
from functions import Copy_Text
from functions import *

### import animation
def particle(Js_file):
    with open(Js_file) as f:
        component.html(f"{f.read()}", height=400)

### insert external css
def insert_css(css_file:str):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)


# page settings
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# sidebar
app_sidebar = st.sidebar
with app_sidebar:
    select_mode = st.selectbox(
        label="Select Mode",
        options=["Summarizer","Que/Ans"],
        key="mode selector",
        index=0
    )

    if select_mode == "Que/Ans":
        st.write("### Que/Ans Settings")

        max_answer_length = st.slider(
            label="Max answer",
            min_value=1,
            max_value=10,
            key="max answer",
            value=4
        )

        max_answer_length = max_answer_length*10

        Best_size = st.slider(
            label="n best size",
            min_value=1,
            max_value=10,
            key="best size",
            value=5
        )

# Initialize session state
if 'scraped_paragraphs' not in st.session_state:
    st.session_state.scraped_paragraphs = []
if 'summarizer_mode' not in st.session_state:
    st.session_state.summarizer_mode = False
if 'summary' not in st.session_state:
    st.session_state.summary = []

app_col = st.columns([2,8,2],gap="small")

with app_col[0]:
    pass

with app_col[2]:
    pass

with app_col[1]:
    # Title
    st.write("## GenAi Scraper")

    # Input URL
    url_input = st.text_input(label="Enter Website URL",key="url input",placeholder="https://www.example.com")

    # number of paragraphs
    num_paragraphs = st.slider("Select number of paragraphs to scrape", 1, 30, 5)

    scrap_btn = st.button("Scrape Paragraphs",key="scrap button")

    if url_input.strip() == "" and not scrap_btn:
        # animation
        particle("animation/particles.html")

    else:
        if scrap_btn:
            st.session_state.scraped_paragraphs = scrape_paragraphs(url_input, num_paragraphs)
            st.session_state.summary = []  # Reset summary

        # Display scraped paragraphs
        if st.session_state.scraped_paragraphs:
            
            st.write("### Scraped Paragraphs")
            
            paragraph_scrap = "\n\n".join(st.session_state.scraped_paragraphs)
            st.write(Text_Cleaning(paragraph_scrap))

            Copy_Text(Text_Cleaning(paragraph_scrap)) ## copy text
        
        #################### summarizer  #############

        if select_mode == "Summarizer":    
            if st.session_state.scraped_paragraphs:
                # Toggle for summarization mode
                st.session_state.summarizer_mode = st.toggle("Enable Summarizer Mode", st.session_state.summarizer_mode)
                    
                if st.session_state.summarizer_mode:
                    value_func = lambda x: x * 0.3 
                    max_tokens = st.slider(label="Select Max Token Length", min_value=10, 
                                    max_value=sum(len(p.split()) for p in st.session_state.scraped_paragraphs), 
                                    value=int(value_func(
                                        sum(len(p.split()) for p in st.session_state.scraped_paragraphs)
                                    ))
                                )
                    if st.button("📄 Generate Summary"):
                        with st.spinner("Generating Summary..."):
                            try:
                                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                                st.session_state.summary = summarizer(
                                    Text_Cleaning(" ".join(st.session_state.scraped_paragraphs)),
                                    max_length=max_tokens+20, 
                                    min_length=max_tokens, 
                                    do_sample=False
                                )

                            except Exception as e:
                                st.warning(f"Error...\n{e}",icon="⚠️")
                    
                # Display summary 
                if st.session_state.summary:
                    st.write("### Summary")
                    generated_summary = st.session_state.summary[0]['summary_text']
                    st.write(generated_summary)
                    Copy_Text(generated_summary)
            else:
                st.info("unable to scrap this website")
        
        ################# question answering #####################

        elif select_mode == "Que/Ans":
            if st.session_state.scraped_paragraphs:
                if st.toggle(label="Question Answering",key="Q/A"):
                    # Inject custom CSS to place the chat input at the bottom
                    st.markdown(
                        """
                        <style>
                            /* Fix the chat input box at the bottom */
                            .stColumn.st-emotion-cache-115gedg.e1f1d6gn3 div[data-testid="stChatInput"] {
                                position: fixed;
                                bottom: 0;
                                margin-bottom: 36px;
                                max-width: 100%;
                            }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

                    # Initialize session state 
                    if "messages" not in st.session_state:
                        st.session_state.messages = []

                    # User inputs context
                    context = Text_Cleaning(paragraph_scrap)

                    # Display chat history
                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])

                    if context:
                        user_input = st.chat_input("💬 Ask a question ",)
                        if user_input:
                            with st.chat_message("user"):
                                st.markdown(user_input)
                                    
                            st.session_state.messages.append({"role": "user", "content": user_input})
                                    
                            with st.spinner("🤔 Thinking..."):
                                response = qa_pipeline({"question": user_input, "context": context},
                                                       max_answer_len=max_answer_length, n_best_size=Best_size)
                                answer = response["answer"]
                                    
                                with st.chat_message("assistant"):
                                    st.markdown(f"{answer}")
                                    
                                st.session_state.messages.append({"role": "assistant", "content": f"{answer}"})

                        # Clear chat history button
                        if st.button("🗑️ Clear Chat"):
                            st.session_state.messages = []
                            st.rerun()

            else:
                st.info("unable to scrap this website")

# app settings css
insert_css("css_files/app.css")
