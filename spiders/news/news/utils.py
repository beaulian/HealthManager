# -*-coding: utf-8 -*-

import re

def clear_html(temp_html):
	html = re.sub(r'''(<p.*?>.*?<a.*?<img.*?</p>|</?u>)''', '', temp_html)
	html = re.sub(u'''(?<=<p>)[^0-9a-zA-Z]+?(?=([\u4E00-\u9FA5]+|<))''', '', html)
	html = re.sub(u'''(?<=<strong>)[^0-9a-zA-Z]+?(?=[\u4E00-\u9FA5]+)''', '', html)
	html = re.sub(r'''<a.*?>(.*?)</a>''', '\g<1>', html)
	try:
		return html.split('''<div class="hzh_botleft">''')[0]
	except IndexError:
		return html