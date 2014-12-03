# coding=utf-8
import chardet
import re
import urllib2

from lxml import etree


__author__ = 'garfield'


def tmall_item(link, ):
    rule = {
        'title': r'<title>(.*)</title>',
        'detail_link': r'(http://mdskip\.taobao\.com/core/initItemDetail.*?)(\')',
        'img': 'src',
        'price': r'(?:orderAmountRestriction[\D]*price\W*|extraPromPrice[\W]*)(\d*\.\d*)',
        'defaultprice': r'(?:defaultItemPrice[\D]*)(\d*\.?\d*)',
        }
    return parser(link, rule)


def taobao_item(link):
    rule = {
        'title': r'<title>(.*)</title>',
        'detail_link': r'(http://detailskip\.taobao\.com/json/sib\.htm.*?)(?:\")',
        'img': 'data-src',
        'price': r'(?:price\W*)(\d*\.\d*)',
        'defaultprice': r'(?:price\W*)(\d*\.\d*)',
    }
    return parser(link, rule)


def parser(link, rule):
    try:
        response = urllib2.urlopen(link, timeout=7)
        html = response.read()
        title_group = re.search(rule['title'], html)
        title = title_group.group(1)
        charset = chardet.detect(title)
        title = title_group.group(1).decode(charset['encoding']).encode('utf-8')
        detail_link = re.search(rule['detail_link'], html)
        page = etree.HTML(html)
        hrefs = page.xpath(u'//ul[@id="J_UlThumb"]//img')
        img = []
        for href in hrefs:
            temp = href.get(rule['img'])
            path = re.search(r'(.*?\.jpg)', str(temp))
            img.append(path.group(1))
        js_link = detail_link.group(1)
        new_request = urllib2.Request(js_link)
        new_request.add_header('Referer', link)
        detail = urllib2.urlopen(new_request, timeout=7)
        detail_content = detail.read()
        dis_price_group = re.search(rule['price'], detail_content)
        default_price_group = re.search(rule['defaultprice'], html)
        if dis_price_group and dis_price_group.group(1):
            price = dis_price_group.group(1)
        else:
            price = default_price_group.group(1)
        result = {
            'title': title,
            'img': img,
            'price': price,
        }
        return result
    except:
        return None