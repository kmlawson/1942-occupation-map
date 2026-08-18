#!/usr/bin/env python3
"""Add period-name fields to settlements.geojson.

The source layer carries only name_zh (a mix of simplified and traditional
forms) and name_en (modern pinyin); name_alt is empty. Every name shown on
the map should be the one the place went by in September 1942, so this
script adds all three parts of the label:

  name_en_period  pinyin of the name in use at the time
  name_zh_period  the characters in use at the time
  name_alt        the romanised form in general Western use at the time

Six places were called something else in 1942, two of them because the
occupation itself renamed them:

  厚和豪特 Houhehaote  Mengjiang renamed 歸綏 in October 1937 (now 呼和浩特)
  石門     Shimen      石家莊 merged with 休門 under the occupation
  彰德     Zhangde     the old prefectural name, still in general use (now 安陽)
  德縣     Dexian      now 德州
  濰縣     Weixian     now 濰坊; the city of Weifang dates only from 1948
  威海衛   Weihaiwei   now 威海

Where the characters are unchanged, the traditional form of name_zh is used,
converted straight off the source string — never round-tripped, which would
corrupt the entries that are already traditional (安陽, 開封, 洛陽).

Prefectural names abolished in 1913 (順德府, 東昌府, 沂州府) are deliberately
not used: by 1942 those places went by their county names. 彰德 is the
exception, as it stayed in general use and appears on Japanese maps of the
period. Two counties are likewise left under their better-known city names:
鄭州 was officially 鄭縣 from 1913 to 1948 and 徐州 was 銅山縣, but
contemporary Japanese usage was 鄭州 and 徐州.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CONV = json.load(open(os.path.expanduser(
    '~/.claude/skills/trad-simp-toggle/assets/convtable.json')))
S2T = dict(zip(CONV['sk'], CONV['sv']))

def to_trad(s):
    return ''.join(S2T.get(c, c) for c in s or '')

# modern name_en -> (characters in 1942, pinyin of that name, romanised form in
# general Western use in 1942). None falls back to the modern form; None for the
# romanisation means it was the same as the pinyin, so nothing is shown.
PERIOD = {
    'Beijing':       (None,       None,           'Peking'),
    'Tianjin':       (None,       None,           'Tientsin'),
    'Zhangjiakou':   (None,       None,           'Kalgan'),
    'Baotou':        (None,       None,           'Paotow'),
    'Hohhot':        ('厚和豪特',  'Houhehaote',   'Kweisui'),
    'Datong':        (None,       None,           'Tatung'),
    'Taiyuan':       (None,       None,           None),
    'Jiexiu':        (None,       None,           'Kiehsiu'),
    'Shijiazhuang':  ('石門',      'Shimen',       'Shihmen'),
    'Xingtai':       (None,       None,           'Hsingtai'),
    'Anyang':        ('彰德',      'Zhangde',      'Changteh'),
    'Kaifeng':       (None,       None,           None),
    'Zhengzhou':     (None,       None,           'Chengchow'),
    'Luoyang':       (None,       None,           'Loyang'),
    'Xuzhou':        (None,       None,           'Suchow'),
    'Jinan':         (None,       None,           'Tsinan'),
    'Qingdao':       (None,       None,           'Tsingtao'),
    'Yantai':        (None,       None,           'Chefoo'),
    'Weihai':        ('威海衛',    'Weihaiwei',    None),
    'Weifang':       ('濰縣',      'Weixian',      'Weihsien'),
    'Jining':        (None,       None,           'Tsining'),
    'Linqing':       (None,       None,           'Lintsing'),
    'Liaocheng':     (None,       None,           None),
    'Dezhou':        ('德縣',      'Dexian',       'Techow'),
    'Linyi':         (None,       None,           None),
    'Rizhao':        (None,       None,           'Jihchao'),
    'Laiwu':         (None,       None,           None),
    'Yishui County': (None,       'Yishui',       None),
}
# Renamings worth spelling out for students, shown in the popup.
NOTE = {
    'Hohhot':       'capital of Mengjiang. 歸綏 Kweisui until the Mengjiang regime '
                    'renamed it 厚和豪特市 in October 1937; it reverted to 歸綏 in 1945 '
                    'and became 呼和浩特 in 1954',
    'Shijiazhuang': 'merged with 休門 and renamed 石門市 under the Japanese occupation; '
                    'it became 石家莊市 in 1947',
    'Weifang':      'the city of 濰坊 Weifang dates only from 1948',
    'Anyang':       'the county was 安陽縣, but the place was generally known, and '
                    'labelled on Japanese maps, by the old prefectural name 彰德',
    'Beijing':      '北平 Peiping under the Nationalists; renamed 北京 by the '
                    'occupation regime in 1937',
    'Weihai':       'the British leased territory of 威海衛 Weihaiwei until 1930, '
                    'then a Chinese special district',
}

path = os.path.join(ROOT, 'data', 'settlements.geojson')
gj = json.load(open(path))
for f in gj['features']:
    p = f['properties']
    en = p.get('name_en') or ''
    hanzi, pinyin, alt = PERIOD.get(en, (None, None, None))
    p['name_zh_period'] = hanzi or to_trad(p.get('name_zh'))
    p['name_en_period'] = pinyin or en
    p['name_alt'] = alt
    p['note'] = NOTE.get(en)
    p.pop('name_zh_trad', None)
json.dump(gj, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))

for f in gj['features']:
    p = f['properties']
    renamed = ' *' if (p['name_en_period'] != p['name_en'] or
                       p['name_zh_period'] != to_trad(p['name_zh'])) else ''
    print(f"{p['name_en_period']:12} {p['name_zh_period']:6} {p['name_alt'] or '-':10}"
          f" (now {p['name_en']} {p['name_zh']}){renamed}")
