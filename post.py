# !usr/env/bin python3
# -*- coding: utf8 -*-

import os, shutil
import requests as req

class Post:
    def availableId(self, dispatch_id):
        posts_list = os.listdir('dispatches/%s/posts'%dispatch_id)
        try:
            posts_list = [int(i) for i in posts_list]
            available_id = max(posts_list) + 1
        except:
            available_id = 0
        print(available_id)
        return available_id


    def readText(self, f):
        f = open(f, 'r', encoding='utf8').read()
        return f


    def validatePost(self, id_, dispatch_id):
        # print('post %s from dispatch %s'%(id_, dispatch_id))
        wdir_name = os.getcwd() + '/dispatches/%s/posts/%s'%(dispatch_id, id_)
        if str(id_) in os.listdir(os.getcwd() + '/dispatches/%s/posts'%dispatch_id):
            if 'photos' in os.listdir(wdir_name):
                # print('photos folder ok')
                pass
            else:
                # print('photos not found in %s'%wdir_name)
                os.mkdir(wdir_name + '/photos')
        else:
            os.mkdir(os.getcwd() + '/dispatches/%s/posts/%s'%(dispatch_id, id_))
            os.mkdir(os.getcwd() + '/dispatches/%s/posts/%s/photos'%(dispatch_id, id_))
            open(os.getcwd() + '/dispatches/%s/posts/%s/text.txt'%(dispatch_id, id_), 'w', encoding='utf8').close()
            open(os.getcwd() + '/dispatches/%s/posts/%s/link.txt'%(dispatch_id, id_), 'w', encoding='utf8').close()
        return wdir_name


    def __init__(self, id_, dispatch_id):
        self.dispatch_id = dispatch_id
        if id_ == 0:
            self.id_ = self.availableId(self.dispatch_id)
        else:
            self.id_ = id_
        self.folder = self.validatePost(self.id_, self.dispatch_id)
        self.post_data = {'id':self.id_, 'dispatch_id':self.dispatch_id, 'photos':[self.folder + '/photos/' + i for i in os.listdir(self.folder + '/photos')][:10], 'photos_amount':len([i for i in os.listdir(self.folder + '/photos')]), 'text':self.readText(self.folder + '/text.txt'), 'link':self.readText(self.folder + '/link.txt')}


    def removePost(self):
        shutil.rmtree(self.folder)
        print('post %s successfully removed'%self.id_)


    def addText(self, text):
        f = open(os.getcwd() + '/dispatches/%s/posts/%s/text.txt'%(self.dispatch_id, self.id_), 'w', encoding='utf8')
        f.write(text)
        f.close()
        print('text %s added to post %s from dispatch %s'%(text, self.id_, self.dispatch_id))


    def validateLink(self, link):
        try:
            r = req.get(link)
            return link
        except:
            return 'http://' + link


    def addLink(self, link):
        link = self.validateLink(link)
        f = open(os.getcwd() + '/dispatches/%s/posts/%s/link.txt'%(self.dispatch_id, self.id_), 'w', encoding='utf8')
        f.write(link)
        f.close()
        print('link %s added to post %s from dispatch %s'%(link, self.id_, self.dispatch_id))
