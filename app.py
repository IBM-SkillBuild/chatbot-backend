from flask import Flask,jsonify,send_file
from flask_cors import CORS, cross_origin
import json
from rivescript import RiveScript
from fuzzywuzzy import fuzz
import requests
from io import BytesIO
import random,os


app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route("/")
def saludo():
    return jsonify({"version 1.1":"chatbot Cv-edu"})

@app.route('/foto-mujer')
def get_foto_female():
    # URL de la API
    num_foto = random.randint(1, 99)
    url = f'https://randomuser.me/api/portraits/med/women/{num_foto}.jpg' #
   
    # Hacer la solicitud GET
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un archivo en memoria
        img = BytesIO(response.content)
        img.seek(0)
        return send_file(img, mimetype='image/jpeg')
    else:
        filepath = os.path.join(os.getcwd(), 'foto-mujer.jpeg')
        return send_file(filepath, mimetype='image/jpeg')

@app.route('/foto-hombre')
def get_foto_male():
    # URL de la API
    num_foto = random.randint(1, 100)
    url = f'https://randomuser.me/api/portraits/med/men/{num_foto}.jpg' #
   
    # Hacer la solicitud GET
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un archivo en memoria
        img = BytesIO(response.content)
        img.seek(0)
        return send_file(img, mimetype='image/jpeg')
    else:
       filepath = os.path.join(os.getcwd(), 'foto-hombre.jpeg')
       return send_file(filepath, mimetype='image/jpeg')   



@app.route("/chatbot/<string:pregunta>",methods=['GET'])
@cross_origin()
def chatbot(pregunta):
    with open('myjson.json', 'r', encoding='utf-8') as f:
         chatbot_data = json.load(f)
    bot=RiveScript()    
    bot.load_file('eduardo.rivescript')
    bot.sort_replies()
    user_input=str(pregunta)
    
      
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
            
    return jsonify(respuesta=respuesta,idioma="es")


if __name__=="__main__":
    app.run(debug=True,port=4000)
    