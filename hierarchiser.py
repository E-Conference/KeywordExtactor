def go():
    f = open("./clusters.csv", "r")
    res = open("./hierarchies.csv", "w")
    ret = ""
    i = 0
    total = [None] * 1000
    terms = [None] * 1000
    cluster_ids = [None] * 1000

    for l in f:
        arr = [None] * 3
        arr[0] = l.split(";")[0]
        arr[1] = l.split(";")[1].replace("\n", "")
        arr[2] = ""
        total[i] = arr
        terms[i] = arr[1]
        cluster_ids[i] = arr[0]    
        i = i + 1

    i=0
    for keyword in total:
        for term in terms:        
            if keyword[1] in term.split(" "):          
                if (keyword[1] != term) & (cluster_ids[i] == keyword[0]):
                    if keyword[1].split(" ") > term.split(" "):
                        keyword[2] = term
        ret = ret + (keyword[0] + ";" + keyword[1] + ";" + keyword[2] + "<br/>")
        res.write(keyword[0] + ";" + keyword[1] + ";" + keyword[2] + "\n")
        i = i+1

    res.close()
    return ret
                
    

