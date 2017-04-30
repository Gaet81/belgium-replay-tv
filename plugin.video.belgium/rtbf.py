#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import channel
import HTMLParser
from bs4 import BeautifulSoup

id2skip = [str(x) for x in [5683,2913,5614,5688,156]] # Empty program

menu = {'rtbfTV': {'name': 'Chaînes TV', 'icon': 'rtbf-all.png','module': 'rtbf','action': 'show_tv'},
            'rtbfRadio': {'name': 'Chaînes radios', 'icon': 'radios.png','module': 'rtbf','action': 'show_radio'},
            'rtbfAll': {'name': 'Toutes les émissions', 'icon': 'rtbf.png','module': 'rtbf','action': 'show_programs'},
            'rtbfCat': {'name': 'Par catégories', 'icon': 'rtbf.png','module': 'rtbf','action': 'show_subcategories'},
            'rtbfLive': {'name': 'Directs', 'icon': 'rtbf.png','module': 'rtbf','action': 'get_lives'}
            }

channelsTV = {'laune': {'name': 'La Une', 'icon': 'laune.png','module':'rtbf'},
            'ladeux': {'name': 'La Deux', 'icon': 'ladeux.png','module':'rtbf'},
            'latrois': {'name': 'La Trois', 'icon': 'latrois.png','module':'rtbf'},
            }
channelsRadio = {'lapremiere': {'name': 'La Première', 'icon': 'lapremiere.png','module':'rtbf'},
            'vivacite': {'name': 'Vivacité', 'icon': 'vivacite.png','module':'rtbf'},
            'musiq3': {'name': 'Musiq 3', 'icon': 'musiq3.png','module':'rtbf'},
            'classic21': {'name': 'Classic 21', 'icon': 'classic21.png','module':'rtbf'},
            'purefm': {'name': 'Pure', 'icon': 'purefm.png','module':'rtbf'},
            }
categories = {'35':{'name': 'Series', 'icon': 'rtbf.png','module': 'rtbf'},
             '36':{'name': 'Films', 'icon': 'rtbf.png','module': 'rtbf'},
             '1':{'name': 'Info', 'icon': 'rtbf.png','module': 'rtbf'},
             '9':{'name': 'Sport', 'icon': 'rtbf.png','module': 'rtbf'},
             '11':{'name': 'Football', 'icon': 'rtbf.png','module': 'rtbf'},
             '40':{'name': 'Humour', 'icon': 'rtbf.png','module': 'rtbf'},
             '29':{'name': 'Divertissement', 'icon': 'rtbf.png','module': 'rtbf'},
             '44':{'name': 'Vie Quotidienne', 'icon': 'rtbf.png','module': 'rtbf'},
             '31':{'name': 'Documentaire', 'icon': 'rtbf.png','module': 'rtbf'},
             '18':{'name': 'Culture', 'icon': 'rtbf.png','module': 'rtbf'},
             '23':{'name': 'Musique', 'icon': 'rtbf.png','module': 'rtbf'},
             '32':{'name': 'Enfants', 'icon': 'rtbf.png','module': 'rtbf'}
            }
liveURL = {'La Une':'http://rtbf.l3.freecaster.net/live/rtbf/geo/open/bc1e985c9592276a91bf1db4a6dd366efc9fc11e/laune.m3u8?token=0db0ad0d41931810f148c',
           'La Deux':'http://rtbf.l3.freecaster.net/live/rtbf/geo/open/87d88b36830bb0d0ff43b139615cffd0a4a93440/ladeux.m3u8?token=0f4d7af3370022aee98bf',
           'La Trois':'http://rtbf.l3.freecaster.net/live/rtbf/geo/open/2e54586bb99b57a87004a7cafba990a213361120/latrois.m3u8?token=00ed017e3c279a25b31fa',
           'Pure':'http://rtbf.l3.freecaster.net/live/rtbf/geo/open/abb1916b08d3b03ffd00218d3d48deda80aa3898/purevision.m3u8?token=04fe5b90b1d52355f235d',
           'Vivacité':'http://rtbf.l3.freecaster.net/live/rtbf/geo/open/7c0c51a7546e72c823e08b6dff63d8d2d86413e9/vivacitevision.m3u8?token=0be710476533d5870f7d3'
          }

