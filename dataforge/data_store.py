from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Literal, Optional


@dataclass
class DataEntry:
    source: Literal["_init_", "custom", "import"]
    directory: Optional[str] = None
    created: Optional[datetime] = None
    df: Dict[str, Dict[str, List]] = field(default_factory=dict)

class DataStore:
    def __init__(self):
        self.widget_data = {}
        self.import_data = {}
        self.custom_data = {}
        self.temp = {}
        self.arch = {}
        self.temp_arch = {}
        self.export_data = {}
        self.mean_data = {}
        self.custom_id = 0
        self.all_data: Dict[str, DataEntry] = {}
