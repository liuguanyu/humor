#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liuguanyu -*-
# python抓取360笑话的所有笑话

import urllib , json , os , time , re
from picbidclient import * 
from jsonpatch import * 

class Hao360Fetcher :
    url = "http://xiaohua.hao.360.cn"
    page_param = "/?page="
    cur_page = 1
    need_next = True
    date_now = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def get(self) :
        url = self.url + self.page_param + str(self.cur_page)
        return urllib.urlopen(url).read()

    #图片已经在图床，不用再抓    
    def make_img_tag(self , picUrl) :
        if picUrl == "" :
            return ""
        else :    
            return "<p><img src='" + picUrl + "'/></p>"  

    def is_need_next (self):
        return self.need_next         

    def make_me_url(self , id) :
        return self.url + "/tj?id=" + id      

    def make_content(self , content):
        if "" == content :
            return ""
        else :
            return ''.join(["<p>" + p + "</p>" for p in content.split("##")])        

    def parse(self , content) :
        reg = re.compile('var JOKEDATA =(.*?);' , re.S)
        text = re.findall(reg , content)    
        
        if len(text) == 0 :
            self.need_next = False
            return []
        else :
            text = text[0]
            text = json.loads(text , object_hook=JsonPatch.decode_dict)

            ret = []
            for item in text :
                node = text[item] 

                jokes  = node["joke"]
                guesses = node["guess"]

                for joke in jokes :
                    con = self.make_content(joke["content"]) + self.make_img_tag(joke["img"])

                    ret.append({
                        "title" : joke["title"] , 
                        "content" : con ,
                        "tag" : joke["tag"] ,
                        "url" : self.make_me_url(joke["id"]) ,
                        "comment_url" : joke["commentUrl"] , 
                        "content_md5" : hashlib.md5(con).hexdigest()
                    }) 

                    pub_time = joke["publishDate"][0:10]


                    if pub_time < self.date_now:
                        self.need_next = False

                '''     
                # 暂时还是小图，需想想怎么抓
                for guess in guesses :
                    print json.dumps(guess , indent=4)    
                    break 
                '''   
            if self.is_need_next() == True :
                self.cur_page = self.cur_page + 1

            return ret        

def main():    
    ret = [] 
    hf = Hao360Fetcher()

    while hf.is_need_next() :
        con = hf.get()
        ret.extend(hf.parse(con))  

    print ret    

if __name__ == "__main__":
    main()