
import sys
import os
import datetime
import trafilatura
from llama_index import SimpleDirectoryReader
from llama_index import GPTVectorStoreIndex
import openai
import json
from typing import Union
from fastapi import FastAPI, UploadFile
from llama_index import StorageContext, load_index_from_storage

app = FastAPI()

os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = "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"
openai_api_key = "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"


class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        openai.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        query_engine = self.index.as_query_engine()
        response = query_engine.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message

    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)



@app.get("/support/{question}")
def read_root(question : str):
    #documents1 = SimpleDirectoryReader('./docs').load_data()
    #index1 = GPTVectorStoreIndex.from_documents(documents1)
    #index1.storage_context.persist()
    print('done')
    storage_context = StorageContext.from_defaults(persist_dir='./storage')
    index1 = load_index_from_storage(storage_context)
    bot = Chatbot("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", index=index1)
    print(question)
    response = bot.generate_response(question)
    print(response)
    return {"Answer": response['content']}

'''@app.post("/uploadfile/")
async def create_upload_file(ufile: UploadFile):
    file_location = f"/workspace/upwork/personal/docs/{ufile.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(ufile.file.read())
    documents1 = SimpleDirectoryReader('./docs').load_data()
    index1 = GPTVectorStoreIndex.from_documents(documents1)
    index1.storage_context.persist()
    return {"info" : f"'{ufile.filename}' is saved to GPT Index "}'''


@app.get("/")
def helper():
    return {"Intent":"Welcome To Chatbot"}

