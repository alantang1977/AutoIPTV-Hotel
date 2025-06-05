import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import re
import os
import threading
from queue import Queue
import eventlet

# Monkey patching for eventlet
eventlet.monkey_patch()

urls = [
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iSGViZWki",  # Hebei (河北)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iYmVpamluZyI%3D",  # Beijing (北京)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iZ3Vhbmdkb25nIg%3D%3D",  # Guangdong (广东)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbmdoYWki",  # Shanghai (上海)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0idGlhbmppbiI%3D",  # Tianjin (天津)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iY2hvbmdxaW5nIg%3D%3D",  # Chongqing (重庆)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbnhpIg%3D%3D",  # Shanxi (山西)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhYW54aSI%3D",  # Shaanxi (陕西)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ibGlhb25pbmci",  # Liaoning (辽宁)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iamlhbmdzdSI%3D",  # Jiangsu (江苏)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iemhlamlhbmci",  # Zhejiang (浙江)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5a6J5b69Ig%3D%3D",  # Anhui (安徽)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iRnVqaWFuIg%3D%3D",  # 福建
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rGf6KW%2FIg%3D%3D",  # 江西
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5bGx5LicIg%3D%3D",  # 山东
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rKz5Y2XIg%3D%3D",  # 河南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5YyXIg%3D%3D",  # 湖北
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5Y2XIg%3D%3D",  # 湖南
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYmVpamluZyI=",  # 北京
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hhbmdoYWki",  # 上海
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0idGlhbmppbiI=",  # 天津
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYW5zaGFuIg==",  # 鞍山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYW55YW5nIg==",  # 安阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYmFpY2hlbmci",  # 白城
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYmFvZGluZyI=",  # 保定
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYmVueGki",  # 本溪
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYm96aG91Ig==",  # 亳州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2FuZ3pob3Ui",  # 沧州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hhb3lhbmci",  # 朝阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hhb3pob3Ui",  # 潮州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hlbmdkZSI=",  # 承德
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hlbmdkdSI=",  # 成都
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hpZmVuZyI=",  # 赤峰
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2h1eGlvbmci",  # 楚雄
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2h1emhvdSI=",  # 滁州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iZGFsaWFuIg==",  # 大连
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iZG9uZ2d1YW4i",  # 东莞
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iZnV5YW5nIg==",  # 阜阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iZnV6aG91Ig==",  # 福州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iZ2FuemhvdSI=",  # 赣州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iZ3Vhbmd6aG91Ig==",  # 广州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iZ3VpeWFuZyI=",  # 贵阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGFuZGFuIg==",  # 邯郸
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGFuZ3pob3Ui",  # 杭州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGViaSI=",  # 鹤壁
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGVmZWki",  # 合肥
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGVuZ3NodWki",  # 衡水
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGVuZ3lhbmci",  # 衡阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaGV6ZSI=",  # 菏泽
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaHVhaWh1YSI=",  # 怀化
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaHVhaW5hbiI=",  # 淮南
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaHVhbmdnYW5nIg==",  # 黄冈
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaHVhbmdzaGFuIg==",  # 黄山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaHVpemhvdSI=",  # 惠州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamlhbXVzaSI=",  # 佳木斯
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamlhbmdtZW4i",  # 江门
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamlhb3p1byI=",  # 焦作
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamluYW4i",  # 济南
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamluZ2RlemhlbiI=",  # 景德镇
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamluZ3pob3Ui",  # 荆州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamluemhvbmci",  # 晋中
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iamluemhvdSI=",  # 锦州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaml1amlhbmci",  # 九江
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iaml4aSI=",  # 鸡西
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ia2FpZmVuZyI=",  # 开封
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ia3VubWluZyI=",  # 昆明
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibGFpYmluIg==",  # 来宾
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibGFuZ2Zhbmci",  # 廊坊
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibGFuemhvdSI=",  # 兰州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibGlhb3l1YW4i",  # 辽源
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibGlueWki",  # 临沂
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibG91ZGki",  # 娄底
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibHVvaGUi",  # 漯河
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibHVveWFuZyI=",  # 洛阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibWFvbWluZyI=",  # 茂名
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibWVpemhvdSI=",  # 梅州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibmFuY2hhbmci",  # 南昌
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibmFuamluZyI=",  # 南京
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibmFubmluZyI=",  # 南宁
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ibmFueWFuZyI=",  # 南阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0icGluZ2RpbmdzaGFuIg==",  # 平顶山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0icHV5YW5nIg==",  # 濮阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0icWluZ2RhbyI=",  # 青岛
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0icXVhbnpob3Ui",  # 泉州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2FubWVueGlhIg==",  # 三门峡
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hhbiI=",  # 佛山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hhbmdxaXUi",  # 商丘
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hhbmdyYW8i",  # 上饶
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hhbnRvdSI=",  # 汕头
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hlbnlhbmci",  # 沈阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hlbnpoZW4i",  # 深圳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2hpamlhemh1YW5nIg==",  # 石家庄
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2h1YW5neWFzaGFuIg==",  # 双鸭山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic2lwaW5nIg==",  # 四平
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ic3V6aG91Ig==",  # 苏州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0idGFpeXVhbiI=",  # 太原
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0idGFuZ3NoYW4i",  # 唐山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0idGVuZ3pob3Ui",  # 滕州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0idGllbGluZyI=",  # 铁岭
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0id2FmYW5nZGlhbiI=",  # 瓦房店
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0id2VpZmFuZyI=",  # 潍坊
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0id3VoYW4i",  # 武汉
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0id3VodSI=",  # 芜湖
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0id3V4aSI=",  # 无锡
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieGlhbiI=",  # 西安
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieGlhbnlhbmci",  # 咸阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieGljaGFuZyI=",  # 西昌
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieGluZ3RhaSI=",  # 邢台
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieGlueGlhbmci",  # 新乡
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieGlueWFuZyI=",  # 信阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieHVjaGFuZyI=",  # 许昌
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieHV6aG91Ig==",  # 徐州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWFuZ2ppYW5nIg==",  # 阳江
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWFudGFpIg==",  # 烟台
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWljaHVuIg==",  # 宜春
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWluY2h1YW4i",  # 银川
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWluZ2tvdSI=",  # 营口
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWluZ3RhbiI=",  # 鹰潭
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieWl5YW5nIg==",  # 益阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieW9uZ3pob3Ui",  # 永州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieXVleWFuZyI=",  # 岳阳
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hhbmdjaHVuIg==",  # 长春
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhhbmdqaWFrb3Ui",  # 张家口
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hhbmdzaGEi",  # 长沙
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iY2hhbmd6aGki",  # 长治
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhhbmd6aG91Ig==",  # 漳州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhhbmppYW5nIg==",  # 湛江
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhlbmd6aG91Ig==",  # 郑州
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhlbmppYW5nIg==",  # 镇江
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhvbmdzaGFuIg==",  # 中山
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemhvdWtvdSI=",  # 周口
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemh1aGFpIg==",  # 珠海
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemh1bWFkaWFuIg==",  # 驻马店
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iemh1emhvdSI=",  # 株洲
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0iYmFvdG91Ig==",  # 包头
    "https://fofa.info/result?qbase64=IlpIR1hUViIgJiYgY2l0eT0ieml5YW5nIg==",  # 资阳
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iSGViZWki",  # Hebei (河北)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iYmVpamluZyI%3D",  # Beijing (北京)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iZ3Vhbmdkb25nIg%3D%3D",  # Guangdong (广东)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbmdoYWki",  # Shanghai (上海)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0idGlhbmppbiI%3D",  # Tianjin (天津)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iY2hvbmdxaW5nIg%3D%3D",  # Chongqing (重庆)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ic2hhbnhpIg%3D%3D",  # Shanxi (山西)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhYW54aSI%3D",  # Shaanxi (陕西)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0ibGlhb25pbmci",  # Liaoning (辽宁)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iamlhbmdzdSI%3D",  # Jiangsu (江苏)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iemhlamlhbmci",  # Zhejiang (浙江)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5a6J5b69Ig%3D%3D",  # Anhui (安徽)
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iRnVqaWFuIg%3D%3D",  # 福建
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rGf6KW%2FIg%3D%3D",  # 江西
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5bGx5LicIg%3D%3D",  # 山东
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rKz5Y2XIg%3D%3D",  # 河南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5YyXIg%3D%3D",  # 湖北
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5rmW5Y2XIg%3D%3D",  # 湖南
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22hebei%22",        #河北
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22beijing%22",   #北京
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22guangdong%22",    #广东
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shanghai%22",    #上海
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22tianjin%22",    #天津
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22chongqing%22",    #重庆
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shanxi%22",    #山西
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shaanxi%22",    #陕西
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22liaoning%22",    #辽宁
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22jiangsu%22",    #江苏
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22zhejiang%22",    #浙江
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22anhui%22",    #安徽
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22fujian%22",    #福建
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22jiangxi%22",    #江西
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22shandong%22",    #山东
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22henan%22",    #河南
    "https://www.zoomeye.org/searchResult?q=%2Fiptv%2Flive%2Fzh_cn.js%20%2Bcountry%3A%22CN%22%20%2Bsubdivisions%3A%22hubei%22",    #湖北
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2ljaHVhbiI%3D",  # 四川
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0i5LqR5Y2XIg%3D%3D",  # 云南
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iQ2hvbmdxaW5nIg%3D%3D",  # 重庆
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iR3VpemhvdSI%3D",  # 贵州
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iU2hhbnhpIg%3D%3D",  # 山西
    "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iR3Vhbmd4aSBaaHVhbmd6dSI%3D",  # 广西
]

