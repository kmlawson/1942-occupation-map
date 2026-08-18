#!/usr/bin/env python3
"""Add period-name fields to settlements.geojson.

The source layer carries only name_zh (a mix of simplified and traditional
forms) and name_en (pinyin); name_alt is empty. This script adds:

  name_zh_period  the characters the place went by around 1942
  name_alt        the romanised name in general use at the time

Several places were renamed between 1942 and now, and two were renamed by the
occupation itself — 歸綏 became 厚和豪特市 under Mengjiang in 1937, and 石家莊
became 石門市 — so the period characters are listed explicitly rather than
derived. Where they are unchanged, the traditional form of name_zh is used,
converted straight off the source string — never round-tripped, which would
corrupt the entries that are already traditional (安陽, 開封, 洛陽).

Prefectural names abolished in 1913 (順德府, 東昌府, 沂州府) are deliberately not
used: by 1942 those places went by their county names. The one exception is
彰德 for Anyang, which stayed in general use and appears on Japanese maps of
the period. Two counties are left under their better-known city names for the
same reason: 鄭州 was officially 鄭縣 from 1913 to 1948, and 徐州 was 銅山縣,
but contemporary Japanese usage was 鄭州 and 徐州.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONV = json.load(open(os.path.expanduser(
    '~/.claude/skills/trad-simp-toggle/assets/convtable.json')))
S2T = dict(zip(CONV['sk'], CONV['sv']))

def to_trad(s):
    return ''.join(S2T.get(c, c) for c in s or '')

# name_en -> (characters in use c.1942, or None to use the traditional form;
#             romanised name in general use c.1942, or None if it matches pinyin)
PERIOD = {
    'Beijing':       (None,    'Peking'),
    'Tianjin':       (None,    'Tientsin'),
    'Zhangjiakou':   (None,    'Kalgan'),
    'Baotou':        (None,    'Paotow'),
    'Hohhot':        ('厚和豪特', 'Kweisui'),
    'Datong':        (None,    'Tatung'),
    'Taiyuan':       (None,    None),
    'Jiexiu':        (None,    'Kiehsiu'),
    'Shijiazhuang':  ('石門',   'Shihmen'),
    'Xingtai':       (None,    'Hsingtai'),
    'Anyang':        ('彰德',   'Changteh'),
    'Kaifeng':       (None,    None),
    'Zhengzhou':     (None,    'Chengchow'),
    'Luoyang':       (None,    'Loyang'),
    'Xuzhou':        (None,    'Suchow'),
    'Jinan':         (None,    'Tsinan'),
    'Qingdao':       (None,    'Tsingtao'),
    'Yantai':        (None,    'Chefoo'),
    'Weihai':        ('威海衛', 'Weihaiwei'),
    'Weifang':       ('濰縣',   'Weixian'),
    'Jining':        (None,    'Tsining'),
    'Linqing':       (None,    'Lintsing'),
    'Liaocheng':     (None,    None),
    'Dezhou':        ('德縣',   'Dexian'),
    'Linyi':         (None,    None),
    'Rizhao':        (None,    'Jihchao'),
    'Laiwu':         (None,    None),
    'Yishui County': (None,    None),
}
# Renamings worth spelling out for students, shown in the popup.
NOTE = {
    'Hohhot':       'capital of Mengjiang. 歸綏 Kweisui until the Mengjiang regime '
                    'renamed it 厚和豪特市 in October 1937; it reverted to 歸綏 in 1945 '
                    'and became 呼和浩特 in 1954',
    'Shijiazhuang': 'merged with 休門 and renamed 石門市 (Shihmen) under the Japanese '
                    'occupation; it became 石家莊市 in 1947',
    'Weifang':      'the city of 濰坊 Weifang dates only from 1948; in 1942 this was 濰縣 Weixian',
    'Dezhou':       'known as 德縣 Dexian at the time',
    'Anyang':       'the county was 安陽縣, but the place was generally known, and '
                    'labelled on Japanese maps, by the old prefectural name 彰德 Changteh',
    'Beijing':      '北平 Peiping under the Nationalists; renamed 北京 by the occupation regime',
    'Weihai':       'the British leased territory of 威海衛 Weihaiwei until 1930, then a Chinese special district',
}

path = os.path.join(ROOT, 'data', 'settlements.geojson')
gj = json.load(open(path))
for f in gj['features']:
    p = f['properties']
    en = p.get('name_en') or ''
    hanzi, alt = PERIOD.get(en, (None, None))
    p['name_zh_period'] = hanzi or to_trad(p.get('name_zh'))
    p['name_alt'] = alt
    p['note'] = NOTE.get(en)
    p.pop('name_zh_trad', None)
json.dump(gj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))

for f in gj['features']:
    p = f['properties']
    star = ' *' if p['name_zh_period'] != to_trad(p['name_zh']) else ''
    print(f"{p['name_en']:15} {p['name_zh_period']:6} {p['name_alt'] or '-':10}{star}")