class Channel(channel.Channel):
    def get_main_url(self):
        return 'https://www.rtbf.be'
    
    def categories(self):
        return categories
    
    def get_categories(self):
        for menu_id, ch in menu.iteritems():
            if channel.in_xbmc:
                icon = channel.xbmc.translatePath(channel.os.path.join(channel.home, 'resources/' + ch['icon']))
                channel.addDir(ch['name'], icon, channel_id=menu_id, action=ch['action'])
            else:
                print ch['name'], menu_id, 'show_programs'
    
    def get_programs(self, skip_empty_id=True):
        data = channel.get_url(self.main_url + '/auvio/emissions/')
        regex = r"""<header class="rtbf-media-item__header">\s*<a\s+href="([^"]+)[^>]+>\s*<h4[^>]*>([^<]+)"""
        icon = None
        for url, name in re.findall(regex, data):
            id = url.split('?id=')[1]
            if skip_empty_id and id in id2skip:
                continue
            channel.addDir(name, icon, channel_id=self.channel_id, url=url, action='show_videos', id=id)

    def show_tv(self, datas):
        for channel_id, ch in channelsTV.iteritems():
            if channel.in_xbmc:
                icon = channel.xbmc.translatePath(channel.os.path.join(channel.home, 'resources/' + ch['icon']))
                channel.addDir(ch['name'], icon, channel_id=channel_id, action='show_channel')
            else:
                print ch['name'], channel_id, 'show_channel'

    def show_radio(self, datas):
        for channel_id, ch in channelsRadio.iteritems():
            if channel.in_xbmc:
                icon = channel.xbmc.translatePath(channel.os.path.join(channel.home, 'resources/' + ch['icon']))
                channel.addDir(ch['name'], icon, channel_id=channel_id, action='show_channel')
            else:
                print ch['name'], channel_id, 'show_channel'
                   
    def get_subcategories(self, datas):
        for category_id, cat in categories.iteritems():
            channel.addDir(name=cat['name'], iconimage='DefaultVideo.png', channel_id=category_id, action='show_category')

    def get_category(self, datas):
        urlName = datas.get('name').replace(' ','-')
        data = channel.get_url(self.main_url+'/auvio/categorie/'+urlName+'?id='+datas.get('channel_id'))
        soup = BeautifulSoup(data, 'html.parser')
        main = soup.main
        section = main.section
        articles = section.find_all('article')
        for article in articles:
            icons = article.find('img',{'data-srcset':True})['data-srcset']
            regex = r""",([^,]+?\.(?:jpg|gif|png|jpeg))\s640w"""
            icon = str(re.findall(regex, icons)[0])
            container = article.h3
            url = container.find('a',{'href':True})['href']
            id = url.split('?id=')[1]
            name = container.find('a', {'title':True})['title']     
            channel.addDir(name, icon, channel_id=datas.get('channel_id'), url=url, action='show_videos', id=id)

    def get_channel(self, datas):
        data = channel.get_url(self.main_url + '/auvio/emissions/')
        try:
            ch = channelsTV[datas.get('channel_id')]['name']
        except:
            ch = channelsRadio[datas.get('channel_id')]['name']
        regex = r"""(?s)<header class="rtbf-media-item__header">\s*<a\s+href="([^"]+)[^>]+>\s*<h4[^>]*>([^<]+).*?<div class="rtbf-media-item__meta-bottom">([^<]+)"""
        icon = None
        for url, name, chan in re.findall(regex, data):
            if ch in chan.strip():
                id = url.split('?id=')[1]
                channel.addDir(name, icon, channel_id=self.channel_id, url=url, action='show_videos', id=id)


    def get_lives(self, datas):
        def parse_lives(data):
            regex = r""",([^,]+?\.(?:jpg|gif|png|jpeg))\s648w"[^/]*/>(?s).*?"rtbf-media-item__title">\s*<a href="([^"]+)"\s*title="([^"]+)"""
            for icon, url, name in re.findall(regex, data, flags=re.DOTALL):
                vurl = channel.array2url(channel_id=self.channel_id, url=url, action='play_live')
                channel.addLink(name.replace('&#039;', "'").replace('&#034;', '"') , vurl, icon) # + ' - ' + date
        live_url = self.main_url + '/auvio/direct/'
        data = channel.get_url(live_url)
        parse_lives(data)

    
    def get_videos(self, datas):
        url = datas.get('url')
        print 'get_videos url:', url
        data = channel.get_url(url)
        print 'After get_url [%s]' % len(data)
        soup = BeautifulSoup(data, 'html.parser')
        print 'soup'
        sections = soup.find_all('section',{'class':True,'id':True})
        print 'soup find all'
        for section in sections:
            print '--section--'
            if section['id']=='widget-ml-avoiraussi-':
                continue
            print '--section 2--'
            regex = r"""(?s)<h3[^<]*<a href="([^"]+)"[^>]*>([^<]+)</a></h3>.*?<time.*?>([^<]+)</time>"""
            try:
                results = re.findall(regex, str(section))
            except:
                continue
            print '--section 3--'
            for url, title, date in results:
                title = title + ' - ' + date
                vurl = channel.array2url(channel_id=self.channel_id, url=url, action='play_video')
                channel.addLink(title.replace('&#039;', "'").replace('&#034;', '"'), vurl, None)
   
                
    def play_video(self, datas):
        url = datas.get('url')
        data = channel.get_url(url)
        regex = r"""src="(https://www.rtbf.be/auvio/embed/media[^"]+)"""
        iframe_url = re.findall(regex, data)[0]
        data = channel.get_url(iframe_url)
        regex = r"""data-media="([^"]+)"""
        media = re.findall(regex, data)[0]
        h = HTMLParser.HTMLParser()
        media_json = h.unescape(media)
        regex = r""""high":"([^"]+)"""
        all_url = re.findall(regex, media_json)
        if len(all_url) > 0:
          video_url = all_url[0]
        else:
            regex = r"""url&quot;:&quot;([^&]+)"""
            iframe_url = re.findall(regex, data)[0]
            video_url = iframe_url.replace("\\", "")     
        channel.playUrl(video_url)


    def play_live(self, datas):
        url = datas.get('url')
        data = channel.get_url(url)
        regex = r"""src="(https://www.rtbf.be/auvio/embed/direct[^"]+)"""
        iframe_urls = re.findall(regex, data)
        #avoid issue if a login is required like belgian reddevils match
        if len(iframe_urls)>0:
            rtmp = self.get_live_rtmp(iframe_urls[0])
            channel.playUrl(rtmp)
        else:
            regex = r"""(?s)<header class="rtbf-media-detail__header container-fluid www-container-md www-rel js-media-header">.*?<li><span class="www-cap">([^<]+)*</span>"""
            channelString = re.findall(regex, data)[0]
            stream_url = liveURL[channelString]
            data = channel.get_url(stream_url)
            best_resolution_path = data.split("\n")[-2]
            hls_stream_url = stream_url[:stream_url.rfind('open')] + best_resolution_path[6:]
            channel.playUrl(hls_stream_url)



    def get_live_rtmp(self, page_url):
        print "live stream!"
        data = channel.get_url(page_url)
        regex = r"""streamName&quot;:&quot;([^&]+)"""
        stream_name = re.search(regex, data)
        if stream_name is None:
            return None
        stream_name = stream_name.group(1)
        print "stream name: >" + stream_name + "<"
        if stream_name == 'freecaster':
            print "freecaster stream"
            regex = r"""streamUrl&quot;:&quot;([^&]+)"""
            freecaster_stream =  re.search(regex, data)
            freecaster_stream = freecaster_stream.group(1)
            freecaster_stream=freecaster_stream.replace("\\", "") 
            return freecaster_stream
        else:
            print "not a freecaster stream"
            regex = r"""streamUrlHls&quot;:&quot;([^&]+)"""
            hls_stream_url = re.search(regex,data)
            if hls_stream_url is not None:
                print "HLS stream"
                stream_url = hls_stream_url.group(1).replace("\\", "")
                data = channel.get_url(stream_url)
                best_resolution_path = data.split("\n")[-2]
                hls_stream_url = stream_url[:stream_url.rfind('open')] + best_resolution_path[6:]
                print "HLS stream url: >" + hls_stream_url + "<"
                return hls_stream_url
            else:
                regex = r"""streamUrl&quot;:&quot;([^&]+)"""
                stream_url = re.search(regex,data)
                if stream_url is not None:
                    stream_url = stream_url.group(1)
                    stream_url = stream_url.replace("\\", "")
                    print "strange stream" 
                    print "stream url: >" + stream_url + "<"
                    return stream_url
                else:
                    print "normal stream"
                    token_json_data = channel.get_url(self.main_url + '/api/media/streaming?streamname=' + stream_name, referer=page_url)
                    token = token_json_data.split('":"')[1].split('"')[0]
                    swf_url = 'http://static.infomaniak.ch/livetv/playerMain-v4.2.41.swf?sVersion=4%2E2%2E41&sDescription=&bLd=0&sTitle=&autostart=1'
                    rtmp = 'rtmp://rtmp.rtbf.be/livecast'
                    page_url = 'http://www.rtbf.be'
                    play = '%s?%s' % (stream_name, token)
                    rtmp += '/%s swfUrl=%s pageUrl=%s tcUrl=%s' % (play, swf_url, page_url, rtmp)
                    return rtmp