def modify_urls(url):
    modified_urls = []
    ip_start_index = url.find("//") + 2
    ip_end_index = url.find(":", ip_start_index)
    base_url = url[:ip_start_index]  # http:// or https://
    ip_address = url[ip_start_index:ip_end_index]
    port = url[ip_end_index:]
    ip_end = "/iptv/live/1000.json?key=txiptv"
    for i in range(1, 256):
        modified_ip = f"{ip_address[:-1]}{i}"
        modified_url = f"{base_url}{modified_ip}{port}{ip_end}"
        modified_urls.append(modified_url)

    return modified_urls

def is_url_accessible(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return url
    except requests.exceptions.RequestException:
        pass
    return None

results = []

for url in urls:
    # 创建一个Chrome WebDriver实例
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    # 使用WebDriver访问网页
    driver.get(url)  # 将网址替换为你要访问的网页地址
    time.sleep(10)
    # 获取网页内容
    page_content = driver.page_source

    # 关闭WebDriver
    driver.quit()

    # 查找所有符合指定格式的网址
    pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
    urls_all = re.findall(pattern, page_content)
    urls = set(urls_all)  # 去重得到唯一的URL列表
    x_urls = []
    for url in urls:  # 对urls进行处理，ip第四位修改为1，并去重
        url = url.strip()
        ip_start_index = url.find("//") + 2
        ip_end_index = url.find(":", ip_start_index)
        ip_dot_start = url.find(".") + 1
        ip_dot_second = url.find(".", ip_dot_start) + 1
        ip_dot_three = url.find(".", ip_dot_second) + 1
        base_url = url[:ip_start_index]  # http:// or https://
        ip_address = url[ip_start_index:ip_dot_three]
        port = url[ip_end_index:]
        ip_end = "1"
        modified_ip = f"{ip_address}{ip_end}"
        x_url = f"{base_url}{modified_ip}{port}"
        x_urls.append(x_url)
    urls = set(x_urls)  # 去重得到唯一的URL列表

    valid_urls = []
    # 多线程获取可用url
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for url in urls:
            url = url.strip()
            modified_urls = modify_urls(url)
            for modified_url in modified_urls:
                futures.append(executor.submit(is_url_accessible, modified_url))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                valid_urls.append(result)

    for url in valid_urls:
        print(url)
    # 遍历网址列表，获取JSON文件并解析
    for url in valid_urls:
        try:
            # 发送GET请求获取JSON文件，设置超时时间为0.5秒
            ip_start_index = url.find("//") + 2
            ip_dot_start = url.find(".") + 1
            ip_index_second = url.find("/", ip_dot_start)
            base_url = url[:ip_start_index]  # http:// or https://
            ip_address = url[ip_start_index:ip_index_second]
            url_x = f"{base_url}{ip_address}"

            json_url = f"{url}"
            response = requests.get(json_url, timeout=0.5)
            json_data = response.json()

            try:
                # 解析JSON文件，获取name和url字段
                for item in json_data['data']:
                    if isinstance(item, dict):
                        name = item.get('name')
                        urlx = item.get('url')
                        if ',' in urlx:
                            urlx = "aaaaaaaa"
                        # if 'http' in urlx or 'udp' in urlx or 'rtp' in urlx:
                        if 'http' in urlx:
                            urld = f"{urlx}"
                        else:
                            urld = f"{url_x}{urlx}"

                        if name and urlx:
                            # 删除特定文字
                            name = name.replace("cctv", "CCTV")
                            name = name.replace("中央", "CCTV")
                            name = name.replace("央视", "CCTV")
                            name = name.replace("高清", "")
                            name = name.replace("超高", "")
                            name = name.replace("HD", "")
                            name = name.replace("标清", "")
                            name = name.replace("频道", "")
                            name = name.replace("-", "")
                            name = name.replace(" ", "")
                            name = name.replace("PLUS", "+")
                            name = name.replace("＋", "+")
                            name = name.replace("(", "")
                            name = name.replace(")", "")
                            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                            name = name.replace("CCTV1综合", "CCTV1")
                            name = name.replace("CCTV2财经", "CCTV2")
                            name = name.replace("CCTV3综艺", "CCTV3")
                            name = name.replace("CCTV4国际", "CCTV4")
                            name = name.replace("CCTV4中文国际", "CCTV4")
                            name = name.replace("CCTV4欧洲", "CCTV4")
                            name = name.replace("CCTV5体育", "CCTV5")
                            name = name.replace("CCTV6电影", "CCTV6")
                            name = name.replace("CCTV7军事", "CCTV7")
                            name = name.replace("CCTV7军农", "CCTV7")
                            name = name.replace("CCTV7农业", "CCTV7")
                            name = name.replace("CCTV7国防军事", "CCTV7")
                            name = name.replace("CCTV8电视剧", "CCTV8")
                            name = name.replace("CCTV9记录", "CCTV9")
                            name = name.replace("CCTV9纪录", "CCTV9")
                            name = name.replace("CCTV10科教", "CCTV10")
                            name = name.replace("CCTV11戏曲", "CCTV11")
                            name = name.replace("CCTV12社会与法", "CCTV12")
                            name = name.replace("CCTV13新闻", "CCTV13")
                            name = name.replace("CCTV新闻", "CCTV13")
                            name = name.replace("CCTV14少儿", "CCTV14")
                            name = name.replace("CCTV15音乐", "CCTV15")
                            name = name.replace("CCTV16奥林匹克", "CCTV16")
                            name = name.replace("CCTV17农业农村", "CCTV17")
                            name = name.replace("CCTV17农业", "CCTV17")
                            name = name.replace("CCTV5+体育赛视", "CCTV5+")
                            name = name.replace("CCTV5+体育赛事", "CCTV5+")
                            name = name.replace("CCTV5+体育", "CCTV5+")
                            results.append(f"{name},{urld}")
            except:
                continue
        except:
            continue

channels = []

for result in results:
    line = result.strip()
    if result:
        channel_name, channel_url = result.split(',')
        channels.append((channel_name, channel_url))

# 线程安全的队列，用于存储下载任务
task_queue = Queue()

# 线程安全的列表，用于存储结果
results = []

error_channels = []

# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        try:
            channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
            lines = requests.get(channel_url, timeout=1).text.strip().split('\n')  # 获取m3u8文件内容
            ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
            ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
            ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接

            # 多获取的视频数据进行5秒钟限制
            with eventlet.Timeout(5, False):
                start_time = time.time()
                content = requests.get(ts_url, timeout=1).content
                end_time = time.time()
                response_time = (end_time - start_time) * 1

            if content:
                with open(ts_lists_0, 'ab') as f:
                    f.write(content)  # 写入文件
                file_size = len(content)
                download_speed = file_size / response_time / 1024
                normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间

                # 删除下载的文件
                os.remove(ts_lists_0)
                result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                results.append(result)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
                print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
        except:
            error_channel = channel_name, channel_url
            error_channels.append(error_channel)
            numberx = (len(results) + len(error_channels)) / len(channels) * 100
            print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")

        # 标记任务完成
        task_queue.task_done()

# 创建多个工作线程
num_threads = 10
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)  # 将工作线程设置为守护线程
    t.start()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()

def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
results.sort(key=lambda x: channel_key(x[0]))

result_counter = 8  # 每个频道需要的个数

with open("lives.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('央视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('卫视频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    file.write('其他频道,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

with open("lives.m3u", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('#EXTM3U\n')
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"央视频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"卫视频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
    channel_counters = {}
    for result in results:
        channel_name, channel_url, speed = result
        if 'CCTV' not in channel_name and '卫视' not in channel_name and '测试' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                    file.write(f"{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"#EXTINF:-1 group-title=\"其他频道\",{channel_name}\n")
                file.write(f"{channel_url}\n")
                channel_counters[channel_name] = 1
