# MergeTiles

MBTile Tile Merge tool

##USage:
mergetiles.py 

  -src src_mbtiles_file

  -dest dest_mbtiles_file

  -zoom zoom_level

ex) python mergetiles -src src.mbtiles -dest dest.mbtiles -zoom 17,18,19

'minZoom','maxZoom','bounds' entry of metadata table will be automatically update with max zoom level extent.

Need python2.7 or later and sqlite3 python module.


