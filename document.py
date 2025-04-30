import streamlit as st
from functions import *
from transformers import pipeline
from pdfminer.high_level import extract_text
import os
import PyPDF2
import base64



#### chatbot function

def Chat_Bot(text_input,Best_size,max_answer_length):
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
    # Load the Question Answering model
    qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []


    # User inputs context
    context = text_input

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if context:
        user_input = st.chat_input("💬 Ask a question based on the context:")
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("🤔 Thinking..."):
                response = qa_pipeline(
                    {"question": user_input, "context": context},
                    max_answer_len=max_answer_length, n_best_size=Best_size
                )
                answer = response["answer"]
            
            with st.chat_message("assistant"):
                st.markdown(f"{answer}")
            
            st.session_state.messages.append({"role": "assistant", "content": f"{answer}"})

    # Clear chat history button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


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





#### displaying uploaded pdf file
def display_pdf_file(uploaded_file):
    """
    it is used to display the
    file on screen
    """
    #### saving the uploaded file
    def save_uploadfile(save_file):
        with open(os.path.join("data",save_file.name),"wb") as f:
            f.write(save_file.getbuffer())
            return st.toast("file uploaded: {}".format(save_file.name))
        
    try:
        ### display pdf on screen
        def displayPDF(pdf_file):
            with open(pdf_file,"rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode("utf-8")

            pdf_display = f"""
                <iframe
                    src="data:application/pdf;base64,{base64_pdf}"
                    width="950" height="1000"
                    type="application/pdf"
                >
                </iframe>
            """

            st.markdown(pdf_display,unsafe_allow_html=True)

        ### save and display file
        save_uploadfile(uploaded_file)
        pdf_file = "data/"+uploaded_file.name
        displayPDF(pdf_file)
    except Exception as e:
        st.warning("Something Went wrong...\n\n",e,icon="⚠️")


# --- PDF Page Text Extractor Function ---
def extract_text_from_pdf(pdf_file, page_num):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        total_pages = len(reader.pages)
        if 1 <= page_num <= total_pages:
            page = reader.pages[page_num - 1]  # Adjusting for 0-based index
            text = page.extract_text()
            return text, total_pages
        else:
            return None, total_pages
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None, 0

def pdf_page_text(file):

    temp_reader = PyPDF2.PdfReader(file)
    total_pages = len(temp_reader.pages)
    st.write(f"### Total Pages: {total_pages}")

    ## columns
    Input_col = st.columns([4,10])
    with Input_col[0]:
        page_number = st.number_input(
            "Select page number", 
            min_value=1, max_value=total_pages,
            value=1, step=1)
        st.write("Page Number {}".format(page_number))
    text, _ = extract_text_from_pdf(file, page_number)
    return text


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

        Best_size_ = st.slider(
            label="n best size",
            min_value=1,
            max_value=10,
            key="best size",
            value=5
        )

def Summarizer_Model(context,Max_Length):
    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        Summary = summarizer(
            context,
            max_length=Max_Length+20, 
            min_length=Max_Length, 
            do_sample=False
        )
        return Summary[0]['summary_text']

    except Exception as e:
        st.warning(f"Error...\n{e}",icon="⚠️")

app_col = st.columns([2,8,2])

with app_col[1]:

    if select_mode == "Summarizer":
        st.write("## 📑 Document Summarizer")
    elif select_mode == "Que/Ans":
        st.write("## 📑 Document Question Answering")

### question answering 
que_col = st.columns([2,8,2])

with que_col[1]:
    if select_mode == "Que/Ans":
        ## input file
        File_input = st.file_uploader(
            label="Drop Your File hear",
            type=["txt", "pdf"],
            key="file uploader"
        )

        if File_input is not None:
            if File_input.type == "text/plain":
                text = File_input.read().decode("utf-8")
                Chat_Bot(
                    text_input=Text_Cleaning(text),
                    Best_size=Best_size_,
                    max_answer_length=max_answer_length
                )
            else:
                file_Display_tab, Pdf_Que_ans_tab = st.tabs(["Pdf Display","PDF Que/Ans"])

                with file_Display_tab:
                    with st.spinner("Loading File..."):
                        display_pdf_file(File_input)
                with Pdf_Que_ans_tab:
                    st.session_state.pdf_text_que_ans = []
                    st.session_state.pdf_text_que_ans  = pdf_page_text(File_input)
                    st.text_area(
                            "Pdf Text",value=Text_Cleaning(st.session_state.pdf_text_que_ans),
                            key="text area que and ans",height=300
                        )
                    Chat_Bot(
                        text_input=Text_Cleaning(st.session_state.pdf_text_que_ans),
                        Best_size=Best_size_,
                        max_answer_length=max_answer_length
                    )

# session state
if 'input_text' not in st.session_state:
    st.session_state.input_text = []

if 'pdf_text' not in st.session_state:
    st.session_state.pdf_text = []

if 'summary_text' not in st.session_state:
    st.session_state.summary_text = []

summ_col = st.columns([2,8,2])

with summ_col[1]:
    if select_mode == "Summarizer":
        ## input file
        File_input = st.file_uploader(
            label="Drop Your File hear",
            type=["txt", "pdf"],
            key="file uploader"
        )
        if File_input is not None:
            if File_input.type == "text/plain":
                text = File_input.read().decode("utf-8")
                st.session_state.input_text = []
                st.session_state.input_text = st.text_area(label="Uploaded document Text",value=Text_Cleaning(text),height=200)
                Text_input = Text_Cleaning(st.session_state.input_text)
                value_func = lambda x: x * 0.3 
                max_length = st.slider(
                    label="Max Length",min_value=1,
                    max_value=len(st.session_state.input_text.split()),
                    value=int(value_func(len(st.session_state.input_text.split())))
                )

                if st.button(label="📄 Generate Summary"):
                    with st.spinner("Generating Summary"):

                        Generated_Summary = Summarizer_Model(context=Text_input,Max_Length=max_length)
                        st.write(Generated_Summary)
                        Copy_Text(Generated_Summary)
            
            else:
                pdf_Display_tab, Pdf_Summarizer_tab = st.tabs(["Pdf Display","PDF Summarizer"])
                with pdf_Display_tab:
                    with st.spinner("Loading File..."):
                        display_pdf_file(File_input)
                with Pdf_Summarizer_tab:
                        
                    st.session_state.pdf_text = []
                    st.session_state.summary_text = []
                    st.session_state.pdf_text = pdf_page_text(File_input)

                    ## text area
                    Text_Area_Input = st.text_area(
                        "Pdf Text",value=Text_Cleaning(st.session_state.pdf_text),
                        key="text area",height=450
                    )

                    value_func = lambda x: x * 0.3 
                    Max_Pdf_Summary_len = st.slider(
                        label="MAx Length",
                        min_value=1,
                        max_value=len(Text_Area_Input.split()),
                        value=int(value_func(len(Text_Area_Input.split()))),
                        key="pdf summarizer Slider"
                    )
                
                    if st.button("📑 Generate Summary",key="pdf Summary"):
                        # generating summary
                        with st.spinner("Generating Summary"):
                            ## initilizing model
                            st.session_state.summary_text = Summarizer_Model(
                                context=Text_Area_Input,Max_Length=Max_Pdf_Summary_len
                            )

                            st.write(st.session_state.summary_text)
                            Copy_Text(st.session_state.summary_text)
