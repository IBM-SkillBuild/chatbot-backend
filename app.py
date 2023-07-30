from flask import Flask,jsonify
import json
from rivescript import RiveScript
from fuzzywuzzy import fuzz


app=Flask(__name__)

with open('myjson.json', 'r', encoding='utf-8') as f:
    chatbot_data = json.load(f)
bot=RiveScript()    
bot.load_file('eduardo.rivescript')
bot.sort_replies()

@app.route("/")
def saludo():
    return jsonify({"version 1.1":"chatbot Cv-edu"})

@app.route("/chatbot/<string:pregunta>",methods=['GET'])
def chatbot(pregunta):
    user_input=str(pregunta)
    respuesta=bot.reply("localuser",user_input)
    return jsonify({"respuesta":respuesta})


if __name__=="__main__":
    app.run(debug=True,port=4000)
    