# coding:utf-8

import json
from News import mynews

news = mynews.News(8)


#print news.show_result();

for n in news.dict:
	print(json.dumps(n, ensure_ascii=False, encoding='UTF-8'))