from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)

# Usuários do sistema
users = {
    "administrador": "adminpass"
}

# Chave secreta para iniciar sessão do usuário
app.secret_key = "LDH2847BDFVAIB%#$@BASGHF1"

# Rotas de renderização
@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return f"Bem-vindo ao painel de controle, {session['username']}!"
    else:
        redirect(url_for('index_page'))

@app.route('/resultado-parcial')
def resultado_parcial():
    age = session.get('age')
    sex = session.get('sex')
    fator1 = session.get('fator-risco-1')
    fator2 = session.get('fator-risco-2')
    fator3 = session.get('fator-risco-3')
    fator4 = session.get('fator-risco-4')
    fator5 = session.get('fator-risco-5')
    fator6 = session.get('fator-risco-6')
    fator7 = session.get('fator-risco-7')
    fator8 = session.get('fator-risco-8')
    fator9 = session.get('fator-risco-9')
    return f"Resultado {age}, {sex} , {fator1} , {fator2} , {fator3} , {fator4} , {fator5} , {fator6} , {fator7} , {fator8} , {fator9}"

# Rotas de ações
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        session['username'] = username
        return jsonify({"success": True, "message":"Login bem-sucedido!"})
    else:
        return jsonify({"success": False, "message":"Nome de usuário ou senha incorretos."})

@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('index_page'))

# Rotas mistas
@app.route("/quiz-start", methods=['GET','POST'])
def quiz_start():
    if request.method == 'POST':
        session['age'] = request.form['age']
        session['sex'] = request.form['sex']
        return redirect(url_for('fatores_de_risco'))
    return render_template('quiz-start.html')

@app.route("/fatores-de-risco", methods=['GET','POST'])
def fatores_de_risco():
    if request.method == 'POST':
        session['fator-risco-1'] = request.form['fator-1']
        session['fator-risco-2'] = request.form['fator-2']
        session['fator-risco-3'] = request.form['fator-3']
        session['fator-risco-4'] = request.form['fator-4']
        session['fator-risco-5'] = request.form['fator-5']
        session['fator-risco-6'] = request.form['fator-6']
        session['fator-risco-7'] = request.form['fator-7']
        session['fator-risco-8'] = request.form['fator-8']
        session['fator-risco-9'] = request.form['fator-9']
        return redirect(url_for('resultado_parcial'))
    return render_template('quiz-fatores-risco.html')

if __name__ == '__main__':
    app.run(debug=True)