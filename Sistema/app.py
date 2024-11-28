from flask import Flask, request, json, render_template, redirect
import sqlite3
import base64
import requests

app = Flask( import_name=__name__, template_folder='.' )

@app.route('/lista', methods=['GET'])
def lista():
    sql = "select cpf, arquivo from arquivo; "
    conexao = sqlite3.connect('banco')
    resultado = conexao.execute(sql).fetchall()
    return render_template('lista.html', imagens=resultado)

@app.route('/cadastro', methods=['GET'])
def cadastro():
    return render_template('cadastro.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    cpf = request.values.get('cpf')
    arquivo = request.files['imagem']
    binario = arquivo.read()
    codificado = base64.b64encode(binario).decode('utf-8')
    sql = f" insert into arquivo values ( '{cpf}', '{codificado}' ); "
    conexao = sqlite3.connect('banco')
    resultado = conexao.execute(sql)
    conexao.commit()
    conexao.close()
    return redirect('/lista')

@app.route('/busca', methods=['GET', 'POST'])
def busca():
    if request.method == 'POST':
        cpf = request.values.get('cpf')
        sql = f'''
	    	select * from arquivo
	    	where cpf = '{cpf}'
	    '''
        conexao = sqlite3.connect('banco')
        resultado = conexao.execute(sql).fetchall()
        if len(resultado) > 0:
            obj = {'cpf' : resultado[0][0] , 'arquivo' : resultado [0][1]}
            return render_template('valida.html', imagens=obj)
        else:
            cpf = {"cpf" : cpf}
            txt = json.dumps(cpf)
            ret = requests.post(url='http://localhost:5002/Verifica', data=txt)         
            txt = ret.content  
            print(txt)       
            obj = json.loads(txt)
            if obj:
                print (obj)
                return render_template('valida.html', imagens=obj)

        txt = json.dumps( obj )
        return txt

    elif request.method == 'GET':
        return render_template('busca.html')

@app.route('/autenticacao', methods=['POST'])
def autenticacao():
    txt = request.get_data()
    obj = json.loads( txt )
    print(obj)
    cpf = obj["cpf"]

    sql = f'''
		select * from arquivo
		where cpf = '{cpf}'
	'''
    conexao = sqlite3.connect('banco')
    resultado = conexao.execute(sql).fetchall()
    obj = { "valido" : False }
   
    if len(resultado) > 0:
        obj = {"valido" : resultado [0][1]}
    txt = json.dumps( obj )
    return txt


app.run( host='0.0.0.0', port=5001, use_reloader=True )