from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)

# Usuários do sistema
users = {
    "administrador": "adminpass"
}

# Chave secreta para iniciar sessão do usuário
app.secret_key = "LDH2847BDFVAIB%#$@BASGHF1"

# Configuracao da planilha
def salvar_dados_excel():
    try:
        caminho_arquivo = os.path.join(os.getcwd(), 'static', 'dados_quiz.xlsx')
    except Exception as e:
        return e

    # Verificar se o arquivo já existe
    if os.path.exists(caminho_arquivo):
        try:
            # Se o arquivo existir, carregue os dados existentes
            df_existente = pd.read_excel(caminho_arquivo)
        except Exception as e:
            return e
        
    else:
        try:
            # Se o arquivo não existir, crie um DataFrame vazio
            df_existente = pd.DataFrame()
        except Exception as e:
            return e

    dados_quiz = {
        'Email': [session.get('email')],
        'Idade': [session.get('age')],
        'Sexo': [session.get('sex')],
        'Fator-risco-1': [session.get('fator-risco-1')],
        'Fator-risco-2': [session.get('fator-risco-2')],
        'Fator-risco-3': [session.get('fator-risco-3')],
        'Fator-risco-4': [session.get('fator-risco-4')],
        'Fator-risco-5': [session.get('fator-risco-5')],
        'Fator-risco-6': [session.get('fator-risco-6')],
        'Fator-risco-7': [session.get('fator-risco-7')],
        'Fator-risco-8': [session.get('fator-risco-8')],
        'Fator-risco-9': [session.get('fator-risco-9')],
        'Fator-Identificacao-1': [session.get('fator-identificacao-avc-1')],
        'Fator-Identificacao-2': [session.get('fator-identificacao-avc-2')],
        'Fator-Identificacao-3': [session.get('fator-identificacao-avc-3')],
        'Tentativas-Identificacao-AVC': [session.get('tentativas-identificacao-avc')],
        'Fator-Tratamento-1': [session.get('fator-tratamento-avc-1')],
        'Fator-Tratamento-2': [session.get('fator-tratamento-avc-2')],
        'Fator-Tratamento-3': [session.get('fator-tratamento-avc-3')],
        'Fator-Tratamento-4': [session.get('fator-tratamento-avc-4')],
        'Fator-Tratamento-5': [session.get('fator-tratamento-avc-5')],
        'Tentativas-Tratamento-AVC': [session.get('tentativas-tratamento-avc')],
        'Resultado-Fator-Risco':[session.get('resultado-fatores-risco')],
        'Resultado-Identificacao':[session.get('resultado-identificacao-avc')],
        'Resultado-Tratamento':[session.get('resultado-tratamento-avc')]
    }



    try:
        df_novo = pd.DataFrame(dados_quiz)
    except Exception as e:
            return e
    
    try:
        df_resultante = pd.concat([df_existente, df_novo], ignore_index=True)
    except Exception as e:
            return e
    
    try:
        df_resultante.to_excel(caminho_arquivo, index=False)
        session.pop('tentativas-identificacao-avc', None)
        session.pop('tentativas-tratamento-avc', None)
    except Exception as e:
            return e

# Rotas de renderização
@app.route("/")
def index_page():
    return render_template('index.html')

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        return render_template('dados-plataforma.html')
    else:
        redirect(url_for('index_page'))

@app.route('/resultado-fatores-risco')
def resultado_fatores_risco():
    if session['resultado-fatores-risco'] == 'ruim':
        imagem = 'fatores-risco-resultado-ruim.JPG'
        frase = 'Você precisa ficar atento aos seus hábitos! A vida pode se tornar mais difícil se os fatores de risco não forem controlados. Infelizmente, suas respostas indicam um risco elevado de complicações de saúde, como um AVC. Tome medidas agora para mudar esse cenário. Evite chegar a uma situação em que a vida dependa de cuidados intensivos. Ainda há tempo para mudar!'

    else:
        imagem = 'fatores-risco-resultado-bom.webp'
        frase = 'Parabéns! Suas respostas mostram que você está no caminho certo para uma vida saudável e longe dos riscos de um AVC. Continue cuidando de sua saúde com bons hábitos, alimentação balanceada e atividades físicas regulares. O esforço vale a pena! Aproveite a vida ao máximo em um ambiente cheio de saúde e energia positiva.'

    return render_template('quiz-fatores-risco-resultado.html', imagem=imagem, frase=frase)

