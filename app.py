from flask import Flask,jsonify,send_file,make_response
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
    return jsonify({"version 1.1":"utilidades-edu"})

@app.route('/foto-mujer')
def get_foto_female():
    # URL de la API
    num_foto = random.randint(1, 99)
    url = f'https://randomuser.me/api/portraits/med/women/{num_foto}.jpg'

    # Hacer la solicitud GET
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un archivo en memoria
        img = BytesIO(response.content)
        img.seek(0)
        
        # Crear una respuesta personalizada para añadir los encabezados
        response = make_response(send_file(img, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        filepath = os.path.join(os.getcwd(), 'foto-mujer.jpeg')
        response = make_response(send_file(filepath, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

@app.route('/foto-hombre')
def get_foto_male():
    # URL de la API
    num_foto = random.randint(1, 100)
    url = f'https://randomuser.me/api/portraits/med/men/{num_foto}.jpg'

    # Hacer la solicitud GET
    response = requests.get(url)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un archivo en memoria
        img = BytesIO(response.content)
        img.seek(0)
        
        # Crear una respuesta personalizada para añadir los encabezados
        response = make_response(send_file(img, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        filepath = os.path.join(os.getcwd(), 'foto-hombre.jpeg')
        response = make_response(send_file(filepath, mimetype='image/jpeg'))
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return 



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


@app.route('/widget-hora-madrid')
def widget():
    return """
    <table>
    <tr><td style="text-align: center;"><canvas id="canvas_tt67b8c1c981673" width="175" height="175"></canvas></td></tr>
    <tr><td style="text-align: center; font-weight: bold"><a href="" style="text-decoration: none" class="clock24" id="tz24-1740161481-c1141-eyJzaXplIjoiMTc1IiwiYmdjb2xvciI6IjAwOTlGRiIsImxhbmciOiJlcyIsInR5cGUiOiJhIiwiY2FudmFzX2lkIjoiY2FudmFzX3R0NjdiOGMxYzk4MTY3MyJ9" title="Madrid Hora" target="_blank" rel="nofollow">Qué hora es Madrid</a></td></tr>
</table>
<script type="text/javascript" src="//w.24timezones.com/l.js" async></script>
  
    """


if __name__=="__main__":
    app.run(debug=True,port=4000)
    