from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(chamados)

def conectar_bd():
    return sqlite3.connect('chamados.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar', methods=['GET', 'POST'])
def criar_chamado():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status = 'Aberto'
        
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chamados (titulo, descricao, status) VALUES (?, ?, ?)",
                       (titulo, descricao, status))
        conn.commit()
        conn.close()

        return redirect(url_for('listar_chamados'))
    
    return render_template('criar_chamado.html')

@app.route('/chamados')
def listar_chamados():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chamados")
    chamados = cursor.fetchall()
    conn.close()

    return render_template('listar_chamados.html', chamados=chamados)

@app.route('/chamado/<int:id>')
def ver_chamado(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chamados WHERE id = ?", (id,))
    chamado = cursor.fetchone()
    conn.close()

    return render_template('ver_chamado.html', chamado=chamado)

if __name__ == '__main__':
    app.run(debug=True)

