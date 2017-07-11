# !usr/env/bin python3
# -*- coding: utf8 -*-

import requests as req
import json, os, time

def vk_makeRequest(method, access_token, **kwargs):
    request = 'https://api.vk.com/method/%s'%method
    if kwargs:
        request += '?'
        for kwarg in kwargs:
            request += '%s=%s&'%(kwarg, kwargs[kwarg])
    request += 'access_token=%s'%access_token
    return request


def vk_callRequest(request, req_method):
    # print('vk_callRequest req_method %s'%req_method)
    r = eval('req.%s(request)'%req_method)
    t = r.text
    j = json.loads(t)
    return j


def callVkApi(method, access_token, req_method = 'get', **kwargs):
    request = vk_makeRequest(method, access_token, **kwargs)
    # print(req_method.upper(), request)
    response = vk_callRequest(request, req_method)
    try:
        response = response['response']
    except:
        pass
    # print('')
    return response


def uploadPhotos(photos_list, group_id, access_token):
    uploaded_photos = []
    for f in photos_list:
        addr = callVkApi('photos.getWallUploadServer', access_token, group_id = group_id)
        upload_url = addr['upload_url']
        pfile = ('f.jpg', open(f, 'rb'))
        data = {'photo':pfile}
        a = req.post(upload_url, files = data)
        a = json.loads(a.text)
        # print(a)
        s = callVkApi('photos.saveWallPhoto', access_token, req_method = 'post', group_id = group_id, photo = a['photo'], server = a['server'], hash = a['hash'])
        print(s)
        for i in s:
            uploaded_photos.append(i['id'])
        time.sleep(0.3333333)
    # print(uploaded_photos)
    return uploaded_photos


def postOnWall(wall_id, access_token, **kwargs):
    r = callVkApi('wall.post', access_token, owner_id = wall_id, **kwargs)
    return r
    

def loadListFromFile(f = 'group_ids_list.txt'):
    a = open(f, encoding='utf8').read().split('\n')
    a = [i for i in a if i != '']
    return a


def makePost(access_token):
    photos_list = ['%s\photos\%s'%(os.getcwd(), i) for i in os.listdir(os.getcwd() + '\photos')] # not longer than 6!
    print(photos_list)
    if len(photos_list) > 6:
        photos_list = photos_list[:5]
        print('too much photos; only first 6 will be uploaded!')
    print('photos to upload: %s'%len(photos_list))
    groups = [int(i) for i in loadListFromFile('group_ids_list.txt')]
    for g in groups:
        print('posting to group %s'%g)
        message = open('post_text.txt', encoding='utf8').read()
        links = ['https://lenta.ru']
        audios = ['audio34241781_456239198']
        photos = uploadPhotos(photos_list, g * -1, access_token)
        attachments = ','.join(links + audios + photos)
        a = postOnWall(g, access_token, message = message, attachments = attachments, signed = 0)
        print(a)
    
    
if __name__ == '__main__':

    access_tokens = loadListFromFile('access_tokens.txt')

    for a in range(len(access_tokens)):
        access_token = access_tokens[a]
        print('access_token: %s'%access_token)
        try:
            makePost(access_token)
        except Exception as e:
            print(e)
            if a == len(access_tokens):
                print('no more access_tokens')
                break
            else:
                continue
