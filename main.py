# -*- coding: utf-8 -*-
try:
    from os import getuid
except ImportError:
    def getuid():
        return 4000

from dispatch import Dispatch
from post import Post
from sendDispatch import *

from flask import Flask, render_template, request, redirect
import json, datetime, time, random, os
from werkzeug import secure_filename

app = Flask(__name__, template_folder='templates')

def renderDispatches():
    disp_dict = {}
    disp_list = os.listdir('dispatches')
    disp_list = [i for i in disp_list if i not in  ['0', 0]]
    for i in disp_list:
        disp_dict[i] = []
        d = Dispatch(i)
        d_id = d.id_
        post_list = os.listdir('dispatches/%s/posts'%d_id)
        post_list = [i for i in post_list if i not in  ['0', 0]]
        for p in post_list:
            p = Post(p, d_id)
            p = p.post_data
            disp_dict[i].append(p)
    return disp_dict


@app.route("/", methods=['GET', 'POST'])
def index():
    d = renderDispatches()
    return render_template('index.html', dispatches = d)


@app.route("/remove_dispatch", methods=['GET', 'POST'])
def removeDispatch():
    if request.method == "POST":
        dispatch_id = request.form['remove_dispatch']
        d = Dispatch(dispatch_id)
        d.removeDispatch()
    return redirect('/')


@app.route("/add_dispatch", methods=['GET', 'POST'])
def addDispatch():
    if request.method == "POST":
        d = Dispatch(0)
        i = d.id_
        p = Post(0, i)
    return redirect('/')


@app.route("/dispatch/<dispatch_id>", methods=['GET', 'POST'])
def displayDispatch(dispatch_id):
    group_ids_lists = os.listdir('group_ids_lists')
    d = renderDispatches()
    d = d[dispatch_id]
    return render_template('dispatch.html', dispatch_id = dispatch_id, d = d, group_ids_lists = group_ids_lists)


@app.route("/save_post/<dispatch_id>/<post_id>", methods=['GET', 'POST'])
def savePost(dispatch_id, post_id):
    if request.method == "POST":
        p = Post(post_id, dispatch_id)
        tx = request.form['text']
        if tx != '':
            p.addText(tx)
    return redirect('/dispatch/%s'%dispatch_id)


@app.route("/add_post/<dispatch_id>", methods=['GET', 'POST'])
def addPost(dispatch_id):
    if request.method == "POST":
        p = Post(0, dispatch_id)
    return redirect('/dispatch/%s'%dispatch_id)


@app.route("/remove_post/<dispatch_id>/<post_id>", methods=['GET', 'POST'])
def removePost(dispatch_id, post_id):
    if request.method == "POST":
        p = Post(post_id, dispatch_id)
        p.removePost()
    return redirect('/dispatch/%s'%dispatch_id)


@app.route("/send_test_post/<dispatch_id>/<post_id>", methods=['GET', 'POST'])
def sendTestPost(dispatch_id, post_id):
    if request.method == "POST":
        p = Post(post_id, dispatch_id)
        p = p.post_data
        print(p)
        access_tokens = loadListFromFile('access_tokens.txt')
        group_ids_list = ['-150121997']
        sendPost(random.choice(access_tokens), p, group_ids_list)

    return redirect('/dispatch/%s'%dispatch_id)


@app.route("/send_dispatch/<dispatch_id>", methods=['GET', 'POST'])
def sendDispatch(dispatch_id):

    if request.method == "POST":
        available_posts = []
        for i in os.listdir('dispatches/%s/posts'%dispatch_id):
            p = Post(i, dispatch_id)
            p = p.post_data
            available_posts.append(p)
        

        # group_ids_list = request.form['group_ids_list']
        group_ids_list = 'group_ids_lists/group_ids_list.txt'
        group_ids_list = loadListFromFile(group_ids_list)
        access_tokens = loadListFromFile('access_tokens.txt')

        for a in range(len(access_tokens)):
            access_token = access_tokens[a]
            print('access_token: %s'%access_token)
            try:
                sendPost(access_token, random.choice(available_posts), group_ids_list)
            except Exception as e:
                print(e)
                if a == len(access_tokens):
                    print('no more access_tokens')
                    break
                else:
                    continue

    return redirect('/dispatch/%s'%dispatch_id)



if __name__ == "__main__":
    app.run(port=getuid() + 1000)