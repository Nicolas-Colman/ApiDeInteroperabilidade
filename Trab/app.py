from flask import Flask, json, render_template, request, redirect, jsonify
import sqlite3
import requests

ingresso = Flask(__name__, template_folder='.')

@ingresso.route('/Verifica', methods=['POST'])
def Verifica():
    txt = request.get_data()
    obj = json.loads( txt )
    cpf = obj['cpf']

    obj = {'cpf' : cpf}
    txt = json.dumps(obj)
    ret1 = requests.post(url='http://localhost:5001/autenticacao', data=txt)
    txt1 = ret1.content
    obj1 = json.loads(txt1)
    
    if obj1['valido']:
        txt = { 'cpf' : obj['cpf'], 'arquivo'  : obj1['valido']}
        obj = json.dumps(txt)
        return obj



    ret2 = requests.post(url='http://172.26.3.187:5002/autenticacao', data=txt)
    txt2 = ret2.content
    obj2 = json.loads(txt2)
    
    if obj2['status']:
        txt = { 'cpf' : obj['cpf'], 'arquivo'  : obj2['status']}
        obj = json.dumps(txt)
        return obj

    
    else:
        txt = {'arquivo' : False}
        obj = json.dumps(txt)
    return obj


        



ingresso.run(port=5002, use_reloader=True)

