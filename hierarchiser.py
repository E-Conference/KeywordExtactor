from stemming.porter2 import stem

def go(keywords):
    ret = list()

    for keyword1 in keywords:        
        for keyword2 in keywords:            
            if father(keyword1,keyword2):                     
                keyword1.assignFather(keyword2)                    
        ret.append(keyword1)
    return ret

def parent(kw1, kw2):
    for subterm1 in kw1.keyword.split(" "):
        for subterm2 in kw2.keyword.split(" "):
            if stem(subterm1) == stem(subterm2):
                return True
    return False

def father(kw1, kw2):    
    if ((len(kw1.keyword.split(" ")) > len(kw2.keyword.split(" "))) | (len(kw1.keyword) >= len(kw2.keyword)))  & (parent(kw1,kw2)) & (kw1.score>kw2.score) & (kw1.cluster == kw2.cluster):
        return True
    return False              

    

