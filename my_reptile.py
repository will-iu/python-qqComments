import requests
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}


def get_comments(music_name):
    # 存储评论
    result = []
    list_comment = []
    # 第一次爬取，通过歌曲名获得歌曲id
    url1 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    params1 = {
        'ct': '24',
        'qqmusic_ver': '1298',
        'new_json': '1',
        'remoteplace': 'sizer.yqq.song_next',
        'searchid': '64405487069162918',
        't': '0',
        'aggr': '1',
        'cr': '1',
        'catZhida': '1',
        'lossless': '0',
        'flag_qc': '0',
        'p': '1',
        'n': '20',
        'w': music_name,
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0'
    }
    res_music = requests.get(url1, headers=headers, params=params1)
    json_music = res_music.json()
    list_music = json_music['data']['song']['list']
    music_id = list_music[0]['id']

    # 第二次爬取，通过歌曲id获得歌曲热评列表
    url2 = 'https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg'
    params2 = {
        'g_tk_new_20200303': '5381',
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'GB2312',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
        'cid': '205360772',
        'reqtype': '2',
        'biztype': '1',
        'topid': music_id,
        'cmd': '8',
        'needcommentcrit': '0',
        'pagenum': '0',
        'pagesize': '25',
        'lasthotcommentid': '',
        'domain': 'qq.com',
        'ct': '24',
        'cv': '10101010'
    }
    res_comment = requests.get(url2, headers=headers, params=params2)
    json_comment = res_comment.json()
    list_comment = json_comment['hot_comment']['commentlist']
    for comment in list_comment:
        result.append(re.sub(r'\[em\].*?\[\/em\]', '',
                             comment['rootcommentcontent']))
    return result
