with open("train.txt", "r", encoding='utf-8') as f:
    f = f.read().replace("作曲",'').replace("作词",'').replace("编曲",'').replace("混音",'').replace("吉他",'').replace("贝斯",'').replace("母带",'')
    f = f.split('\n')
    data = []
    for lyrics in f:
        tmp1 = lyrics.split(" ")
        le = 0
        for i in range(len(tmp1)):
            if len(tmp1[i]) > 4:
                le = i
                break
        tmp1 = tmp1[le:]
        data.append(tmp1)
    tmpp = []
    for lyrics in data:
        lyrics = ' '.join(lyrics)
        if len(lyrics) > 128:
            tmpp.append(lyrics)
    data = '\n'.join(tmpp)
    with open("train1.txt", "w", encoding='utf-8') as f:
        f.write(data)
