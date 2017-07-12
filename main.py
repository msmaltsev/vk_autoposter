# -*- coding: utf-8 -*-
try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000

import sendPosts

from flask import Flask, render_template, request, redirect
import json, datetime, time

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/accept_data", methods = ['GET', 'POST'])
def accept_data():
    if request.method == 'POST':
        post_text = request.form['post_text']
        # access_tokens = request.form['access_tokens']
        group_ids_list = request.form['group_ids_list']

        with open('post_text.txt', 'w', encoding='utf8') as f:
            f.write(post_text)
        
        # with open('access_tokens.txt', 'w', encoding='utf8') as f:
        #     f.write(access_tokens)

        with open('group_ids_list.txt', 'w', encoding='utf8') as f:
            f.write(group_ids_list)

    sendPosts.main()
    return render_template('accept_data.html')


if __name__ == "__main__":
    app.run(port=getuid() + 1000)
    
