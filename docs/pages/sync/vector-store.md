# Vector Stores 

`geoserverx` allows users to access all/one vector stores from geoserver. As of now, `geoserverx` also supports new vector store creation for `shapefile` and `gpkg` data

## Get all Vector stores 
This command fetches all Vector store available in given workspace from geoserver. 

```Python
# Get all vector stores available in `cite` workspace
client.get_vector_stores_in_workspaces('cite')
```



## Get single Vector store
This command fetches all Information about Vector store available in given workspace from geoserver. 

```Python
# Get all information about `shape` vector stores available in `cite` workspace

client.get_vector_store(workspace='cite', store='shape') 
```


## Create new shapefile Vector store
Use this command to create new Vector store based on `shapefile` path. 

```Python
# Create new store in `cite` workspace with name `shape` and using `path/for/shapefile` as local shapefile path
client.create_file_store(workspace='cite', store='shape', file='path/for/shapefile', service_type='shapefile') 
```


## Create new geopackage Vector store
Use this command to create new Vector store based on `Geopackage` path. 

```Python
# Create new store in `cite` workspace with name `shape` and using `path/for/gpkg` as local Geopackage path
client.create_file_store(workspace='cite', store='shape', file='path/for/gpkg', service_type='gpkg') 
```
