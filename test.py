# !usr/env/bin python3
# -*- coding: utf8 -*-

from dispatch import Dispatch
from post import Post
from sendDispatch import *

import random

if __name__ == '__main__':
    for k in range(0,10):
        d = Dispatch(0)
        p = Post(0, d.id_)
        p.addText('текст поста %s в рассылке %s'%(p.id_, d.id_))
        p.addLink(random.choice(['http://lenta.ru/', 'http://vk.com', 'http://python.org']))
        p = Post(0, d.id_)
        p.addText('текст поста %s в рассылке %s'%(p.id_, d.id_))
        p.addLink(random.choice(['http://lenta.ru/', 'http://vk.com', 'http://python.org']))
        p = Post(0, d.id_)
        p.addText('текст поста %s в рассылке %s'%(p.id_, d.id_))
        p.addLink(random.choice(['http://lenta.ru/', 'http://vk.com', 'http://python.org']))
        