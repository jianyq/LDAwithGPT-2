from tqdm import tqdm
import requests
import random
import json
import time
import re
pattern = re.compile(r'[\u4e00-\u9fa5]+')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}
def get_song_data(item):
    song_id = item['song_id']
    song_title = item['title']
    url = 'http://music.163.com/api/song/lyric?lv=-1&id={}'.format(song_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        doc = json.loads(response.text)
    else:
        print(url, 'failed!')
    lrc = doc.get('lrc', None)
    if lrc:
        lyric = lrc.get('lyric', None)
        lyric = lyric.replace(' ','')
        lyric = pattern.findall(lyric)
        lyric = ' '.join(lyric)
        if len(lyric) < 100:
            return None
        else:
            lyric += (',' + song_title)
            return lyric
    else:
        return None
if __name__ == "__main__":
    with open('data\\detail_list.json', 'r', encoding='utf-8') as f:
        detail_list = json.load(f)
    dataset = []
    for detail_data in tqdm(detail_list[:-1]):
        text = get_song_data(detail_data)
        if text:
            dataset.append(text)
    dataset = '\n'.join(dataset)
    with open('data\\rap.txt', 'w', encoding='utf-8') as f:
        f.write(dataset)
    print("finish")

            
