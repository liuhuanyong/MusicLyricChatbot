#!/usr/bin/env python3
# coding: utf-8
# File: search_es.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-10

from elasticsearch import Elasticsearch
import re

class SearchEs:
    def __init__(self):
        self._index = "music_data"
        self.es = Elasticsearch([{"host": "127.0.0.1", "port": 9200}])
        self.doc_type = "music"

    '''查询歌手，singer'''
    def search_singer(self, singer):
        query_body = {
            "query": {
                "match": {
                    "singer": singer,
                }
            }
        }
        searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]

    '''查询歌词，geci'''
    def search_geci(self, geci):
        query_body = {
            "query": {
                "match": {
                    "geci": geci,
                }
            }
        }
        searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]

    '''查询作曲者'''
    def search_composer(self, composer):
        query_body = {
            "query": {
                "match": {
                    "compser": composer,
                }
            }
        }
        searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]


    '''查询作词者'''
    def search_author(self, author):
        query_body = {
            "query": {
                "match": {
                    "composer": author,
                }
            }
        }
        searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=20)
        # 输出查询到的结果
        return searched["hits"]["hits"]

    '''判断一个字符串是否包含英文'''
    def has_english(self, str):
        for ch in str:
            if ch.lower() in ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
                return True


    '''根据当前歌词，获取下一句歌词'''
    def next_geci(self, geci):
        res_gecis = self.search_geci(geci)
        context = []
        for res in res_gecis:
            geci_list = []
            _gecis = res['_source']['geci'].split('\n')
            for _tmp in _gecis:
                if not self.has_english(_tmp):
                    _tmps = [i for i in re.split(r'[ \t\r\n]',_tmp) if i]
                else:
                    _tmps = [_tmp]
                geci_list += _tmps
            song = res['_source']['song']
            singer = res['_source']['singer']
            album = res['_source']['album']
            if geci in geci_list:
                last = 'start'
                next = 'end'
                data = {}
                data['song'] = song
                data['singer'] = singer
                data['album'] = album
                cur_index = geci_list.index(geci)
                if cur_index == 0:
                    last = 'start'
                    next = geci_list[cur_index - 1]
                elif cur_index == len(geci_list)-1:
                    last = geci_list[cur_index - 1]
                    next = 'end'
                else:
                    last = geci_list[cur_index-1]
                    next = geci_list[cur_index+1]

                if last != 'start' or next != 'end':
                    data['cur'] = geci
                    data['last'] = last
                    data['next'] = next
                    context.append(data)
        return context

    '''查询歌曲，song'''
    def search_song(self, song):
        query_body = {
            "query": {
                "match_phrase": {
                    "song": song,
                }
            }
        }
        searched = self.es.search(index=self._index, doc_type=self.doc_type, body=query_body, size=1)
        # 输出查询到的结果
        return searched["hits"]["hits"]


if  __name__ == '__main__':
    handler = SearchEs()
    song = '能不能给我一首歌的时间'
    singer = '许嵩'
    geci = '我要一步一步往上爬'
    res_singer = handler.search_singer(singer)
    res_context = handler.next_geci(geci)
    print(res_context)