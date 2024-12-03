from utils import fetchDocument
from classes import ThiVien, Wiki
import time

import random
import json
import os

from bs4 import BeautifulSoup

def crawlThiVien(url, name):
    document = fetchDocument(url, "document1")
    crawler = ThiVien(document)
    poems = crawler.getPoemLinks()
    
    if not os.path.exists(f'data'):
        os.makedirs(f'data')
        
    # print(poems)
    if (len(poems) == 0):
        data = crawler.processBigDocument()
    else:
        data = []
        
        cnt = 0
        for poem in poems:
            smallDoc = fetchDocument(poem['url'], 'document2')
            print(poem['url'])
            data.append(crawler.process(smallDoc, poem['name']))
            
            time.sleep(5)
    
    # print(data)
    json_poem = json.dumps(data, indent=4)
    with open(f"data/{name}.json", "w") as file:
        file.write(json_poem)
        
def crawlWiki(url, name):
    document = fetchDocument(url, "document1")
    crawler = Wiki(document)
    poems = crawler.getPoemLinks()
    
    if not os.path.exists(f'data'):
        os.makedirs(f'data')
        
    # print(poems)
    
    data = []
    for poem in poems:
        smallDoc = fetchDocument(poem['url'], 'document2')
        print(poem['url'])
        dict = crawler.process(smallDoc, poem['name'])
        if (len(dict) != 0): data.append(dict)
    
    if (len(data) == 0):
        data.append(crawler.process(crawler.document, name))
        
    json_poem = json.dumps(data, indent=4)
    with open(f"data/{name}.json", "w") as file:
        file.write(json_poem)

def crawlPhuDay(url, name):
    document = fetchDocument(url, "document1")
    soup = BeautifulSoup(document, 'html.parser')
    
    if not os.path.exists(f'data'):
        os.makedirs(f'data')
        
    # print(poems)
    
    classes = {'x11i5rnm', 'xat24cr', 'x1mh8g0r', 'x1vvkbs', 'xtlvy1s', 'x126k92a'}
    elements = soup.find_all(lambda tag: tag.has_attr('class') and classes.issubset(tag['class']))
    
    data = []
    
    parity = 0
    title = ""
    paragraph = {}
    for element in elements:
        if (parity == 0): 
            title = (element.text).lstrip('\n').rstrip('\n').lstrip(' ').rstrip(' ')
            paragraph[f"{title}"] = []
            
        else:
            for child in element:
                text = (child.text).lstrip('\n').rstrip('\n').lstrip(' ').rstrip(' ')
                if (text != ""): paragraph[f"{title}"].append(text)
            
            data.append(paragraph)
            paragraph = {}
        
        parity ^= 1
        
    data.pop(0)
    json_poem = json.dumps(data, indent=4)
    with open(f"data/{name}.json", "w") as file:
        file.write(json_poem)
    
def crawlChuNom(url, name):
    document = fetchDocument(url, "document1")
    soup = BeautifulSoup(document, 'html.parser')
    
    if not os.path.exists(f'data'):
        os.makedirs(f'data')
        
    # print(poems)
    
    classes = {'textline'}
    elements = soup.find_all(class_ = classes)
    
    data = []
    poem = {}
    poem['BuomHoaTanTruyen'] = []
    for element in elements:
        textElement = element.find('div')
        texts = textElement.find_all('div')
        
        sentence = ' '.join([child.text for child in texts[-1]])
        sentence = sentence.lstrip('\n').rstrip('\n')
        sentence = ' '.join(sentence.split())
        poem['BuomHoaTanTruyen'].append(sentence)
        
    data.append(poem)
    json_poem = json.dumps(data, indent=4)
    with open(f"data/{name}.json", "w") as file:
        file.write(json_poem)
    
    
mainPoems = [
    {
        'name': "BachVanQuocNguThiTap",
        'url': "https://www.thivien.net/Nguy%e1%bb%85n-B%e1%bb%89nh-Khi%c3%aam/B%e1%ba%a1ch-V%c3%a2n-qu%e1%bb%91c-ng%e1%bb%af-thi-t%e1%ba%adp/group-LDyeyyK346olez8YrQLETw"
    },
    
    {
        'name': "CungOanNgamKhuc",
        'url': "https://www.thivien.net/Nguy%e1%bb%85n-Gia-Thi%e1%bb%81u/Cung-o%c3%a1n-ng%c3%a2m-kh%c3%bac/poem-_hflrw-MrPlLEBFOl7MVPA"
    },
    
    {
        'name': "CungOanThi",
        'url': "https://www.thivien.net/Nguy%E1%BB%85n-Huy-L%C6%B0%E1%BB%A3ng/Cung-o%C3%A1n-thi-100-b%C3%A0i/group-zGcRuu0y-a0QRhHMxX_8zg"
    },
    
    {
        'name': "ThuDaLuHoaiNgamKhuc",
        'url': "https://www.thivien.net/%C4%90inh-Nh%E1%BA%ADt-Th%E1%BA%ADn/Thu-d%E1%BA%A1-l%E1%BB%AF-ho%C3%A0i-ng%C3%A2m/poem-QwHBlDHxHjNmmwiMhPsXpg"
    },
    
    {
        'name': "MaiDinhMongKy",
        'url': "https://www.thivien.net/Nguy%E1%BB%85n-Huy-H%E1%BB%95/Mai-%C4%90%C3%ACnh-m%E1%BB%99ng-k%C3%BD/poem-yr4jF9Y1Dea-3fy-zhdaug"
    }
    ]

# crawlThiVien("https://www.thivien.net/Nguy%E1%BB%85n-Huy-H%E1%BB%95/Mai-%C4%90%C3%ACnh-m%E1%BB%99ng-k%C3%BD/poem-yr4jF9Y1Dea-3fy-zhdaug", "MaiDinhMongKy")
    
# for poem in mainPoems:
#     crawlThiVien(poem['url'], poem['name'])

# crawlWiki("https://vi.wikisource.org/wiki/Trinh_th%E1%BB%AD", "TrinhThu")
# crawlPhuDay("https://phuday.com/tien-pha-dich-luc.html", "TienPhaDichLuc")
crawlChuNom("https://chunom.org/shelf/corpus/2/", "BuomHoaTanTruyen")
    
# "https://vi.wikisource.org/wiki/H%E1%BA%A1nh_Th%E1%BB%A5c_ca", "HanhThucCa"
# "https://vi.wikisource.org/wiki/Trinh_th%E1%BB%AD", "TrinhThu"
# "https://vi.wikisource.org/wiki/Nh%E1%BB%8B_%C4%91%E1%BB%99_mai", "NhiDoMai"

    


