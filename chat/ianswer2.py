# -*- coding:utf8 -*-
import os
import json
from .mytools import get_timestamp

thispath = os.path.split(os.path.realpath(__file__))[0]
with open(thispath + '/data/answer2.xml', 'r', encoding="UTF-8") as file:
    answer = file.read()

item = '''<item><Title><![CDATA[]]></Title><Description><![CDATA[]]></Description><PicUrl><![CDATA[{img_url}]]></PicUrl><Url><![CDATA[]]></Url></item>'''

def answer2xml(data):
    imgs = ''
    img_urls = []
    items = ''
    result = {
        # ===========================原接口==============================
        "question": data['question'],
        "content": data['content'],
        "context": data['context'],
        "url": data['url'],
        "behavior": data['behavior'],
        "parameter": data['parameter'],
        # ===========================新扩展==============================
        "picurl": ""
    }
    # 对于无按钮图片的场景节点和问答节点，"picurl" 直接返回 "" 而不是格式化为 xml.
    # Modify：2018-1-8
    if data['button'] == '' and data['img'] == '':
        return result

    if data['img'] != '':
        img = json.loads(data['img'])
        img_urls = [item['iurl'] for item in img.values()]
        img_names = [item['content'] for item in img.values()]
        if img_names:
            imgs = '|'.join(img_names)
        if len(img_urls) > 1:
            xml_items = [item.format(img_url=url) for url in img_urls[1:]]
            items = '\n'.join(xml_items)
    
    result['picurl'] = answer.format(
        timestamp=str(get_timestamp()),
        news='news',
        article_count=str(len(img_urls)),
        content=data['content'],
        context=data['context'],
        button=data['button'],
        imgs=imgs,
        img_url=img_urls[0] if img_urls else '',
        items=items
    )
    result['content'] = "" # Modify：场景中要说的话放到 picurl 中。(2018-1-8)
    return result
