# -*-coding: utf-8 -*-

import re

def clear_html(temp_html):
	html = re.sub(r'''(<p.*?>.*?<a.*?<img.*?</p>|</?u>)''', '', temp_html)
	html = re.sub(u'''(?<=<p>)[^0-9a-zA-Z]+?(?=([\u4E00-\u9FA5]+|<))''', '', html)
	html = re.sub(u'''(?<=<strong>)[^0-9a-zA-Z]+?(?=[\u4E00-\u9FA5]+)''', '', html)
	html = re.sub(r'''<a.*?>(.*?)</a>''', '\g<1>', html)

	return html


if __name__ == "__main__":
	test_html = '''
		 <div class="detail_con">
                       <p><p align="center"><a target="_blank" href="http://image.99.com.cn/uploads/120309/58_103142_1.jpg"><img title="精液对女性健康11个好处" alt="男性精液的好处 精液对女性健康的好处 精液" border="0"  src="http://image.99.com.cn/uploads/120309/58_103142_1.jpg" /></a></p>

<p>　　<strong>奇效一：有利于消除失眠</strong></p>

<div class="hzh_botleft"><script type="text/javascript">BAIDU_CLB_fillSlot("251396");</script></div>
<p>　　所有人都渴望有个深沉、甜美的睡眠，但是各种各样的原因导致的失眠，经常困扰着大家。特别是<a href='http://nv.99.com.cn/' target='_blank'><u>女性</u></a>，更容易失眠。而当经历一次和谐的性生活后，紧张激动的身体开始放松，肌肉也在满足之后的疲倦中得以舒展，睡意自然而然地袭来，有助于消除失眠症。而且性生活越是美满，事后也越容易入睡。</p>

<p>　　<strong>奇效二：减轻<a href='http://www.99.com.cn/special/jingqiyinshi.htm' target='_blank'><u>经期</u></a>前的综合症</strong></p>

<p>　　女性在月经前的5-7天内，流入骨盆的血液增加，有可能引起肿胀和痉挛，导致腹胀或<a href='http://jbk.99.com.cn/futong/' target='_blank' class="tips" kid="297"><u>腹痛</u></a>。而性生活中的肌肉收缩运动，能促使血液加速流出骨盆区，进入血液总循环，而减轻骨盆压力，从而减轻腹部不适。</p>
<p></p>

                    </div>
	'''
	print clear_html(test_html)
