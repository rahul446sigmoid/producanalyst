import numpy as np
import pandas as pd
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
# from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
# from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os

instruction_existing= """
            Role: Product designer/developer at Kenvue, focusing on Neutrogena Hydro Boost Face Moisturizer.
            Goal: Understand customer sentiment on Neutrogena moisturizers.
            Sources: Prioritize feedback from customer reviews, social media posts, and community posts.
            Focus Areas: Effectiveness, cost, packaging, texture, and potential side effects.
            Approach: Ask for clarifications on vague feedback, but generally make educated guesses based on expertise.
            Communication: Maintain a formal and professional tone.
                """

output_format = """
                    Only give the information that have been asked donot include additional details
                    try to give the output in minimum words possible
                """

template_string = """Follw the instruction carefully {instruction_existing}
                    give the output according to the output format {output_format}
                    based on the user question {user_question}
                """

