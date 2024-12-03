from bs4 import BeautifulSoup

class ThiVien:
    def __init__(self, document):
        self.document = document
        
    def getPoemLinks(self):
        soup = BeautifulSoup(self.document, 'html.parser')
        
        poems = []
        className = "poem-group-list"
        containers = soup.find_all(class_=className)
        
        for container in containers:
            postElements = container.find_all('a')
            for element in postElements:
                poem = {}
                poem['name'] = element.text
                poem['url'] = "https://www.thivien.net" + element.get('href')
                poems.append(poem)
        
        return poems
    
    def process(self, poemDocument, name):
        soup = BeautifulSoup(poemDocument, 'html.parser')
        element = soup.find(class_="poem-content")
        poemContainer = element.find("p")
        
        data = {}
        data[f'{name}'] = []
        
        sentence = ""
        for child in poemContainer:
            if (child.name == 'br'): 
                if (sentence != ""): data[f'{name}'].append(sentence)
                sentence = ""
            sentence += child.text
            # print(child.text)
            # print("BANANA")
        
        if (sentence != ""): data[f'{name}'].append(sentence)
        
        return data
    
    def processBigDocument(self):
        soup = BeautifulSoup(self.document, 'html.parser')
        element = soup.find(class_="poem-content")
        poemContainer = element.find("p")
        
        data = []
        
        sentence = ""
        cntParagraph = 1
        cntBr = 0
        
        sentenceData = {}
        sentenceData[f"Doan {cntParagraph}"] = []
        
        for child in poemContainer:
            if (child.name == 'b'): continue
            
            if (child.name == 'br'): 
                cntBr += 1
                if (sentence != "" and cntBr == 1): 
                    sentenceData[f"Doan {cntParagraph}"].append(sentence.lstrip())
                    
                elif (cntBr == 2):
                    if (len(sentenceData[f"Doan {cntParagraph}"]) != 0): data.append(sentenceData)
                    cntParagraph += 1
                    cntBr = 0
                    
                    sentenceData = {}
                    sentenceData[f"Doan {cntParagraph}"] = []
                    
                sentence = ""
                
            else: cntBr = 0
            sentence += child.text
        
        if (len(sentenceData[f"Doan {cntParagraph}"]) != 0): data.append(sentenceData)
        return data
    
class Wiki:
    def __init__(self, document):
        self.document = document
        
    def getPoemLinks(self):
        soup = BeautifulSoup(self.document, 'html.parser')
        container = soup.find(id="mw-content-text")
        
        listElements = container.find_all('ul')
        if (len(listElements) == 0): return []
        
        elements = listElements[len(listElements) - 1].find_all('li')
        
        # print(elements)
        poems = []
        for element in elements:
            # print(element)
            linkElement = element.find('a')
            poem = {}
            poem['name'] = element.text
            poem['url'] = "https://vi.wikisource.org" + linkElement.get('href')
            poems.append(poem)
        
        return poems

    def process(self, poemDocument, name):
        soup = BeautifulSoup(poemDocument, 'html.parser')
        
        lucbat = soup.find_all(class_ = "ws-lucbat-kho")
        # print(lucbat)
        data = {}
        data[f'{name}'] = []
        
        if (len(lucbat) != 0):
            sentence = ""
            for kho in lucbat:
                # print(kho)
                for child in kho:
                    # print(child.name)
                    
                    sentence = ''.join([text for text in child.strings if text.parent == child])
                    sentence.lstrip('\n').rstrip('\n')
                    if (sentence != None and sentence != ""): data[f'{name}'].append(sentence.lstrip('\n').rstrip('\n'))
                    # print(sentence)
                    # print(child.text)
                    # print("BANANA")
        else:
            elements = soup.find_all(class_="poem")
            poemContainer = elements[len(elements) - 1].find("p")
            
            sentence = ""
            for child in poemContainer:
                if(child.name == 'span'): continue
                if (child.name == 'br'): 
                    if (sentence != ""): data[f'{name}'].append(sentence.lstrip('\n').rstrip('\n'))
                    sentence = ""
                sentence += child.text
                # print(child.text)
                # print("BANANA")
            
            if (sentence != ""): data[f'{name}'].append(sentence.lstrip('\n').rstrip('\n'))
        
        if (len(data[f'{name}']) == 0): return {}
        return data
    
            