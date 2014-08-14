#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liuguanyu -*-
# python抓取快乐麻花的所有笑话

import urllib2 , json , os , time , re , hashlib
from thirdpart import jsonpatch , picbidclient 

class MahuaFetcher :
    url = "http://m.mahua.com/"
    page_inited = False
    page_start_1 = 0
    cur_page = 1
    max_page = 5
    article_url = "http://m.mahua.com/xiaohua/%s.htm"
    need_next = True
    pbc = picbidclient.PicBedClient()
    headers = ('User-Agent','Mozilla/5.0 (Linux; U; Android 4.2.2; zh-CN; GT-I9500 Build/JDQ39) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/533')
                               
    def get(self) :
        if self.page_inited :
            url = self.url + "newjokes/index_" + str(int(self.page_start_1) - self.cur_page + 1) + ".htm"
        else :    
            url = self.url 
 
        opener = urllib2.build_opener()
        opener.addheaders = [self.headers]
        data = opener.open(url).read()

        data = data.decode("gbk").encode("utf8")

        if self.page_inited == False :
            m = re.search(r'mahua.T=(\d+)' , data , re.IGNORECASE | re.DOTALL | re.MULTILINE)
            if m :
                self.page_inited = True
                self.page_start_1 = int(m.group(1))   
        return data
    
    def make_img_tag(self , picUrl):
        if picUrl == "" :
            return ""
        else:
            pc = self.pbc.save(picUrl)
            pc = picUrl if pc == "" else pc
            return "<p><img src='" + pc + "'/></p>"      
        
    def make_me_url(self , id):
        return self.article_url.replace("%s" , id)	

    def parse(self , content):
        reg = re.compile('<div class="mahua">(.*?)</div>', re.IGNORECASE | re.DOTALL | re.MULTILINE)
        text = re.findall(reg , content)  
        rets = []  

        if len(text) == 0 :
            self.need_next = False
            return []
        else :
            for joke in text:
                id = ""
                title = ""

                img = ""
                content = ""

                # 找到标题
                m = re.search(r'<h3 id="t_(\d*?)"><a.*?>(.*?)</a></h3>' , joke , re.IGNORECASE | re.DOTALL | re.MULTILINE) 
                if m :
                    id = m.group(1)
                    title = m.group(2)

                # 找图  
                m = re.search(r'<img.*?src="(.*?)".*?>'  , joke , re.IGNORECASE | re.DOTALL | re.MULTILINE)

                if m :
                    img = m.group(1)

                    if joke.find('播放动态图') >= 0 :
                        img = img.replace('.jpg' ,  '.gif')
                        continue
                else :         
                    m = re.search(r'<img.*?src=(.*?)\s+?/>'  , joke , re.IGNORECASE | re.DOTALL | re.MULTILINE)

                    if m :
                        img = m.group(1)

                        if joke.find('播放动态图') >= 0 :
                            img = img.replace('.jpg' ,  '.gif')
                            continue

                # 找内容
                m = re.search(r'<div.*?class="content".*?>(.*?)</div>' , joke , re.IGNORECASE | re.DOTALL | re.MULTILINE)
                if m : 
                    content = m.group(1) 

                con = content + self.make_img_tag(img)

                rets.append({
                    "content" : con ,
                    "title" : title ,
                    "url" : self.make_me_url(id),
                    "content_md5" : hashlib.md5(con).hexdigest()
                })

            self.cur_page = self.cur_page + 1    
             
            if self.cur_page >= self.max_page:
                self.need_next = False
                
            return rets

    def is_need_next (self):
        return self.need_next            
    
def main():    
    ret = [] 
    mf = MahuaFetcher()

    while mf.is_need_next() :
        con = mf.get()
        ret.extend(mf.parse(con))  

    print ret  

if __name__ == "__main__":
    main()