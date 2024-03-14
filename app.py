import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import random
import string
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from  css import render_navbar
from prompt import instruction_existing,output_format,template_string
st.set_page_config(
        page_title="Sigmoid Style",
        layout="wide",
    )

render_navbar()

openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

llm_model = "gpt-4"
chat = ChatOpenAI(temperature=0.9, model=llm_model, openai_api_key=openai_api_key)

# col1,col2 = st.columns([0.6,0.4])
# with col1:
from streamlit_option_menu import option_menu
selected3 = option_menu(None, ['Product Analyst', "Product Designer"], 
    icons=['person', 'image'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#F15050"},
    }
)
if selected3 =="Product Analyst":
    def randon_string() -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


    def chat_actions():
        st.session_state["chat_history"].append(
            {"role": "user", "content": st.session_state["chat_input"]},
        )
        prompt_template = ChatPromptTemplate.from_template(template_string)
        customer_messages = prompt_template.format_messages(
            
            instruction_existing=instruction_existing,
            output_format=output_format,
            user_question =st.session_state["chat_input"]
            )
        customer_response=chat(customer_messages)
        st.session_state["chat_history"].append(
            {
                "role": "assistant",
                "content": customer_response.content,
            },  # This can be replaced with your chat response logic
        )


    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


    st.chat_input("Enter your message", on_submit=chat_actions, key="chat_input")

    for i in st.session_state["chat_history"]:
        with st.chat_message(name=i["role"]):
            st.write(i["content"])

if selected3 =="Product Designer":

    def generate_image(image_inst,brand,product,type):
        image_prompt = f''' create an image for the packaging for a {product} \
                        that has the brand name { brand} clearly shown on it. \
                        The packaging should capture the main features {image_inst}, \
                        the product should be for {type} customer also take refrence from the internet for 
                        product design and logo of given {brand} make sure to include the brand name in pic {brand}'''

        # Generate image using OpenAI API
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Get the URL of the generated image
        image_url = response.data[0].url
        return image_url

    def main():
        # Text input for image description
        with st.container(border=True,height=150):
            col1,col2,col3 = st.columns(3)
            with col2:
            # Select Channel
                neutrogena_products = [
                    "Water Gel",
                    "Fash Wash",
                    "Moisturizer"]

                selected_product = st.selectbox("Select Product Type", neutrogena_products)

            with col1:
            
                selected_brand = st.selectbox("Brand Name", ["Neutrogena","Other"])
                  

            with col3:
               
                selected_type = st.selectbox("Select Type",["Traditional","Genz"])
    
        image_inst = st.text_input(label="How you want your image")

        if st.button("Generate Image"):
            # Check if input is provided
            if image_inst:
                # Generate and display the image
                image_url = generate_image(image_inst,selected_brand,selected_product,selected_type)
                st.image(image_url, caption="Generated Image", use_column_width=True)
            else:
                st.warning("Please provide a description for the image.")

    if __name__ == "__main__":
        main()