import streamlit as st

### page setup

web_qna = st.Page(
    page="webscraper.py",
    title="web Scraper",
    icon=":material/globe:",
    default=True
)

text_qna = st.Page(
    page="text.py",
    title="Text Q&A , Summarizer",
    icon=":material/description:",
)

document_qna = st.Page(
    page="document.py",
    title="Document Q&A , Summarizer",
    icon=":material/picture_as_pdf:",
)



about_app = st.Page(
    page="about_app.py",
    title="About App",
    icon=":material/person:"
)

pg = st.navigation(
    pages=[web_qna,text_qna,document_qna,about_app],
    expanded=False,position="sidebar"
)
pg.run()

app_sidebar = st.sidebar

with app_sidebar:
    
    # project Link
    st.link_button(
        label="Project Link",
        url="https://github.com/Nishant43S/Gen-Ai-Summarizer-Question-Answering-App.git",
        icon=":material/code_off:",
        use_container_width=True
    )

### insert external css
def insert_css(css_file:str):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

# app settings css
insert_css("css_files/app.css")