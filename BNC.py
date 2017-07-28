from random import*
from math import*
from copy import*

class text_data:
    alpha = set("qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю")
    num = set("1234567890")
    synt = set("~`!?.,:-();'" + '"')
    ends = {"а", "я", "о", "е", "ь", "ы", "и", "а", "ое", "ой", "ей", "ее", "ий", "у", "ю", "ою", "ею", "ею", "ом", "ем", "ью", "ами", "ями", "ах", "ях",
            "ой", "его", "ему", "ому", "им", "ем", "ого", "ому", "ую", "ею", "ом", "ие", "их", "ими", "яя", "юю", "их", "им", "ое", "ешь", "ишь", "л", "лю", "ла", "ло", "ли", "ет", "ит", "ете", "ите", "ут", "ют", "ат", "ят", "ая", "ый", "ые", "ое", "s"}
    
    def normalize_char(self, a):
        if 'A' <= a <= 'Z':
            return chr(ord(a) + ord('a') - ord('A'))
        if 'А' <= a <= 'Я':
            return chr(ord(a) + ord('а') - ord('А')) 
        return a
    
    def normalize_word(self, a):
        a = list(a)
        for i in range(len(a)):
            a[i] = self.normalize_char(a[i])
        mx = 0
        for el in self.ends:
            if (el == "".join(a[-len(el):])):
                mx = max(mx, len(el))
        a = a[:-mx]
        return "".join(a)
    
    def normalize_text(self, txt):
        text = []
        curr = ""
        for el in txt:
            z = self.normalize_char(el)
            if z in self.alpha:
                curr = curr + z
            else:
                if len(curr) < 2:
                    curr = ""
                    continue
                curr = self.normalize_word(curr)
                if len(curr) < 2:
                    curr = ""
                    continue
                text.append(curr)
                curr = ""
        return text    
    
    def __init__(self, arr):
        self.text = self.normalize_text("".join(arr))

class NBC: # Naive Bayes Classifier
    c = 0.05 # !!!!!!! MAGIC !!!!!
    def __init__(self, data, c1, c2):
        self.c1 = c1
        self.c2 = c2
        self.classes = dict()
        self.words = dict()
        self.n = len(data)
        for sample in data: 
            ans = sample[1]
            if ans not in self.classes:
                self.classes[ans] = [1, dict()]
            else:
                self.classes[ans][0] += 1
            for word in sample[0]:
                if word not in self.words:
                    self.words[word] = 1
                else:
                    self.words[word] += 1
                if (word not in self.classes[ans][1]):
                    self.classes[ans][1][word] = 1
                else:
                    self.classes[ans][1][word] += 1     
        words = deepcopy(self.words)
        classes2 = deepcopy(self.classes)
        for writer in self.classes:
            for word in self.classes[writer][1]:
                log = True
                mx = -1
                mn = 10000000000
                for writer2 in self.classes:
                    if word not in self.classes[writer2][1] or self.classes[writer2][1][word] < 80: #100
                        log = False
                        break
                    else:
                        mx = max(mx, self.classes[writer2][1][word])
                        mn = min(mn, self.classes[writer2][1][word])
                if log or (abs(mx - mn) <= 10):
                    for writer2 in self.classes:
                        if word not in classes2[writer2][1]:
                            continue
                        if word in self.words:
                            self.words[word] -=  self.classes[writer2][1][word]
                        classes2[writer2][1].pop(word)
                    continue
                if self.classes[writer][1][word] <= self.c2:
                    classes2[writer][1].pop(word)
                    if word in self.words:
                        self.words[word] -=  self.classes[writer][1][word]

        self.classes = deepcopy(classes2)            
        for word in words:
            if words[word] == 0:
                self.words.pop(word)
        self.thrust = dict()
        for key in self.classes:
            self.thrust[key] = 1
        self.thrust["А. С. Пушкин"] = self.c1
                   
    def ask(self, text):
        mx = 0
        mx_id = "Void"
        for z in self.classes:
            el = [z, self.classes[z]]
            p = log1p(el[1][0] / self.n)
            pr = 0
            for word1 in el[1][1]:
                word = [word1, el[1][1][word1]]
                pr += word[1] + self.c
            for word in text:
                z = el[1][1][word] if word in el[1][1] else 0
                p += log1p((z + self.c) / pr)
            z = el[0]
            p *= self.thrust[z]
            if p > mx:
                mx = p
                mx_id = el[0]
        return mx_id
    
    
cnt_all = dict()
cnt_wrong = dict()
fin1 = open("Pushkin.txt", encoding = "utf-8")
fin2 = open("Lermontov.txt", encoding = "utf-8")
samples = []
curr = []
for el in fin1.readlines():
    el = el.rstrip()
    flag1 = True
    flag2 = False
    for char in el:
        if 'A' <= char <= 'Z' or 'А' <= char <= 'Я':
            flag2 = True 
        if 'a' <= char <= 'z' or 'а' <= char <= 'я':
            flag1 = False
    if flag1 and flag2:
        curr = text_data(" ".join(curr))
        if curr.text != []:
            samples.append([curr.text, "А. С. Пушкин"])
        curr = []
    else:
        curr.append(el)
        
for el in fin2.readlines():
    el = el.rstrip()
    flag1 = True
    flag2 = False
    for char in el:
        if 'A' <= char <= 'Z' or 'А' <= char <= 'Я':
            flag2 = True 
        if 'a' <= char <= 'z' or 'а' <= char <= 'я':
            flag1 = False
    if flag1 and flag2:
        curr = text_data(" ".join(curr))
        if curr.text != []:
            samples.append([curr.text, "М. Ю. Лермонтов"])
        curr = []
    else:
        curr.append(el)    
fin1.close()
fin2.close()    
#Parsing compleated

mn = 100000000000000
mn_id = 0
for over in range(5000):
    study = []
    work = []
    for el in samples:
        if (randint(0, 4)): 
            study.append(el)
        else:
            work.append(el)
    AI = NBC(study, 1.02, 20)
    for el in work: #23
        z = AI.ask(el[0])
        if el[1] not in cnt_all:
            cnt_all[el[1]] = 1
            cnt_wrong[el[1]] = 0
        else:
            cnt_all[el[1]] += 1
        if el[1] != z:
            cnt_wrong[el[1]] += 1
for el in cnt_wrong:
    print(el, round(cnt_wrong[el] / cnt_all[el] * 100, 2), "% errors from", cnt_all[el])