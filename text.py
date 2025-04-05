import streamlit as st
import re
from cleantext import clean
import streamlit.components.v1 as component
from transformers import pipeline
from functions import Copy_Text
from functions import *

# page settings 
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

### insert external css
def insert_css(css_file:str):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

# app settings css
insert_css("css_files/app.css")

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

# initilize session state
if 'summary' not in st.session_state:
    st.session_state.summary = []    

app_col = st.columns([2,8,2])

with app_col[1]:

    if select_mode == "Summarizer":
        st.write("## Text Summarizer")
    elif select_mode == "Que/Ans":
        st.write("## 📚 Text Question Answering")

#################### question answering ####################

if select_mode == "Que/Ans":
    app_c = st.columns([2,8,2])
    with app_c[0]:
        pass
    with app_c[1]:
        # Inject custom CSS to place the chat input at the bottom
        st.markdown(
            """
            <style>
                /* Fix the chat input box at the bottom */
                div[data-testid="stChatInput"] {
                    position: fixed;
                    bottom: 0;
                    margin-bottom: 36px;
                    
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        # Load model
        qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

        # Initialize session state 
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # User inputs context
        context = st.text_area("📜 Enter Text Hear", "", height=200)
        context = Text_Cleaning(context)

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


############ summarizer ###########

app_sum_col = st.columns([2,8,2])


# add session state
if 'summary' not in st.session_state:
    st.session_state.summary = []

with app_sum_col[1]:
    if select_mode == "Summarizer":
        Text_input = st.text_area(label="📜 Enter Text Hear",key="Summarizer input",height=220)
        Text_input = Text_Cleaning(Text_input)

        if Text_input.strip() != "":
            st.session_state.summary = []

            value_func = lambda x: x * 0.3 
            # max length
            max_tokens = st.slider(
                label="Max Length",
                key="max length",
                min_value=1,
                max_value=len(Text_input.split()),
                value=int(value_func(len(Text_input.split())))
            )

            if st.button(label="📄 Generate Summary "):
                try:
                    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                    st.session_state.summary = summarizer(
                        Text_input,
                        max_length=max_tokens+20, 
                        min_length=max_tokens, 
                        do_sample=False
                    )

                except Exception as e:
                    st.warning(f"Error...\n{e}",icon="⚠️")
                
                if st.session_state.summary:
                    with st.spinner("Generating Summary..."):
                        st.write("### Summary")
                        generated_summary = st.session_state.summary[0]['summary_text']
                        st.write(generated_summary)
                        Copy_Text(generated_summary)