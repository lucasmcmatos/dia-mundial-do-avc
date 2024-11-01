from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import datetime

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
        caminho_arquivo = os.path.join(os.getcwd(), 'dynamic', 'dados_quiz.xlsx')
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
        'Data / Hora': [session.get('date_time')],
        'Email': [session.get('email')],
        'Idade': [session.get('age')],
        'Sexo': [session.get('sex')],
        '1° Fator de Risco': [session.get('fator-risco-1')],
        '2° Fator de Risco': [session.get('fator-risco-2')],
        '3° Fator de Risco': [session.get('fator-risco-3')],
        '4° Fator de Risco': [session.get('fator-risco-4')],
        '5° Fator de Risco': [session.get('fator-risco-5')],
        '6° Fator de Risco': [session.get('fator-risco-6')],
        '7° Fator de Risco': [session.get('fator-risco-7')],
        '8° Fator de Risco': [session.get('fator-risco-8')],
        '9° Fator de Risco': [session.get('fator-risco-9')],
        '1° Fator Identificacao': [session.get('fator-identificacao-avc-1')],
        '2° Fator Identificacao': [session.get('fator-identificacao-avc-2')],
        '3° Fator Identificacao': [session.get('fator-identificacao-avc-3')],
        'Tentativas Realizadas Identificacao AVC': [session.get('tentativas-identificacao-avc')],
        '1° Fator Tratamento': [session.get('fator-tratamento-avc-1')],
        '2° Fator Tratamento': [session.get('fator-tratamento-avc-2')],
        '3° Fator Tratamento': [session.get('fator-tratamento-avc-3')],
        '4° Fator Tratamento': [session.get('fator-tratamento-avc-4')],
        '5° Fator Tratamento': [session.get('fator-tratamento-avc-5')],
        'Tentativas Realizadas Tratamento AVC': [session.get('tentativas-tratamento-avc')],
        'Resultados Fatores de Risco':[session.get('resultado-fatores-risco')],
        'Resultados Identificacao AVC':[session.get('resultado-identificacao-avc')],
        'Resultados Tratamento AVC':[session.get('resultado-tratamento-avc')]
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

@app.route('/dynamic/graphs/<path:filename>')
def dynamic_graphs(filename):
    return send_from_directory('dynamic/graphs', filename)

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        file_path = 'dynamic/dados_quiz.xlsx'
        data = pd.read_excel(file_path) # Ajustar aqui para onde o arquivo excel estiver
        graph_dir = 'dynamic/graphs'
        os.makedirs(graph_dir, exist_ok=True) # Ajustar aqui para onde o arquivos dinamicos forem ajustados

        # Gráfico 1: Distribuição de Idades (conta de indivíduos por idade)
        idade_graph_path = os.path.join(graph_dir, 'grafico_idade.png')
        plt.figure(figsize=(8, 4))
        data['Idade'].value_counts().sort_index().plot(kind='bar', color='skyblue')
        plt.title('Distribuição de Idades')
        plt.xlabel('Idade')
        plt.ylabel('Número de Indivíduos')
        plt.tight_layout()
        plt.savefig(idade_graph_path)
        plt.close()

        # Gráfico 2: Quantidade de Pessoas que Realizaram o Quiz
        # Assumimos que cada e-mail representa uma pessoa única.
        total_individuos = data['Email'].nunique()  # Contagem de e-mails únicos

        # Gráfico 3: Gráficos de Pizza para Respostas das Perguntas
        resposta_graphs = []
        for coluna in data.columns[2:]:  # Assumindo que as respostas começam na terceira coluna
            resposta_graph_path = os.path.join(graph_dir, f'grafico_{coluna}.png')
            plt.figure(figsize=(6, 6))
            data[coluna].value_counts().plot.pie(autopct='%1.1f%%', colors=['#ff9999','#66b3ff', '#99ff99'])
            plt.title(f'Respostas para {coluna}')
            plt.ylabel('')  # Remove o rótulo do eixo y para clareza
            plt.tight_layout()
            plt.savefig(resposta_graph_path)
            resposta_graphs.append(f'dynamic/graphs/grafico_{coluna}.png')
            plt.close()

        # Passar caminhos dos gráficos para o template
        return render_template('dados-plataforma.html', 
                            idade_graph_path=idade_graph_path, 
                            total_individuos=total_individuos,
                            resposta_graphs=resposta_graphs)

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

    data_hora_chamada = datetime.now()
    session['date_time'] = data_hora_chamada.strftime('%Y-%m-%d %H:%M:%S')

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