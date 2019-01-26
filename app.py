# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests
import json
import datetime

app = Flask(__name__)
app.secret_key = b'_1@#12qdasd%#$%$U%DFsd'
BASE_API_URL = "http://localhost:5000/api/v1"


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


@app.route('/post/<string:post_id>', methods=['GET'])
def get_post_by_id(post_id):
    if not session.get('token'):
        return redirect(url_for('login'))
    post = json.loads(
        requests.get(BASE_API_URL + '/blogposts/' + post_id, headers={
            'api-token': session.get('token')
        }).content.decode('utf-8')
    )
    post['created_at'] = post.get('created_at').split('T')[0]

    return render_template('post.html', post=post)


@app.route('/teste', methods=['GET'])
def teste():
    if not session.get('token'):
        return redirect(url_for('login'))
    return render_template('posts.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=8000, debug=True)
