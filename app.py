from flask import Flask,jsonify
import json


app=Flask(__name__)

@app.route("/chatbot/<string:pregunta>",methods=['GET'])
def chatbot(pregunta):
    respuesta="lo que encuentre en la busqueda"
    return jsonify({"respuesta":respuesta})


if __name__=="__main__":
    app.run(debug=True,port=4000)
    