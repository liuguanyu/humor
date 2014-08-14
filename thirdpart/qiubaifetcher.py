#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liuguanyu -*-
# python抓取糗事百科的所有笑话

import urllib2 , json , os , time , re , hashlib
from thirdpart import jsonpatch , picbidclient

class QiubaiFetcher :
    url = "http://m.qiushibaike.com/hot"
    page_param = "/page/"
    cur_page = 1
    max_page = 5
    article_url = "http://www.qiushibaike.com/article/"
    need_next = True
    date_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    pbc = picbidclient.PicBedClient()
    headers = ('User-Agent','Mozilla/5.0 (Linux; U; Android 4.2.2; zh-CN; GT-I9500 Build/JDQ39) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/533')
                               
    def get(self) :
        url = self.url + self.page_param + str(self.cur_page)
        opener = urllib2.build_opener()
        opener.addheaders = [self.headers]
        return opener.open(url).read()
    
    def make_img_tag(self , picUrl):
        if picUrl == "" :
            return ""
        else:
            pc = self.pbc.save(picUrl)
            pc = picUrl if pc == "" else pc
            return "<p><img src='" + pc + "'/></p>"
        
    def make_content(self , msg):      
        addP = lambda line : "<p>" + line + "</p>" 
        return ''.join([addP(line) for line in msg.split("<br>")])
        
        
    def make_me_url(self , id):
        return self.article_url + id      	

    def parse(self , content):
        # <article id="article_(\d*?)".+?>.*?(?:<div class="m-m fs-m">(.*?)</div>)*?.*?(?:<img.*?class="w-xl".*?src="(.*?)".*?>)*?.*?</article>
        reg = re.compile('<article id="article_(\d*?)".+?>(.*?)</article>', re.IGNORECASE | re.DOTALL | re.MULTILINE)
        text = re.findall(reg , content)    
        
        rets = []        
        if len(text) == 0 :
            self.need_next = False
            return []
        else : 
            for joke in text:
                id = joke[0] 
                inner = joke[1]
                con = "" 
                img = ""
                 
                m = re.search(r'<div class="m-m fs-m">(.*?)</div>' , inner , re.IGNORECASE | re.DOTALL | re.MULTILINE)
                
                if m :
                    con = m.group(1)
                
                m = re.search(r'<img.*?class="w-xl".*?src="(.*?)".*?>' , inner , re.IGNORECASE | re.DOTALL | re.MULTILINE)
                
                if m :
                    img = m.group(1)
                    
                con = self.make_content(con) + self.make_img_tag(img)	    
                               
                rets.append({
                    "title" : "" ,
                    "content" : con ,
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
    qf = QiubaiFetcher()
   
    while qf.is_need_next() :
        con = qf.get()
        ret.extend(qf.parse(con))  

    print ret   

if __name__ == "__main__":
    main()