# -*- coding:utf8 -*-
import os
import json
from mytools import get_timestamp

xmlpath = os.path.split(os.path.realpath(__file__))[0]
with open(xmlpath + './answer.xml', 'r', encoding="UTF-8") as file:
    answer = file.read()

item = '''		<item>
			<Title><![CDATA[]]>
			</Title>
			<Description>
				<![CDATA[]]>
			</Description>
			<PicUrl>
				<![CDATA[{img_url}]]>
			</PicUrl>
			<Url>
				<![CDATA[]]>
			</Url>
		</item>	'''

def answer2xml(data):
    previous = '0'
    next = '0'
    buttons = ''
    imgs = ''
    img_urls = []
    items = ''
    result = {
        # ===========================原接口==============================
        'question': data['question'],
        'content': data['content'],
        'context': data['context'],
        'url': data['url'],
        'behavior': data['behavior'],
        'parameter': data['parameter'],
        # ===========================新扩展==============================
        'picurl': ''
    }
    if data['button'] != '':
        button = json.loads(data['button'])
        button_names = [item['content'] for item in button['area'].values()]
        button_tids = [item['url'] for item in button['area'].values()]
        if button_names:
            buttons = ('|'.join(button_names) + '|')
        if button['previous']:
            previous = button['previous']['content']
        if button['next']:
            next = button['next']['content']
    if data['img'] != '':
        img = json.loads(data['img'])
        img_urls = [item['iurl'] for item in img.values()]
        img_names = [item['content'] for item in img.values()]
        img_tids = [item['url'] for item in img.values()]
        if img_names:
            imgs = '|'.join(img_names)
        if len(img_urls) > 1:
            xml_items = [item.format(img_url=url) for url in img_urls[1:]]
            items = '\n'.join(xml_items)
    pic_xml = answer.format(
        timestamp=str(get_timestamp()),
        news='news',
        article_count=str(len(img_urls)),
        content=data['content'],
        context=data['context'],
        previous=previous,
        buttons=buttons,
        next=next,
        imgs=imgs,
        img_url=img_urls[0] if img_urls else '',
        items=items
    )
    result['picurl'] = pic_xml
    return result
    # return pic_xml
    # return json.dumps(result)
    
if __name__ == '__main__':
    data = {
        'question': "看看理财产品", # 用户问题
        'content': "我行的各种理财产品请参考下图，您可以点击图标查看详情，也可以语音或手动选择购买。",
        'context': "理财产品",
        'url': "",
        'behavior': 4098, # 0x1002
        'parameter': "{'id': 1, 'level': 3, 'pos': 0.5}",
        'name': "理财产品", # 标准问题
        'tid': "0",
        'txt': "",
        'img': '{"area_1": {"pos": 1, "content": "乾元共享型理财产品", "iurl": "img/1.jpg", "url": "1"}, "area_2": {"pos": 2, "content": "乾元周周利开放式保本理财产品", "iurl": "img/2.jpg", "url": "2"}, "area_3": {"pos": 3, "content": "乾元私享型理财产品", "iurl": "img/3.jpg", "url": "3"}, "area_4": {"pos": 4, "content": "乾元满溢120天开放式理财产品", "iurl": "img/4.jpg", "url": "4"}}',
        'button': '{"previous": {"pos": 0, "content": "理财产品", "url": "0"}, "next": {"pos": 4, "content": "乾元共享型理财产品", "url": "1"},"area": {"area_1": {"pos": 1, "content": "手机银行办理", "url": "5"}, "area_2": {"pos": 2, "content": "呼叫大堂经理", "url": "6"}, "area_3": {"pos": 3, "content": "理财产品取号", "url": "7"}}}',
        'valid': 1 # valid=0 代表 error_page
    }
    print(answer2xml(data))
 