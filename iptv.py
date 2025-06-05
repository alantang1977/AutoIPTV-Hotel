import concurrent.futures
import requests
from bs4 import BeautifulSoup


# 定义 URL 列表
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

# 获取 URL 内容
def get_url_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to get content from {url}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error getting content from {url}: {e}")
        return None

# 提取直播源 URL
def extract_live_urls(content):
    live_urls = []
    if content:
        soup = BeautifulSoup(content, 'html.parser')
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and 'http' in href:
                live_urls.append(href)
    return live_urls

# 修改 URL（目前只是简单返回原 URL，可按需修改）
def modify_urls(url):
    return [url]

# 获取所有 URL 的内容并提取直播源
all_live_urls = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    contents = executor.map(get_url_content, urls)
    for content in contents:
        live_urls = extract_live_urls(content)
        all_live_urls.extend(live_urls)

# 处理所有直播源 URL
all_modified_urls = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(modify_urls, all_live_urls)
    for modified_urls in results:
        all_modified_urls.extend(modified_urls)

# 生成 M3U 文件
with open('live_list.m3u', 'w', encoding='utf-8') as m3u_file:
    m3u_file.write('#EXTM3U\n')
    for index, url in enumerate(all_modified_urls):
        m3u_file.write(f'#EXTINF:-1,Channel {index + 1}\n')
        m3u_file.write(url + '\n')

# 生成 TXT 文件
with open('live_list.txt', 'w', encoding='utf-8') as txt_file:
    for url in all_modified_urls:
        txt_file.write(url + '\n')
