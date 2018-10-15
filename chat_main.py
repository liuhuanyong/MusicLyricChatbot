#!/usr/bin/env python3
# coding: utf-8
# File: chat_main.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-15

from search_es import *

class MusicChatbot:
    def __init__(self):
        self.es_searcher = SearchEs()
        return

    '''搜索下一歌词'''
    def search_next(self, lyric):
        res_context = self.es_searcher.next_geci(lyric)
        nexts = []
        for res in res_context:
            next = res['next']
            _from = res['singer'] + '的' + '《%s》'%res['song']
            if next != 'end':
                nexts.append([next, _from])
        if not nexts:
            return '没找着，我确实比较笨, 可能是你创作的哦'
        else:
            return "\n".join(["下一句："]+['---来自'.join(i) for i in nexts])

    '''搜索下一歌词'''
    def search_last(self, lyric):
        res_context = self.es_searcher.next_geci(lyric)
        nexts = []
        for res in res_context:
            last = res['last']
            _from = res['singer'] + '的' + '《%s》' % res['song']
            if last != 'start':
                nexts.append([last, _from])

        if not nexts:
            return '没找着，我确实比较笨, 可能是你创作的哦'
        else:
            return "\n".join(["上一句："]+['---来自'.join(i) for i in nexts])


if __name__ == '__main__':
    handler = MusicChatbot()
    lyric = '我爱你中国'
    next = handler.search_next(lyric)
    last = handler.search_last(lyric)
    print(next)
    print(last)
