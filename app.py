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

if __name__ == '__main__':
    app.run(debug=True)