#!/usr/bin/env python3
# coding: utf-8
# File: modify_data.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-10

import pymongo
from collections import Counter
from langconv import *
import re

def Traditional2Simplified(sentence):
    if not sentence:
        return ''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


class BuildData:
    def __init__(self):
        mongo = pymongo.MongoClient()
        db_name = 'mus'
        self.db = mongo[db_name]
        self.stopwords = ['www.5nd.com', '歌词', '下载', 'http://www.5nd.com', '.com', 'www', '制作', 'qq', 'QQ']
        self.attr_dict = {i.strip().split('\t')[0]:i.strip().split('\t')[1] for i in open('attr_map.txt') if len(i.strip().split('\t')) == 2}

    '''构建基本数据集'''
    def build_data(self):
        singers = set()
        songs = set()
        albums = set()
        singer_songs = set()
        f_singer = open('singer.txt', 'w+')
        f_song = open('song.txt', 'w+')
        f_album = open('album.txt', 'w+')
        f_singer_song = open('singer_song.txt', 'w+')
        count = 0
        for item in self.db['clean'].find():
            # url = item['url']
            singer = item['singer']
            song = item['song']
            album = item['album']
            geci = item['geci']
            singers.add(singer)
            songs.add(song)
            albums.add(album)
            singer_songs.add('#'.join([singer, song]))
            count += 1
            print(count)

        f_singer.write('\n'.join(list(singers)))
        f_song.write('\n'.join(list(songs)))
        f_album.write('\n'.join(list(singers)))
        f_singer_song.write('\n'.join(list(singer_songs)))
        f_singer.close()
        f_song.close()
        f_album.close()
        f_singer_song.close()
        return

    '''根据分割符对字符串进行分割，对字符串进行分割'''
    def pretty_song(self, song, singer):
        tags = ['（', '（', '-', '-', '《','<','.','DJ']
        en_status = self.has_english(song)
        song_name = [i for i in re.split(r'[(（《<./\\_\-【\[]', song) if i]
        if not en_status:
            song_name = [i.replace(' ', '') for i in song_name if i.replace(' ','')]
        if not song_name:
            return
        if singer in song_name and len(song_name) > 1:
            return song_name[1]
        else:
            return song_name[0]

    '''判断一个字符串是否包含中文'''
    def has_chinese(self, str):
        for ch in str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True

    '''判断一个字符串是否包含英文'''
    def has_english(self, str):
        for ch in str:
            if ch.lower() in ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
                return True

    '''对字符串进行移除噪声处理'''
    def remove_noisy(self, str):
        str = str.replace(',', '&').replace('＆','&').replace('\\', '&').replace('：',':')
        str = str.replace(' & ', '&').replace('\u3000', ' ').replace('\xa0',' ')
        return str


    '''标准化中文人名'''
    def pretty_singer(self, singer):
        singer = self.remove_noisy(singer)
        singer = singer.replace('（','(').replace('、','&').replace('\\','&').split('(')[0]
        return singer

    '''标准化歌词'''
    def pretty_geci(self):
        count = 0
        for item in self.db['data'].find():
            singer = self.remove_noisy(item['singer'])
            singer = self.pretty_singer(singer)
            song_ = self.remove_noisy(item['song'])
            song = self.pretty_song(song_, singer)
            album = self.remove_noisy(item['album'])
            geci = self.remove_noisy(item['geci'])
            geci_list = [i for i in geci.split('\n') if i not in ['\r', '']]
            attr_region = geci_list[:20]
            attr_tuples = self.attribute_extract(attr_region)
            body = self.extract_geci(geci_list)
            if body:
                try:
                    data = {}
                    data['singer'] = Traditional2Simplified(singer)
                    data['song'] = Traditional2Simplified(song)
                    data['album'] = Traditional2Simplified(album)
                    data['geci'] = [Traditional2Simplified(' '.join([j for j in i.replace('&','').replace('.','').split(' ') if j])) for i in body if i not in attr_tuples and self.check_stop(i) and singer not in i and song not in i and album not in i]
                    data['attrs'] = self.pretty_attrs(attr_tuples)
                    try:
                        self.db['clean2'].insert(data)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
            count += 1
            print(count)

    '''歌词截取'''
    def extract_geci(self, geci_list):
        start_index = 0
        if '暂无歌词' in geci_list:
            return []
        for index, geci in enumerate(geci_list):
            if '歌词出处' in geci:
                start_index = index
                break
        body = [i.replace('http://www.5nd.com', '') for i in geci_list[start_index+1:] if self.check_stop(i)]
        if len(body) < 5:
            return []
        return body


    '''判断停用词'''
    def check_stop(self, str):
        for s in self.stopwords:
            if s in str:
                return False
        return True

    '''歌词属性信息提取'''
    def attribute_extract(self, attrs):
        print('***********')
        attr_infos = []
        for attr in attrs:
            if len(attr.split(':')) > 1:
                attr_infos.append(attr)
        return attr_infos

    '''整理attrs'''
    def process_attrs(self):
        f = open('attrs.txt', 'w+')
        keys = []
        for item in self.db['clean2'].find():
            attrs = item['attrs']
            for attr in attrs:
                key = attr[0]
                value = attr[1]
                keys.append(key)

        keys_dict = Counter(keys).most_common()
        filter_words = ['词', '曲']
        for item in keys_dict:
            for wd in filter_words:
                if wd in item[0] and item[1] > 9:
                    f.write(item[0] + '@' + str(item[1]) + '\n')
        f.close()

    '''规范化infobox'''
    def pretty_attrs(self, attrs):
        '''整理attrs'''
        _attrs = []
        for attr in attrs:
            _attr = attr.split('  ')
            for _tmp in _attr:
                tmp = _tmp.split(':')
                if len(tmp) == 2:
                    key = tmp[0].replace(' ', '').replace('\t', '')
                    key = Traditional2Simplified(key)
                    value = Traditional2Simplified(tmp[1])
                    _attrs.append([key, value])
        return _attrs


    '''计算歌词总行数'''
    def count_geci_num(self):
        count = 0
        f = open('geci.txt', 'w+')
        count = 0
        gecis = []
        for item in self.db['clean'].find():
            geci = item['geci']
            gecis += geci
            count += 1
            print(count)

        set_geci = set(gecis)
        f.write('\n'.join(list(set_geci)))
        f.close()
        print(len(gecis), len(set_geci))

    '''更新作词，作曲信息'''
    def update_detail(self):
        count = 0
        for item in self.db['clean2'].find():
            singer = item['singer']
            song = item['song']
            geci = item['geci']
            attrs = item['attrs']
            album = item['album']
            composer = ''
            author = ''
            for attr in attrs:
                key = attr[0]
                value = attr[1]
                value = value.replace('/', '&').replace('／','&').replace(',','&').replace('，','&')
                value = value.replace('?br>', '').replace('（','(').replace('@', '&').replace('、','&').replace('__','').split('(')[0]
                en_status = self.has_english(value)
                if not en_status:
                    value = value.replace(' ','')
                else:
                    value = value.lstrip()
                if not value:
                    continue
                if key in self.attr_dict:
                    types = self.attr_dict[key]
                    if types == 'q':
                        composer = value
                    elif types == 'c':
                        author = value
                    elif types == 'qc':
                        composer = value
                        author = value
            data = {}
            data['singer'] = singer
            data['song'] = song
            data['geci'] = geci
            data['composer'] = composer
            data['author'] = author
            data['album'] = album
            self.db['final'].insert(data)
            count += 1
            print(count)

handler = BuildData()
handler.update_detail()
