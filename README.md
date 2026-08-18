# Japanese North China Area Army Map — September 1942

北支那方面軍占拠地域内治安概況

A small Leaflet page for students to explore four layers from the QGIS project
`basic project.qgz`, over a choice of base maps.

## Layers

| # in QGIS | Layer | Rendering |
|---|---|---|
| 10 | Pacified areas 治安地区 | light blue polygons |
| 9 | Un-pacified areas 未治安地区 | light red polygons |
| 5 | Guerrilla attacks | dark red graduated circles, sized by `strength` |
| 6 | Settlements | black points labelled `Pinyin` over `(漢字 alt. name)`, both as of 1942 |

Areas left blank on the original sheet are its third category, semi-pacified
areas (準治安地区), and are left unshaded here too.

Base maps: CARTO Light (default), OpenStreetMap Standard, Esri World Imagery.

The graduated symbology for the guerrilla attacks layer reproduces the QGIS style: six
classes on a log scale (5 – 10⁴) with marker sizes 1.7–4.3 mm, converted to
pixels at 96 dpi.

## Data

`data/*.geojson` are exported from the GeoPackages in the QGIS project with
`ogr2ogr` (EPSG:4326, RFC 7946). To rebuild:

```sh
export PATH=/Applications/QGIS-LTR.app/Contents/MacOS/bin:$PATH
G="$HOME/Library/CloudStorage/Dropbox/GIS/China"
ogr2ogr -f GeoJSON -t_srs EPSG:4326 -lco RFC7946=YES -lco COORDINATE_PRECISION=6 \
  data/attacks.geojson "$G/resistance-attacks-1942.gpkg" resistanceattack
ogr2ogr -f GeoJSON -t_srs EPSG:4326 -lco RFC7946=YES -lco COORDINATE_PRECISION=6 \
  data/settlements.geojson "$G/north-china-major-settlements.gpkg" northchinasettlements
ogr2ogr -f GeoJSON -t_srs EPSG:4326 -lco RFC7946=YES -lco COORDINATE_PRECISION=6 \
  data/resistance-areas.geojson "$G/resistance-area-1942.gpkg" resistanceareas1942map
ogr2ogr -f GeoJSON -t_srs EPSG:4326 -lco RFC7946=YES -lco COORDINATE_PRECISION=6 \
  data/japanese-occupied.geojson "$G/Japanese Occupied Territory/japna-occupied-1942-map.gpkg" japanoccupied1942
python3 tools/enrich_settlements.py
```

`tools/enrich_settlements.py` adds two fields the source layer does not carry:

- `name_zh_period` — the characters the place went by around 1942. Where the
  name has since changed outright (歸綏→呼和浩特, 石門→石家莊, 德縣→德州,
  濰縣→濰坊, 彰德→安陽) the period form is listed explicitly; otherwise the
  traditional form of `name_zh` is used, converted straight off the source
  string rather than round-tripped.
- `name_alt` — the romanised name in general use at the time (Peking, Tientsin,
  Kalgan, Kweisui, Chefoo …), left empty where it matches the pinyin. The source
  field was empty; edit the `PERIOD` table in that script to change either field.

Prefectural names abolished in 1913 (順德府, 東昌府, 沂州府) are deliberately not
used — by 1942 those places went by their county names.

## Running locally

Needs a web server, because the page fetches the GeoJSON files:

```sh
python3 -m http.server 8000   # then open http://localhost:8000/
```

## Source

The map is 付図第五「北支那方面軍占拠地域内治安概況（昭和十七年九月中）」, an appendix
to 防衛庁防衛研修所戦史室 編『北支の治安戦＜2＞』(戦史叢書 第50巻, 東京: 朝雲新聞社,
1971).

The volume has been scanned and is readable online at the National Institute for
Defense Studies (防衛省防衛研究所):

- The scanned sheet, in this repository:
  [`original/hokushi-chian-gaikyo-1942-09.jpg`](original/hokushi-chian-gaikyo-1942-09.jpg)
  (3768×3066) — the layers on the page are traced from it
- Volume: [戦史叢書第050巻 北支の治安戦＜2＞](https://www.nids.mod.go.jp/military_history_search/SoshoView?kanno=050)
- The map: [付図第五](https://www.nids.mod.go.jp/military_history_search/SoshoAppendixView?no=050&f=050_332.jpg)

## Licence

Public domain — no copyright is claimed over the original map or over this
website. Attribution for the georeferencing and digitisation work (Konrad M.
Lawson) is asked for as a courtesy. See [LICENSE](LICENSE).
