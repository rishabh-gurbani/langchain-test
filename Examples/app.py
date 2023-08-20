from flask import Flask, request, jsonify
from langchain.chat_models import ChatOpenAI
from flask_cors import CORS
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
os.environ["OPENAI_API_KEY"] = ""

app = Flask(__name__)
CORS(app)


@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    print(user_message)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
    conversation = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory()
    )

    def predict(message):
        # Start the conversation
        conversation.predict(input=message)
        output = conversation.memory.dict()['chat_memory']['messages'][-1]['content']
        # output = """
        # I am an AI language model developed by OpenAI.
        # My purpose is to assist and engage in conversations with users like you.
        # I don't have a physical form, but I can provide information and answer
        # questions to the best of my abilities. How can I assist you today?
        # """
        print(output)
        return output

    return jsonify({'response': predict(message=user_message)})

if __name__ == '__main__':
    app.run(debug=True)
