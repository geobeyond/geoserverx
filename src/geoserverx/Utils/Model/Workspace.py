from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class Workspace:
    name : str
    default : bool
    isolated : bool