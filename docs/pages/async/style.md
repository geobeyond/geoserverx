# Style 


## Get all Styles  

This command fetches all Styles available in geoserver. 

```Python
# Get all styles available in geoserver
await client.get_allstyles()
```


## Get single Style

This command fetches information about particular Style from geoserver. 

```py
# Get information about `population` style from geoserver
await client.get_style('population') 
```
