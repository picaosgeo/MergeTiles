# -*- coding: utf-8 -*-
#con.execute_non_query(INSERT_EX_SQ.encode('your language encoder'))
#
# MBTile Tile Merge tool
#
# USAGE:python mergetiles -src src.mbtiles -dest dest.mbtiles -zoom 17,18,19
#

from os import getenv
import sys
import math
import sqlite3

def Usage():
	print('Usage: mergetiles.py ')
	print('        [-src src_mbtiles_file]')
	print('        [-dest dest_mbtiles_file]')
	print('        [-zoom zoom_level]')


def num2deg(xtile, ytile, zoom):
	n = 2.0 ** zoom
	lon_deg = xtile / n * 360.0 - 180.0
	lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
	lat_deg = math.degrees(lat_rad)
	return (-lat_deg, lon_deg)


srctablename=None
desttablename=None
zoom_level=[]

argv=sys.argv

i = 1
while i < len(argv):
	arg = argv[i]

	if arg == '-src':
		i+=1
		srctablename = argv[i]
	elif arg == '-dest':
		i+=1
		desttablename = argv[i]
	elif arg == '-zoom':
		i+=1
		arg=argv[i].split(",")
		zoom_level=map(int,arg)
	elif arg[:1] == '-':
		Usage()
		sys.exit(0)
	else:
		i+=1

print srctablename
print desttablename
print zoom_level

if srctablename == None or desttablename == None or len(zoom_level) < 1:
	Usage()
	sys.exit(0)

try :
	conn1 = sqlite3.connect(srctablename)
	cursor1 = conn1.cursor() 

	conn2 = sqlite3.connect(desttablename)
	cursor2 = conn2.cursor() 

	# src から dest へタイルインサート
	for src_zoom_level in zoom_level:

		sqltext = u"SELECT * FROM tiles where zoom_level = "  + str(src_zoom_level)

		cursor1.execute(sqltext)
		row = cursor1.fetchone()
		while row:
			print row[0],row[1],row[2]
			cursor2.execute('''INSERT OR REPLACE INTO tiles(zoom_level, tile_column, tile_row, tile_data) VALUES (?,?,?,?);''',(row[0],row[1],row[2],buffer(row[3])))
			row = cursor1.fetchone()

	conn2.commit()


	#dest の最大レベルのエクステントを作成する
	cursor2.execute("select min(zoom_level),max(zoom_level) from tiles")
	row = cursor2.fetchone()
	print row
	minzoom = min(row[0],min(zoom_level))
	maxzoom = max(row[1],max(zoom_level))

	print minzoom,maxzoom

	cursor2.execute("select min(tile_column), min(tile_row), max(tile_column),max(tile_row) from tiles where zoom_level=%i" % maxzoom)
	row = cursor2.fetchone()

	print row[0],row[1],row[2],row[3]
	lonlat = num2deg(row[0],row[1],maxzoom)
	print lonlat
	lonlat2 = num2deg(row[2]+1,row[3]+1,maxzoom)
	print lonlat2

	s= str(lonlat[1])+','+str(lonlat[0])+','+str(lonlat2[1])+','+str(lonlat2[0])
	print s

	cursor2.execute('''INSERT OR REPLACE INTO metadata(name, value) VALUES (?,?);''',('minZoom',minzoom))
	cursor2.execute('''INSERT OR REPLACE INTO metadata(name, value) VALUES (?,?);''',('maxZoom',maxzoom))
	cursor2.execute('''INSERT OR REPLACE INTO metadata(name, value) VALUES (?,?);''',('bounds',s))

	conn2.commit()

	cursor2.execute("""ANALYZE;""")
	cursor2.execute("""VACUUM;""")
	conn2.close()
	conn1.close()

	sys.exit(0)

except Exception,err:
	print err
	sys.exit(1)
