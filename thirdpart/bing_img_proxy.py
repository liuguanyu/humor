#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liuguanyu -*-
# python抓取bing主页所有背景图片

import urllib , json , os , time
from picbidclient import * 
from jsonpatch import * 

def get_photos(max = 1000) :
    imgs = []    

    for i in range(0 , 1000) :
        url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx='+str(i)+'&n=1&nc='+str(int(time.time()))
        html = urllib.urlopen(url).read()

        if html == 'null':
            break

        pic_info = json.loads(html , object_hook=JsonPatch.decode_dict);
        for node in pic_info["images"]:
            imgs.append({
                "url" : node["url"],
                "hsh" : node["hsh"]
            })
        
    return imgs   

class DefaultSaver : 
    def  __init__ (self , path = None):
        if path is None :            
            if (os.path.exists('photos')== False):
                os.mkdir('photos')
            self.path = 'photos/'
        else :
            self.path = path 

    def save (self , imgUrl) :  
        right = imgUrl.rindex('/')
        name = imgUrl.replace(imgUrl[ : right+1] , '')

        save_path = self.path + name
        urllib.urlretrieve(imgUrl, save_path)

class PicSaver :
    def __init__ (self , saver = None):
        if saver is None :
           self.saver = DefaultSaver()
        else:   
           self.saver = saver

    def save (self , imgUrl):
        self.saver.save(imgUrl)       

def main():
    max  = 1000  
    imgs = get_photos(max)
    ps = PicSaver()
    ps2 = PicBedClient()
    for img in imgs:
        ps.save(img["url"])

if __name__ == "__main__":
    main()