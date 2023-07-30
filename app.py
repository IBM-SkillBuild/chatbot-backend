from flask import Flask,jsonify
from flask_cors import CORS, cross_origin
import json
from rivescript import RiveScript
from fuzzywuzzy import fuzz
from langdetect import detect


app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

with open('myjson.json', 'r', encoding='utf-8') as f:
    chatbot_data = json.load(f)
bot=RiveScript()    
bot.load_file('eduardo.rivescript')
bot.sort_replies()

@app.route("/")
def saludo():
    return jsonify({"version 1.1":"chatbot Cv-edu"})

@app.route("/chatbot/<string:pregunta>",methods=['GET'])
@cross_origin()
def chatbot(pregunta):
    user_input=str(pregunta)
    idioma=detect(user_input)
    if user_input.lower()=="hello":
      idioma="en"
    if user_input.lower()=="help":
      idioma="en"
      
    mejor_coincidencia=chatbot_data['datos'][0]['pregunta']
    mejor_respuesta=chatbot_data['datos'][0]['respuesta']  
    mejor_accion=chatbot_data['datos'][0]['accion'] 
    mejor_ejecucion=chatbot_data['datos'][0]['path'] 
    mejor_url=chatbot_data['datos'][0]['url'] 
         
       
        
    porcentaje_obtenido=0
                                                  
    for question in chatbot_data['datos']:
        porcentaje_iterado=fuzz.token_sort_ratio(user_input,question['pregunta'])+\
        fuzz.partial_ratio(user_input,question['respuesta'] ) 
            
           
        if porcentaje_iterado>porcentaje_obtenido:
            
            mejor_coincidencia=question['pregunta']
            mejor_respuesta=question['respuesta']
            mejor_accion=question['accion']
            mejor_ejecucion=question['path']
            mejor_url=question['url']
            mejor_seguridad=question['seguridad']
            porcentaje_obtenido=porcentaje_iterado
            if porcentaje_obtenido>90:
                respuesta = str(mejor_respuesta) 
            else:
                respuesta=bot.reply("localuser",user_input)
                
    return jsonify(respuesta=respuesta,idioma=idioma)


if __name__=="__main__":
    app.run(debug=True,port=4000)
    