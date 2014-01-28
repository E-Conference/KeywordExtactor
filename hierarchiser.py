def go(clusters):
    ret = ""
    i = 0
    clusters_arr = clusters.split("<br/>")
    size = len(clusters_arr)
    total = [None] * size
    terms = [None] * size
    scores = [None] * size
    cluster_ids = [None] * size

    for cluster in clusters.split("<br/>"):        
            arr = [None] * 4
            cl_arr = cluster.split(";")
            arr[0] = cl_arr[0]        
            arr[1] = cl_arr[1]        
            arr[2] = ""
            arr[3] = cl_arr[2]
            total[i] = arr
            terms[i] = arr[1]
            scores[i] = arr[3]
            cluster_ids[i] = arr[0]    
            i = i + 1

    i=0
    for keyword in total:
        for term in terms:            
            if (keyword[1] in term.split(" ")) | (father(keyword[1],term,keyword[1][3],scores[i])):
                if (keyword[1] != term) & (cluster_ids[i] == keyword[0]):
                    keyword[2] = term
        ret = ret + (keyword[0] + ";" + keyword[1] + ";" + keyword[2] + ";" + scores[i] + "<br/>")        
        i = i+1
    return ret

def parent(kw1, kw2):
    for subterm1 in kw1.split(" "):
        for subterm2 in kw2.split(" "):
            if subterm1 == subterm2:
                return True
    return False

def father(kw1, kw2, score1, score2):
    if (kw1.split(" ") > kw2.split(" ")) & (parent(kw1,kw2)) & (score1>score2):
        return True
    return False              

    

