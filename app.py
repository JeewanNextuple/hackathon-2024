from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Connection parameters
host = 'localhost'
port = '5432'
database_name = 'hackathon'
username = 'postgres'
password = 'postgres'
#connection string for PostgreSQL
connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database_name}'


@app.route('/ask', methods=['POST'])
def ask():

    data = request.get_json()
    question = data['question']
    response = get_response_from_script(question)
    return response

def get_response_from_script(question):
    
    QUERY = """For a given input statement or question: {}, create a SQL query and return the results according to the following conditions:
1. If the input asks to give results in a certain format like table, then return the result in JSON format.
2. If the input does not specify the format, then return a normal answer.
3. If the resultant query is responding with records then return the result as array of JSON"""

    QUERY = QUERY.format(question)

    db = SQLDatabase.from_uri(connection_string)

    llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo-1106", temperature=0, verbose=True)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    retrieved_data = db_chain.run(QUERY)

    return retrieved_data

if __name__ == '__main__':
    app.run(debug=True)







