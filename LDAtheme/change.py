with open("rap.txt","r",encoding='utf-8') as f:
    f = f.read()
    f = f.replace ("作词","").replace("作曲","")
    with open("train.txt","w",encoding='utf-8') as t:
        t.write(f)
        