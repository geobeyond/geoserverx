from typing import List, Optional

from pydantic import BaseModel


class Metric(BaseModel):
    available: bool
    description: str
    name: str
    unit: Optional[str]
    category: str
    identifier: str
    priority: int
    value: str

class Metrics(BaseModel):
    metric: List[Metric]

class MetricsDataModel(BaseModel):
    metrics: Metrics
