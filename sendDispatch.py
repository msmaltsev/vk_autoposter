# !usr/env/bin python3
# -*- coding: utf8 -*-

import requests as req
import json, os, time
from vkApiAccess import *



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


def sendPost(access_token, post_dict, group, interval = 0.33333333):
    # print('sendPost function working now')
    photos_list = post_dict['photos']
    # print(photos_list)
    if len(photos_list) > 10:
        photos_list = photos_list[:10]
        # print('too much photos; only first 10 will be uploaded!')
    print('photos to upload: %s'%len(photos_list))
    print('posting to group %s'%group)
    message = post_dict['text']
    photos = uploadPhotos(photos_list, group * -1, access_token)
    link = [post_dict['link']]
    attachments = ','.join(photos + link)
    # print(attachments)
    a = postOnWall(group, access_token, message = message, attachments = attachments, signed = 0)
    print('sleeping %s seconds...'%interval)
    time.sleep(interval)
    # print(a)
    
    
if __name__ == '__main__':
    pass
    

