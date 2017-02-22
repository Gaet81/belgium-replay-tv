#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import channel
import HTMLParser
from bs4 import BeautifulSoup

channels = {'rtltvi': 'http://www.rtl.be/tv/rtltvi',
            'clubrtl': 'http://www.rtl.be/tv/clubrtl',
            'plugrtl': 'http://www.rtl.be/tv/plugrtl'}

#id2skip = [str(x) for x in [2601,4497,3098,4452,4509,1585,1103,4388,657,767,4296,4468,701]]
#only_good_cat = {'2616': 'Le journal'}

class Channel(channel.Channel):
    def get_main_url(self):
        return 'http://www.rtl.be/tv/'

    def get_categories(self):
        channel_url = self.main_url + self.channel_id
        channel.addDir("direct", 'DefaultVideo.png', channel_id=self.channel_id, url=channel_url+'/live', action='show_videos', id='direct', direct='1')
        data_url = channel_url + '/emissions'
        print ('emissions' + data_url)
        data = channel.get_url(data_url)
        soup = BeautifulSoup(data, 'html.parser')
        main = soup.main
        section = soup.find('section', type='glossary')
        letters = section.find_all('div', {'class':'letter'})
        for letter in letters:
            name = letter.string
            channel.addDir(name, 'DefaultVideo.png', channel_id=self.channel_id, url=letter.parent.prettify().encode('UTF-8'), action='show_subcategories', id=name)

    def get_subcategories(self,datas):
        data = datas.get('url')
        print ('letter data' + data)
        letter = BeautifulSoup(data, 'html.parser')
        links = letter.find_all('a')
        for link in links:
            name = link.string
            cat_id = link['href']
            cat_url = 'http:'+cat_id
            #print ('1 emission ' + cat_url)
            dataCat = channel.get_url(cat_url) #to add only emissions with video 
            regex = r"""<section type="videos"(.)"""
            if re.search(regex,dataCat):
                regex1 = r"""<meta property="og:image" content="(.+)\""""
                img = 'http:'+re.findall(regex1,dataCat)[0]
                url = cat_url + '/videos/playlist_' + cat_url.rsplit('/', 1)[-1]
                #print ('playlist emissions '+url)
                channel.addDir(name, img, channel_id=self.channel_id, url=url, action='show_videos', id=cat_id)
##            cat_url = 'http:'+cat_id
##            #print ('1 emission ' + cat_url)
##            #add only emissions with video
##            url = cat_url + '/videos/playlist_' + cat_url.rsplit('/', 1)[-1]
##            if channel.get_status(url):
##                img = 'DefaultVideo.png'
##                channel.addDir(name, img, channel_id=self.channel_id, url=url, action='show_videos', id=cat_id)
# 
    def get_videos(self, datas):
        url = datas.get('url')
        if datas.get('direct', False):
            self.get_direct_videos()
            return
        data = channel.get_url(url)
        soup = BeautifulSoup(data, 'html.parser')
        main = soup.main
        section = soup.find('section', type='videos-list')
        articles = section.find_all('article', card='video')
        for article in articles:
            a = article.find('a')
            title = article.h3.string
            prog_id = a['href']
            prog_url = 'http:'+prog_id
            video = channel.get_url(prog_url)
            regex = r"""videoid="(.+)" """
            id = re.findall(regex,video)[0]
            img = 'http:'+ article.find('img',{'src':True})['src']
            vurl = channel.array2url(channel_id=self.channel_id, url=id, action='play_video')
            channel.addLink(title, vurl, img)

    def get_direct_videos(self):
        url = self.main_url + self.channel_id + '/live'
        data = channel.get_url(url)
        soup = BeautifulSoup(data, 'html.parser')
        main = soup.main
        section = soup.find('section', {'video':True})
        if not section:
            pass
        else:
            time = section.find('time')
            if not time:
                title = section.find('h3').string
            else:
                title = section.find('h3').string + ' - ' + time.string
            id = section.find('script', {'liveid':True})['liveid']
            img =''
            vurl = channel.array2url(channel_id=self.channel_id, url=id, action='play_video', direct='1')
            channel.addLink(title, vurl, img)

    def play_video(self, datas):
        id = datas.get('url')
        url = 'http://www.rtl.be/videos/player/replays/' + id[:-3] + '000/' + id + '.xml'
        if datas.get('direct'):
            url = 'http://www.rtl.be/videos/player/lives/' + id[:-3] + '000/'+ id + '.xml'   
        data = channel.get_url(url)
        #print('xml '+ url)
        soup = BeautifulSoup(data, 'html.parser')
        title = soup.find('title').string
        img = 'http:' + soup.find('thumbnail').string
        urlTag = ['url_hls','url_mp4','url_hds','url_flash']
        i = 0
        flow_url = ''
        while flow_url == '' and i < len(urlTag):
            flow_url = soup.find(urlTag[i]).string
            i += 1
        channel.playUrl(flow_url)
    
##    def get_direct_video_id(self, id):
##        url = 'http://www.rtl.be/videos/player/lives/' + id[:-3] + '000/'+ id + '.xml'
##        data = channel.get_url(url)
##        regex = r"""<URL_HLS>(.+)</"""
##        id = re.findall(regex, data)[0]
##        return id


if __name__ == "__main__":
    import sys
    args = sys.argv
    if len(args) == 1:
        print ('rtltvi clubrtl plugrtl')
    elif len(args) == 3:
        if args[2] == 'direct':
            Channel({'channel_id': args[1], 'action': 'show_videos', 'direct': 1})
        elif args[2] == 'scan_empty':
            Channel({'channel_id': args[1], 'action': 'scan_empty'})
        else:
            Channel({'channel_id': args[1], 'action': 'show_subcategories', 'url':args[2]})
    elif len(args) == 4:
        if args[2] == 'play':
            Channel({'channel_id': args[1], 'action': 'play_video', 'url':args[3]})
        else:
            Channel({'channel_id': args[1], 'action': 'show_videos', 'url':args[3]})
    elif len(args) == 5:
        Channel({'channel_id': args[1], 'action': 'play_video', 'url':args[3], 'direct':'1'})
    else:
        Channel({'channel_id': args[1], 'action': 'show_categories'})
