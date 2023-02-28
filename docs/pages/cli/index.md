# Command line access

`geoserverx` allows users to leverage power of command line to communicate with geoserver.
`gsx` is a command line tool by `geoserverx`. 

## Installation
To use `gsx` , Install `geoserverx` using `pip` on local environment. 

<div class="termy">

```
gsx --help
Usage: gsx [OPTIONS] COMMAND [ARGS]...

  GeoserverX CLI tools to talk to Geoserver efficiently .

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create-file       Create Vector Layer in Geoserver
  create-workspace  Add workspace in the Geoserver
  raster-st-wp      Get raster stores in specific workspaces
  raster-store      Get raster store information in specific workspaces
  style             Get style in Geoserver
  styles            Get all styles in Geoserver
  vector-st-wp      Get vector stores in specific workspaces
  vector-store      Get vector store information in specific workspaces
  workspace         Get workspace in the Geoserver
  workspaces        Get all workspaces in the Geoserver
```
</div>

Checkout other pages to understand how to use Command line 