@app.route('/resultado-identificacao-avc')
def resultado_identificacao_avc():
    if session['resultado-identificacao-avc'] == 'aprovado':
        imagem = 'identificacao-avc-aprovado.webp'
        frase = 'Parabéns! Você demonstrou conhecimento e atenção ao identificar corretamente os sinais de um AVC. Sua conscientização pode salvar vidas. Continue assim!' 
        id_botao = 'exit-btn'
        text_butao = 'Sair do quiz'

    else:
        imagem = 'identificacao-avc-reprovado.webp'
        frase = 'Infelizmente, você não conseguiu identificar todos os sinais de um AVC. Mas não desanime! Refaça o quiz e aprimore seus conhecimentos para estar preparado a ajudar quando necessário.'
        id_botao = 'redo-btn'
        text_butao = 'Refazer Quiz'
    
    return render_template('quiz-identificacao-avc-resultado.html', imagem=imagem , frase=frase, id_botao=id_botao, text_butao=text_butao)

# Resultado parcial do tratamento
@app.route('/resultado-tratamento-avc')
def resultado_tratamento_avc():
    if session['resultado-tratamento-avc'] == 'aprovado':
        imagem = 'tratamento-avc-aprovado.webp'
        frase = 'Parabéns! Você demonstrou conhecimento e atenção a como tratar corretamente uma suspeita de AVC. Sua conscientização pode salvar vidas. Continue assim!' 
        id_botao = 'exit-btn'
        text_butao = 'Sair do quiz'

    else:
        imagem = 'tratamento-avc-reprovado.jpeg'
        frase = 'Infelizmente, você não conseguiu identificar todos os tratamentos adequados para uma suspeita de AVC. Mas não desanime! Refaça o quiz e aprimore seus conhecimentos para estar preparado a ajudar quando necessário.'
        id_botao = 'redo-btn'
        text_butao = 'Refazer Quiz'
    
    return render_template('quiz-tratamento-avc-resultado.html', imagem=imagem , frase=frase, id_botao=id_botao, text_butao=text_butao)

@app.route('/resultado-final')
def resultado_final():
    e = salvar_dados_excel()

    if e:
        return f"Ocorreu um erro: {e}"
    
    if session.get('resultado-fatores-risco') == 'ruim':
        frase_fatores_risco = 'Você precisa ficar atento aos seus hábitos! A vida pode se tornar mais difícil se os fatores de risco não forem controlados. Infelizmente, suas respostas indicam um risco elevado de complicações de saúde, como um AVC. Tome medidas agora para mudar esse cenário. Evite chegar a uma situação em que a vida dependa de cuidados intensivos. Ainda há tempo para mudar!'
        imagem_fatores_risco = 'fatores-risco-resultado-ruim.JPG'
    else:
        frase_fatores_risco = 'Parabéns! Suas respostas mostram que você está no caminho certo para uma vida saudável e longe dos riscos de um AVC. Continue cuidando de sua saúde com bons hábitos, alimentação balanceada e atividades físicas regulares. O esforço vale a pena! Aproveite a vida ao máximo em um ambiente cheio de saúde e energia positiva.'
        imagem_fatores_risco = 'fatores-risco-resultado-bom.webp'

    if session.get('resultado-identificacao-avc') == 'aprovado':
        frase_identificacao_avc = 'Parabéns! Você demonstrou conhecimento e atenção ao identificar corretamente os sinais de um AVC. Sua conscientização pode salvar vidas. Continue assim!'
        imagem_identificacao_avc = 'identificacao-avc-aprovado.webp'
    else:
        frase_identificacao_avc = 'Infelizmente, você não conseguiu identificar todos os sinais de um AVC. Mas não desanime! Refaça o quiz e aprimore seus conhecimentos para estar preparado a ajudar quando necessário.'
        imagem_identificacao_avc = 'identificacao-avc-reprovado.webp'

    if session.get('resultado-tratamento-avc') == 'aprovado':
        frase_tratamento_avc = 'Parabéns! Você demonstrou conhecimento e atenção a como tratar corretamente uma suspeita de AVC. Sua conscientização pode salvar vidas. Continue assim!'
        imagem_tratamento_avc = 'tratamento-avc-aprovado.webp'
    else:
        frase_tratamento_avc = 'Infelizmente, você não conseguiu identificar todos os tratamentos adequados para uma suspeita de AVC. Mas não desanime! Refaça o quiz e aprimore seus conhecimentos para estar preparado a ajudar quando necessário.'
        imagem_tratamento_avc = 'tratamento-avc-reprovado.jpeg'
    
    return render_template('resultado-final.html',frase_fatores_risco=frase_fatores_risco,imagem_fatores_risco=imagem_fatores_risco,frase_identificacao_avc=frase_identificacao_avc,imagem_identificacao_avc=imagem_identificacao_avc,frase_tratamento_avc = frase_tratamento_avc, imagem_tratamento_avc=imagem_tratamento_avc)

