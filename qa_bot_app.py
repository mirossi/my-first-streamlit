import streamlit as st
import openai
import yaml

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


#credentials
try:
  with open("chatgpt_api_credentials.yml",'r') as file:
    creds= yaml.safe_load(file)
except:
  creds={}


with st.sidebar:
  openapi_api_key= creds.get("openai_key",'')
  if openapi_api_key:
    st.text("OpenAI API Key Provided")
  else:
    openapi_api_key= st.text_input("Please provide our OpenAI API Key")
    #Hyperlink
    "[Get an OpenAI API key](https://openai.com/blog/openai-api)"


st.title ("File Q&A with ChatGPT")
# File Uploader
uploaded_file=st.file_uploader("Upload the article", type = ("txt", "md","pdf")) 
st.write("## file")



#User Text Input
question= st.text_input("Ask something about this article", placeholder="summarize")

#Parse text
if uploaded_file and question and openapi_api_key:
  if uploaded_file.name[-3:].lower()=="pdf":
    output_string = StringIO()
    parser = PDFParser(uploaded_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)
    article=output_string.getvalue()
  else:
    article= uploaded_file.read().decode()

  #st.text(article)

  #Prompting
  my_prompt=f"Here is the article: {article}. \n\n{question}"
  #st.text("======")
  #st.text(my_prompt)


  openai.api_key=openapi_api_key
  response = openai.Completion.create(
    model= "gpt-3.5-turbo-instruct", 
    prompt = my_prompt,
    max_tokens=500)



  st.write("## Answer")
  st.write(response["choices"][0]["text"])





