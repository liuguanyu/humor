#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liuguanyu -*-
# python图片上到图床

import json , hashlib
import httplib , urllib  
import urlparse

class ReqUtils: 
    @staticmethod
    def post(url , params):
        url_info = urlparse.urlparse(url)

        params = urllib.urlencode(params)
        path = url_info.path + ("?" + url_info.query if (url_info.query) else url_info.query)

        headers = {
            "Host" : url_info.hostname,
            "Content-type" : "application/x-www-form-urlencoded",
            "Content-length": len(params),  
            "Connection" : "close",
            "Accept": "text/plain"
        }  

        print params

        conn = httplib.HTTPConnection(url_info.hostname  + ":" + ("80" if (url_info.port == "") else str(url_info.port)))  
        conn.request("POST", path , params, headers)  
        response = conn.getresponse()  

        data = response.read()  
        print data
        conn.close()  

class PicBedConf:
    PICA_API_DOMAIN = "api.v3.picasso.qhimg.com"
    PICA_API_PORT   = "80"

    def get_upload_api(self , app):
        return "http://" + self.PICA_API_DOMAIN + ":" + self.PICA_API_PORT + "/v3/app/"  + app + "/upload_pics/";  

class PicBedClient:
    _key = "majiax"
    _src = "0d2efd3ed1bc8e41"
    _upKey = "demo0"
    _version = "3.1.0.40"
    _single = 0

    def __init__(self , key="" , src=""):
        pass

    def add_to_pic_bed(self , stream):
        rules = json.dumps({self._upKey:[]}).replace(" " , "") 
        data = {}
        data["RULES"] = rules
        data["APP"]   = self._key
        data["VER"]   = self._version
        data["NOTIFYOPT"] = json.dumps([])
        data["CURLOPT"] = json.dumps([])
        data["FILTER"] = json.dumps([])
        data["EFFECTIVE"] = json.dumps(False)
        data["PRIORITY"] = "\"HIGH\""

        data['TYPE'] = self._single
    
        data['IMGSTREAM'] = json.dumps([urllib.quote_plus(stream)]);

        data['SIGN'] = hashlib.md5(data["IMGSTREAM"] + "|" + rules + "|" + self._key + "|" + self._src  + "|360IMG").hexdigest()

        pbclt = PicBedConf()
        ReqUtils.post(pbclt.get_upload_api(self._key) , data);

def main():
    pbc = PicBedClient()
    pbc.add_to_pic_bed('http://www.baidu.com/img/baidu_jgylogo3.gif')

if __name__ == "__main__":
    main()