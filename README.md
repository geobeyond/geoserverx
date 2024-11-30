# GeoServerX

A modern, powerful GeoServer REST API client influenced by HTTPX, offering Sync, Async, and CLI capabilities.

[![Downloads](https://pepy.tech/badge/geoserverx)](https://pepy.tech/project/geoserverx)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

## Features

- 🚀 Synchronous and Asynchronous API support
- 🖥️ Command Line Interface (CLI)
- 🔄 Complete GeoServer REST API coverage
- 🏗️ Modern Pythonic interface
- 📦 Easy to install and use
- 📝 Type hints for better development experience

## Installation

```bash
pip install geoserverx
```
## Quick Start
### Synchronous Usage
```python
from geoserverx._sync.gsx import SyncGeoServerX

# Initialize with default GeoServer settings
# Default: URL=http://localhost:8080/geoserver/rest, username=admin, password=geoserver
geo_server = SyncGeoServerX()

# Custom initialization
geo_server = SyncGeoServerX(
    url="http://your-server:8080/geoserver/rest",
    username="your_username",
    password="your_password"
)

# Get all workspaces
workspaces = geo_server.get_all_workspaces()

# Access workspace information
print(workspaces)  # Print Workspaces Model
print(workspaces.workspaces)  # Print detailed list of workspaces
print(workspaces.workspaces.workspace[0].name)  # Print first workspace name
```

### Asynchronous Usage
```python
from geoserverx._async.gsx import AsyncGeoServerX
import asyncio

async def main():
    geo_server = AsyncGeoServerX()
    workspaces = await geo_server.get_all_workspaces()
    print(workspaces)

asyncio.run(main())
```

### CLI Usage
```bash
# Get help
geoserverx --help

# List workspaces
geoserverx workspaces list

# Add a new workspace
geoserverx workspaces create --name my_workspace
```

## Documentation
Detailed documentation is available through [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

## Development Setup
Install Poetry (dependency management tool):
```bash
  curl -sSL https://install.python-poetry.org | python3 -
```
```bash
# Clone the repository:
git clone https://github.com/geobeyond/geoserverx.git
cd geoserverx
```
```bash
# Install dependencies:
poetry install
```
```bash

# Activate virtual environment:
poetry shell
```

## Contributing
We welcome contributions! Here's how you can help:

- Check for open issues or create a new one to discuss new features or bugs.
- Fork the repo and create a new branch for your contribution.
- Write your code and tests.
- Send a pull request.

## Development Guidelines

- Follow [Black](https://black.readthedocs.io/en/stable/) code style
- Use [isort](https://pycqa.github.io/isort/index.html) ([black profile](https://pycqa.github.io/isort/docs/configuration/black_compatibility.html)) for import sorting
- Use [Ruff](https://docs.astral.sh/ruff/) for linting
- Ensure all tests pass
- Add tests for new features
- Update documentation as needed

## Bug Reports and Feature Requests
Please use the GitHub issue tracker to report bugs or request features.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- HTTPX for inspiration
- GeoServer community
- All contributors who have helped shape this project