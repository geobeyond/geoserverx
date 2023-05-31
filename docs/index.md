# Welcome to geoserverx 

`geoserverx` is a modern Python package that provides an efficient and scalable way to interact with Geoserver REST APIs. It leverages the asynchronous capabilities of Python to offer a high-performance and reliable solution for managing Geoserver data and services.

With geoserverx, users can easily access and modify data in Geoserver, such as uploading and deleting shapefiles, publishing layers, creating workspaces, styles, etc. . The package supports asynchronous requests along with synchronous method to the Geoserver REST API, which enables users to perform multiple tasks simultaneously, improving performance and reducing wait times.

Apart from being implemented as Python package, geoserverx also provides CLI support for all of its operations. Which makes it useful for people who want to avoid Python all-together. 

Checkout official pypi link [here](https://pypi.org/project/geoserverx/)

## Get Started

`geoserverx` can be installed using `pip` or `pip3`

<div class="termy">

```console

pip install geoserverx

---> 100%
```
</div>

After which , It can be used in Python projects using <i>sync, async</i> methods or can ve used as Command Line tool

## For testing purpose
If you don't have geoserver installed locally, feel free to use following command to quickly spin up Geoserver using [Docker](https://www.docker.com/)

<div class="termy">
```console
docker run -e GEOSERVER_ADMIN_USER=admin -e GEOSERVER_ADMIN_PASSWORD=geoserver -e SAMPLE_DATA=true -p 8080:8080 kartoza/geoserver
```
</div>

Please not that this will work on amd64 architecture machines.