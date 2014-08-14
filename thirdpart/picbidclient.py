#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liuguanyu -*-
# python图片上到图床

import json , hashlib
import httplib , urllib  
import urlparse
import random
import time
from jsonpatch import * 

import binascii

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

        conn = httplib.HTTPConnection(url_info.hostname  + ":" + ("80" if (url_info.port == "") else str(url_info.port)))  
        conn.request("POST", path , params , headers)  
        response = conn.getresponse()  

        data = response.read()  
        conn.close()  

        return data

    @staticmethod
    def get(url ,  try_time = 3  , timeout=10):
        url_info = urlparse.urlparse(url)
        headers = {
            "Host" : url_info.hostname,
            "Connection" : "close"
        }  
        conn = httplib.HTTPConnection(url_info.hostname  + ":" + ("80" if (url_info.port == "") else str(url_info.port))) 
        path = url_info.path + ("?" + url_info.query if (url_info.query) else url_info.query)
        conn.request("GET", path)  
        response = conn.getresponse()  

        data = response.read()

        if (data == "null"):
            time.sleep(2) # 休息两秒
            
            if try_time > 1 :
                return ReqUtils.get(url , try_time - 1 , timeout)
            else :
                raise Exception('Not Complete Task!')  
        else :    
            return data

class PicBedConf:
    PICA_API_DOMAIN = "api.v3.picasso.qhimg.com"
    PICA_API_PORT   = "80"
    PICA_TIMEOUT = 10
    
    @staticmethod
    def get_upload_api(app):
        return "http://" + PicBedConf.PICA_API_DOMAIN + ":" + PicBedConf.PICA_API_PORT + "/v3/app/"  + app + "/tasks/"; 

    @staticmethod     
    def get_query_tasks_url(app):  
        return "http://" + PicBedConf.PICA_API_DOMAIN + ":" + PicBedConf.PICA_API_PORT + "/v3/app/"  + app + "/query_tasks/";          

class PicBedClient:
    _key = "majiax"
    _src = "0d2efd3ed1bc8e41"
    _up_key = "demo0"
    _version = "3.1.0.40"
    _single = 0
    _try_time = 3
    _OK = "SUCC"

    def __init__ (self , key="" , src=""):
        if key != "" :
            self._key = key

        if src != "" :
            self._src = src

    def post_pic (self , stream) :
        rules = json.dumps({self._up_key:[]},separators=(',',':'))
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
    
        '''修正为PHP的json_encode'''
        data['IMGSTREAM'] = json.dumps([stream]).replace("/" , "\/");
        data['SIGN'] = hashlib.md5(data["IMGSTREAM"] + "|" + rules + "|" + self._key + "|" + self._src  + "|360IMG").hexdigest()

        data = ReqUtils.post(PicBedConf.get_upload_api(self._key) , data);       
        return json.loads(data , object_hook=JsonPatch.decode_dict)    

    def get_res_by_group_id (self , group_id):
        url = PicBedConf.get_query_tasks_url(self._key) + "?GROUPID=" + group_id
        data = ReqUtils.get(url , self._try_time , PicBedConf.PICA_TIMEOUT)     

        return json.loads(data , object_hook=JsonPatch.decode_dict)                

    def save (self , stream):
        res = self.post_pic(stream)

        data = res["DATA"]
        status = res["STATUS"]

        if status == self._OK :
            try :
                msg = self.get_res_by_group_id(data)
                msg = msg[0]

                data = msg["DATA"]
                status = msg["STATUS"]  

                if status == self._OK:
                    imgs = data[self._up_key]["URL"]
                    length = len(imgs)

                    idx = 0 if length < 1 else binascii.crc32(stream) % length; 

                    return imgs[idx]
                else:
                    return "" 
            except Exception :
                return ""                  
        else :   
            return ""

def main():
    pbc = PicBedClient()
    print pbc.save('http://p7.qhimg.com/t016b0fd14ba6b086ae.jpg')

if __name__ == "__main__":
    main()