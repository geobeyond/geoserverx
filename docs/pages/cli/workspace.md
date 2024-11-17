# Workspaces 

`geoserverx` allows users to access all/one workspace from GeoServer, along with ability to add new workspaces. 

!!! get "Get started"
    To start using `geoserverx` using command line, activate the Environment where package is installed and use `gsx` command



## Paramters for all workspaces command

<div class="termy">

```console
$ gsx workspaces --help

Usage: gsx workspaces [OPTIONS]

  Get all workspaces in the Geoserver

Options:
  --request [sync|async]  [default: requestEnum._sync]
  --url TEXT              Geoserver REST URL  [default:
                          http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT         Geoserver Password  [default: GeoServer]
  --username TEXT         Geoserver username  [default: admin]
  --help                  Show this message and exit.
```
</div>

As listed above, `workspaces` command accepts four parameters. 


* request type ( sync or async )
* url - Geoserver REST URL
* password - Password for GeoServer
* username - Username for GeoServer

All these parameters have default value setup which will work for local default installation

## Get all workspaces

<div class="termy">
```console
$ gsx workspaces

{"workspaces": {"workspace": [{"name": "cesium", "href": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium.json"}]}}
```
</div>

## Get all workspaces of hosted GeoServer

<div class="termy">
```console
$ gsx workspaces --url http://locahost:8080/geoserver/rest --password myPassword --username admin
{"workspaces": {"workspace": [{"name": "giz", "href": 
"http://locahost:8080/geoserver/rest/workspaces/giz.json"}]}}
```
</div>


## Paramters to get single workspace command

<div class="termy">

```console
$ gsx workspace --help
Usage: gsx workspace [OPTIONS]

  Get workspace in the Geoserver

Options:
  --request [sync|async]  [default: requestEnum._sync]
  --workspace TEXT        Workspace name  [required]
  --url TEXT              Geoserver REST URL  [default:
                          http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT         Geoserver Password  [default: GeoServer]
  --username TEXT         Geoserver username  [default: admin]
  --help                  Show this message and exit.
```
</div>

As listed above, `workspace` accepts `workspace` parameter as the name of workspace 


## Get single workspaces

<div class="termy">
```console
$ gsx workspace cesium
{"workspace": {"name": "cesium", "isolated": false, "dateCreated": "2023-02-13 
06:43:28.793 UTC", "dataStores": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/datastores.json", 
"coverageStores": 
"http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/coveragestores.json", 
"wmsStores": "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/wmsstores.json", 
"wmtsStores": "http://127.0.0.1:8080/geoserver/rest/workspaces/cesium/wmtsstores.json"}}
```
</div>


## Parameters for create workspace command

<div class="termy">

```console
$ gsx create-workspace --help
Usage: gsx create-workspace [OPTIONS]

  Add workspace in the Geoserver

Options:
  --request [sync|async]      [default: requestEnum._sync]
  --workspace TEXT            Workspace name  [required]
  --default / --no-default    Make workspace default?  [default: no-default]
  --isolated / --no-isolated  Make workspace isolated?  [default: no-isolated]
  --url TEXT                  Geoserver REST URL  [default:
                              http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT             Geoserver Password  [default: GeoServer]
  --username TEXT             Geoserver username  [default: admin]
  --help                      Show this message and exit.
```
</div>

As listed above, `create-workspace` command accepts parameters as follows

* workspace - name of workspace
* --default/--no-default - To keep workspace either default or not
* --isolated/--no-isolated - To keep workspace either isolated or not


## Create single workspaces

<div class="termy">
```console
$ gsx create-workspace mydefaultws --default
code=201 response='Data added successfully'
```
</div>

## Parameters for delete workspace command

<div class="termy">

```console
$ gsx delete-workspace --help
Usage: gsx delete-workspace [OPTIONS]

  Delete workspace in the Geoserver

Options:
  --request [sync|async]  [default: requestEnum._sync]
  --workspace TEXT        Workspace name  [required]
  --recurse / --no-recurse  Delete all stores,layers,styles,etc.  [default: no-recurse]
  --url TEXT              Geoserver REST URL  [default:
                          http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT         Geoserver Password  [default: geoserver]
  --username TEXT         Geoserver username  [default: admin]
  --help                  Show this message and exit.
```
</div>

As listed above, `delete-workspace` command accepts parameters as follows

* --current_name - name of workspace
* --recurse / --no-recurse - This parameter recursively deletes all layers referenced by the specified workspace, including data stores, coverage stores, feature types, and so on

## Delete single workspaces

<div class="termy">
```console
gsx delete-workspace my_wrkspace --recurse
{"code":200,"response":"Executed successfully"}
```
</div>


## Parameters for update workspace command

<div class="termy">

```console
$ gsx update-workspace --help
Usage: gsx update-workspace [OPTIONS]

  Add workspace in the Geoserver

Options:
  --request [sync|async]      [default: requestEnum._sync]
  --current-name TEXT         Current Workspace name  [required]
  --new-name TEXT             New Workspace name
  --isolated / --no-isolated  Make workspace isolated?  [default: no-isolated]
  --url TEXT                  Geoserver REST URL  [default:
                              http://127.0.0.1:8080/geoserver/rest/]
  --password TEXT             Geoserver Password  [default: geoserver]
  --username TEXT             Geoserver username  [default: admin]
  --help                      Show this message and exit.
```
</div>

As listed above, `update-workspace` command accepts parameters as follows

* --current-name - name of current workspace
* --new-name - name of new workspace
* --isolated/--no-isolated - To keep workspace either isolated or not

## Update single workspaces

<div class="termy">
```console
gsx update-workspace d --new-name duster
{"code":200,"response":"Executed successfully"}
```
</div>