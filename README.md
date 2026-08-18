# Japanese North China Area Army Map — September 1942

北支那方面軍占拠地域内治安概況

A small Leaflet page for students to explore four layers from the QGIS project
`basic project.qgz`, over a choice of base maps.

## Layers

| # in QGIS | Layer | Rendering |
|---|---|---|
| 10 | Japanese-occupied territory | light blue polygons |
| 9 | Resistance areas | light red polygons |
| 5 | Resistance attacks | dark red graduated circles, sized by `strength` |
| 6 | Settlements | black points labelled `Pinyin (1942 name 傳統漢字)` |

Base maps: CARTO Light (default), OpenStreetMap Standard, Esri World Imagery.

The graduated symbology for the attacks layer reproduces the QGIS style: six
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

- `name_zh_trad` — traditional-character form of `name_zh` (the source mixes
  simplified and traditional, so conversion runs straight off the source string).
- `name_alt` — the name the place went by around 1942, in the Chinese Postal Map
  romanisation then in general use (Peking, Tientsin, Kalgan, Kweisui, …). The
  source field was empty; edit the `PERIOD` table in that script to change them.

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

- Volume: [戦史叢書第050巻 北支の治安戦＜2＞](https://www.nids.mod.go.jp/military_history_search/SoshoView?kanno=050)
- The map: [付図第五](https://www.nids.mod.go.jp/military_history_search/SoshoAppendixView?no=050&f=050_332.jpg)

## Licence

Public domain — no copyright is claimed over the original map or over this
website. Attribution for the georeferencing and digitisation work (Konrad M.
Lawson) is asked for as a courtesy. See [LICENSE](LICENSE).
