# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests, json

app = Flask(__name__)
app.secret_key = b'_1@#12qdasd%#$%$U%DFsd'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('token'):
        return redirect(url_for('teste'))
    if request.method == 'GET':
        return render_template('login.html')
    res = json.loads((requests.post('http://localhost:5000/api/v1/users/login', data=json.dumps({
        'email': request.form['email'],
        'password': request.form['password']
    }), headers={
        'content_type': 'application/json'
    })).content.decode('utf-8'))

    if res.get('error'):
        flash(u'Login e/ou senha incorretos', 'error')
        return redirect(url_for('login'))

    session['token'] = res['jwt_token']
    return redirect(url_for('teste'))


@app.route('/teste', methods=['GET'])
def teste():
    if not session.get('token'):
        return redirect(url_for('login'))
    return render_template('posts.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/cadastrar-post', methods=['GET', 'POST'])
def cadastrarPost():
    if not session.get('token'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('cadastrar-post.html')
    requests.post('http://localhost:5000/api/v1/blogposts/', data=json.dumps({
        'title': request.form['title'],
        'contents': request.form['contents']
    }), headers={
        'content_type': 'application/json',
        'api-token': session['token']
    })

    flash(u'Post cadastrado com sucesso', 'message')
    return redirect(url_for('cadastrarPost'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)
