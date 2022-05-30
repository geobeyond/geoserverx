from dataclasses import dataclass

from pyparsing import Optional


@dataclass
class Style:
    code : int
    name : str
    format : str
    languageVersion : Optional[dict]
    filename : str