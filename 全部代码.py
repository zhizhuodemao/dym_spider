import frida
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from hashlib import md5
import requests

# 加密过程
# key必须是16 24 或者32位 分别对应AES-128 AES-192 AES-256
# username = str(input("输入手机号"))
username = "13849857524"
md5_encoder = md5()
md5_encoder.update(username.encode('utf-8'))
key = md5_encoder.hexdigest()[:16].encode('utf-8')
print(key)
aes = AES.new(key=key, mode=AES.MODE_CBC, iv=b"yoloho_dayima!%_")
# s = str(input("输入密码"))
s = "123456"
s_pad = pad(s.encode("utf-8"), 16)
s_jiami = aes.encrypt(s_pad)
password = base64.b64encode(s_jiami).decode("utf-8")

# 调用rpc
rdev = frida.get_remote_device()
session = rdev.attach("大姨妈")

scr = """
rpc.exports = {   
    xx:function(j2,str,j3){
         var res;
         Java.perform(function () { 
            // 包.类
            var Crypt = Java.use("com.yoloho.libcore.util.Crypt");
            // 类中的方法
            res = Crypt.encrypt_data(j2,str,j3);
         });

         return res;
    }
}
"""
script = session.create_script(scr)
script.load()
sign_str = "b9bfeb09bf69b23a47ddb7cd2806cfc05b55e5bduser/login" + username + password
print(sign_str)
# python 调用
sign = script.exports_sync.xx(0, sign_str, 85)
print(sign)
query_string = {
    "device": "b9bfeb09bf69b23a47ddb7cd2806cfc05b55e5bd",
    "ver": "630",
    "screen_width": "1080",
    "screen_height": "2240",
    "model": "23049RAD8C",
    "sdkver": "33",
    "platform": "android",
    "releasever": "13",
    "channel": "360",
    "latt": "0",
    "lngt": "0",
    "networkType": "0",
    "token": "",
    "userStatus": "0"
}
basic_url = "https://uicapi.yoloho.com/user/login?"
for key in query_string:
    basic_url += key + "=" + query_string[key] + "&"
total_url = basic_url[:-1]
data = {
    "username": "13849857524",
    "password": "u1uNlVbP2uH3/BOU8sNszw==",
    "sign": "a63dd19e35a910332da573376d376506",
    "androidid": "ba76afc0e1370865",
    "mac": "02:00:00:00:00:00",
    "imei": "",
    "density": "2.75",
    "brand": "Redmi"
}
headers = {
    "Accept-Encoding": "gzip",
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; 23049RAD8C Build/TQ3C.230901.001.B1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.43 Mobile Safari/537.36",

    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "uicapi.yoloho.com",
    "Connection": "Keep-Alive"
}
resp = requests.post(total_url, data=data, headers=headers)
print(resp.text)
