import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import LLamaLLMChain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title('Cold Email Generator')
    url = st.text_input('Enter a URL:')

    submit_button = st.button('Submit')

    if submit_button:
         if submit_button:
            try:
                loader = WebBaseLoader([url])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_job_details(data)
                print(jobs)
                print()
                for job in jobs:
                    print(job)
                    skills = job.get('skills', [])
                    tasks = job.get('tasks', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_email(job, tasks, links)
                    st.code(email, language='markdown')
                    print()
            except Exception as e:
                st.error(f"Error Occurred: {e}")


if __name__ == "__main__":
    chain = LLamaLLMChain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)