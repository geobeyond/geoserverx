# Raster Stores 

`geoserverx` allows users to access all/one raster stores from GeoServer


## Get all raster stores 
This command fetches all Vector store available in given workspace from GeoServer. 

```py
# Get all raster stores available in `cite` workspace
client.get_raster_stores_in_workspaces('cite')
```


## Get single raster store

This command fetches all Information about raster store available in given workspace from GeoServer. 

```Python
# Get all information about `image` raster stores available in `cite` workspace

client.get_raster_store(workspace='cite', store='image') 
```
