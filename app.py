from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import os
import requests

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Connection parameters
host = 'localhost'
port = '5432'
database_name = 'postgres'
username = 'postgres'
password = 'postgres'
#connection string for PostgreSQL
connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']

    response = get_response_from_script(question)

    return render_template('index.html', question=question, response=response)

def get_response_from_script(question):
    # logic for interacting with LangChain and OpenAI

    db = SQLDatabase.from_uri(connection_string)

    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo-1106", temperature=0, verbose=True)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    retrieved_data = db_chain.run(question)

    return retrieved_data

if __name__ == '__main__':
    app.run(debug=True)







