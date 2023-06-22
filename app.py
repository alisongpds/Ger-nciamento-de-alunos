from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'escola_pa_2023'

db = sqlite3.connect('db_alunos.db', check_same_thread=False)
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS professor (
        email TEXT NOT NULL,
        senha TEXT NOT NULL             )
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS aluno (
        nome TEXT NOT NULL,
        ra INTEGER NOT NULL PRIMARY KEY,
        curso TEXT NOT NULL            )
''')
db.commit()

@app.route('/')
def home():
    session['usuario_logado'] = None
    return render_template('home.html')

@app.route('/cadastro')
def cadastro():
    return render_template('index.html')

@app.route('/cadastrar_user',methods=['POST','GET'],)

def cadastrar_user():
    email = request.form['email']
    senha = request.form['senha']

    # Insere os dados na tabela de usuários
    cursor.execute('''
        INSERT INTO professor (email,senha)
        VALUES (?,?)
    ''', (email,senha)) 
    db.commit()

    return redirect(url_for('home'))

@app.route('/login')

def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST','GET'])
def autenticar():

    email = request.form['email']
    senha = request.form['senha']

    # Verifica se o email e senha estão cadastrados no banco de dados
    cursor.execute('''
        SELECT * FROM professor WHERE email = ? AND senha = ?
    ''', (email, senha))
    usuario = cursor.fetchone()

    if usuario:
        session['usuario_logado'] = email
        flash(' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        if proxima_pagina=='/':
            proxima_pagina = '/home'

        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
    
@app.route('/home')
def home_logged():
    if 'usuario_logado' not in session or session['usuario_logado'] == None: 
         return redirect(url_for('login', proxima=url_for('home_logged'))) 
    else:
        return render_template('home_logado.html')

app.run(debug=True)