# Rotas de ações -----------------------------------------------------------
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
        session['email'] = request.form['email']
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

        respostas_ruins = 0
        if session.get('fator-risco-1') == 'nao':
            respostas_ruins += 1
        if session.get('fator-risco-2') == 'nao':
            respostas_ruins += 1
        if session.get('fator-risco-3') == 'sim':
            respostas_ruins += 1
        if session.get('fator-risco-4') == 'nao':
            respostas_ruins += 1
        if session.get('fator-risco-5') == 'sim':
            respostas_ruins += 1
        if session.get('fator-risco-6') == 'nao':
            respostas_ruins += 1
        if session.get('fator-risco-7') == 'sim':
            respostas_ruins += 1
        if session.get('fator-risco-8') == 'sim':
            respostas_ruins += 1
        if session.get('fator-risco-9') == 'sim':
            respostas_ruins += 1

        if respostas_ruins >= 5:
            session['resultado-fatores-risco'] = 'ruim'
        else:
            session['resultado-fatores-risco'] = 'bom'

        return redirect(url_for('resultado_fatores_risco'))
    
    return render_template('quiz-fatores-risco.html')

@app.route('/identificacao-avc', methods=['GET','POST']) 
def identificacao_avc():
    if request.method == 'POST':
        session['fator-identificacao-avc-1'] = request.form['fator-1']
        session['fator-identificacao-avc-2'] = request.form['fator-2']
        session['fator-identificacao-avc-3'] = request.form['fator-3']

        respostas_corretas = 0

        if session.get('fator-identificacao-avc-1') == 'sim':
            respostas_corretas += 1
        if session.get('fator-identificacao-avc-2') == 'nao':
            respostas_corretas += 1
        if session.get('fator-identificacao-avc-3') == 'sim':
            respostas_corretas += 1
        
        if respostas_corretas >= 2:
            session['resultado-identificacao-avc'] = 'aprovado'
        else:
            session['resultado-identificacao-avc'] = 'reprovado'
        
        if 'tentativas-identificacao-avc' not in session:
            session['tentativas-identificacao-avc'] = 1
        else:
            session['tentativas-identificacao-avc'] += 1

        return redirect(url_for('resultado_identificacao_avc'))
    
    return render_template('quiz-identificacao-avc.html')

@app.route('/tratamento-avc', methods=['GET','POST']) 
def tratamento_avc():
    if request.method == 'POST':
        
        session['fator-tratamento-avc-1'] = request.form['fator-1']
        session['fator-tratamento-avc-2'] = request.form['fator-2']
        session['fator-tratamento-avc-3'] = request.form['fator-3']
        session['fator-tratamento-avc-4'] = request.form['fator-4']
        session['fator-tratamento-avc-5'] = request.form['fator-5']

        respostas_corretas = 0

        if session.get('fator-tratamento-avc-1') == '2':
            respostas_corretas += 1
        if session.get('fator-tratamento-avc-2') == '3':
            respostas_corretas += 1
        if session.get('fator-tratamento-avc-3') == '1':
            respostas_corretas += 1
        if session.get('fator-tratamento-avc-4') == '3':
            respostas_corretas += 1
        if session.get('fator-tratamento-avc-5') == '1':
            respostas_corretas += 1

        if respostas_corretas >= 3:
            session['resultado-tratamento-avc'] = 'aprovado'
        else:
            session['resultado-tratamento-avc'] = 'reprovado'

        if 'tentativas-tratamento-avc' not in session:
            session['tentativas-tratamento-avc'] = 1
        else:
            session['tentativas-tratamento-avc'] += 1

        return redirect(url_for('resultado_tratamento_avc'))
    
    return render_template('quiz-tratamento-avc.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)