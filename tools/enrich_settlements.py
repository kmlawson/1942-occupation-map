#!/usr/bin/env python3
"""Add traditional-hanzi and period-name fields to settlements.geojson.

name_zh in the source layer is a mix of simplified and already-traditional
forms, so conversion goes straight from the source string (never S->T->S).
name_alt is empty in the source, so period names (Chinese Postal Map
romanisation / the name the place went by c.1942) are filled in here.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONV = json.load(open(os.path.expanduser(
    '~/.claude/skills/trad-simp-toggle/assets/convtable.json')))
S2T = dict(zip(CONV['sk'], CONV['sv']))

def to_trad(s):
    return ''.join(S2T.get(c, c) for c in s or '')

# Name in general English use on maps and in the press c.1942.
# Left blank where the period form is effectively identical to the pinyin.
PERIOD = {
    'Beijing':      'Peking',
    'Tianjin':      'Tientsin',
    'Zhangjiakou':  'Kalgan',
    'Baotou':       'Paotow',
    'Hohhot':       'Kweisui',
    'Datong':       'Tatung',
    'Taiyuan':      'Taiyuan',
    'Jiexiu':       'Kiehsiu',
    'Shijiazhuang': 'Shihmen',
    'Xingtai':      'Shuntehfu',
    'Anyang':       'Changteh',
    'Kaifeng':      'Kaifeng',
    'Zhengzhou':    'Chengchow',
    'Luoyang':      'Loyang',
    'Xuzhou':       'Suchow',
    'Jinan':        'Tsinan',
    'Qingdao':      'Tsingtao',
    'Yantai':       'Chefoo',
    'Weihai':       'Weihaiwei',
    'Weifang':      'Weixian',
    'Jining':       'Tsining',
    'Linqing':      'Lintsing',
    'Liaocheng':    'Tungchang',
    'Dezhou':       'Dexian',
    'Linyi':        'Yichow',
    'Rizhao':       'Jihchao',
    'Laiwu':        'Laiwu',
    'Yishui County':'Yishui',
}
# Places renamed outright under the occupation, worth spelling out for students.
NOTE = {
    'Weifang':      'the city of 濰坊 Weifang dates from 1948; in 1942 this was 濰縣 Weixian',
    'Dezhou':       'known as 德縣 Dexian at the time',
    'Shijiazhuang': 'renamed 石門市 (Shihmen) in 1941 under Japanese occupation',
    'Hohhot':       'capital of Mengjiang; 歸綏 Kweisui at the time',
    'Beijing':      '北平 Peiping under the Nationalists; renamed 北京 by the occupation regime',
    'Xingtai':      'the old prefectural name 順德府 Shuntehfu was still in common use',
    'Anyang':       'the old prefectural name 彰德 Changteh was still in common use',
}

path = os.path.join(ROOT, 'data', 'settlements.geojson')
gj = json.load(open(path))
for f in gj['features']:
    p = f['properties']
    en = p.get('name_en') or ''
    p['name_zh_trad'] = to_trad(p.get('name_zh'))
    # PERIOD wins, so re-running the script picks up edits to the table above.
    p['name_alt'] = PERIOD.get(en) or p.get('name_alt') or None
    p['note'] = NOTE.get(en)
json.dump(gj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))
for f in gj['features']:
    p = f['properties']
    print(f"{p['name_en']:15} {p['name_alt'] or '-':12} {p['name_zh']} -> {p['name_zh_trad']}")
