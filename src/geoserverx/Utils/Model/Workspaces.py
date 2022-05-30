from dataclasses import dataclass,field
from typing import Optional
from typing import Any, List, Optional

from .WorkspaceBulk import WorkspaceBulk

@dataclass
class Workspaces : 
    workspace : dict = field(default_factory={'Workspace': List[WorkspaceBulk]})