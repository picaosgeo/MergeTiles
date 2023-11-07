# MergeTiles

MBTile tile merge tool.

## Install
```
git clone git@github.com:m05quit0/MergeTiles.git
cd MergeTiles
```

## Usage:

```sh
python mergetiles.py -src src_mbtiles_file -dest dest_mbtiles_file -zoom zoom_level1,zoom_level2,zoom_level3,...
```

Example:
```sh
python mergetiles -src src.mbtiles -dest dest.mbtiles -zoom 17,18,19
```

'minZoom', 'maxZoom', 'bounds' entry of metadata table will be automatically update with max zoom level extent.
