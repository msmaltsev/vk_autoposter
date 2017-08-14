# !usr/env/bin python3
# -*- coding: utf8 -*-

import os, shutil

class Dispatch:
    def availableId(self):
        dispatches_list = os.listdir('dispatches')
        try:
            dispatches_list = [int(i) for i in dispatches_list]
            available_id = max(dispatches_list) + 1
        except:
            available_id = 0
        # print(available_id)
        return available_id


    def validateDispatch(self, id_):
        # print('dispatch %s'%id_)
        wdir_name = os.getcwd() + '/dispatches'
        if str(id_) in os.listdir(wdir_name):
            if 'posts' in os.listdir('%s/%s'%(wdir_name, id_)):
                # print('posts folder ok')
                pass
            else:
                # print('creating posts folder')
                os.mkdir('%s/%s/posts'%(wdir_name, id_))
            if 'group_id_lists' in os.listdir('%s/%s'%(wdir_name, id_)):
                # print('group_id_list folder ok')
                pass
            else:
                # print('creating group_id_lists folder')
                os.mkdir('%s/%s/group_id_lists'%(wdir_name, id_))
            if 'delay.txt' in os.listdir('%s/%s'%(wdir_name, id_)):
                # print('delay.txt ok')
                pass
            else:
                # print('creating delay.txt')
                df = open('%s/%s/delay.txt'%(wdir_name, id_))
                df.write('10.0')
                df.close()
        else:
            # print('creatig dispatch with id %s'%(id_))
            os.mkdir('%s/%s'%(wdir_name, id_))
            # print('creating posts folder in dispatch %s'%id_)
            os.mkdir('%s/%s/posts'%(wdir_name, id_))
            # print('creating group_id_lists folder in dispatch %s'%id_)
            # os.mkdir('%s/%s/group_id_lists'%(wdir_name, id_))
            
        return '%s/%s'%(wdir_name, id_)


    def __init__(self, id_):
        if id_ == 0:
            self.id_ = self.availableId()
        else:
            self.id_ = id_
        self.folder = self.validateDispatch(self.id_)
        self.posts = os.listdir(self.folder + '/posts')
        self.acc_file = '%s/dispatches/%s/group_ids.txt'%(os.getcwd(), self.id_)
        self.delay_file = '%s/dispatches/%s/delay.txt'%(os.getcwd(), self.id_)
        try:
            self.interval = open(self.delay_file,  'r', encoding='utf8').read().split('\n')[0]
            self.interval = float(self.interval)
        except Exception as e:
            f = open(self.delay_file, 'w', encoding='utf8')
            f.write('10')
            f.close()
            self.interval = open(self.delay_file,  'r', encoding='utf8').read().split('\n')[0]
            self.interval = float(self.interval)


    def removeDispatch(self):
        shutil.rmtree(self.folder)
        print('dispatch %s successfully removed'%self.id_)
