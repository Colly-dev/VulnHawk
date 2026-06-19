
import yaml
import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            # Fallback to absolute path if relative fails
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            abs_path = os.path.join(base_dir, self.config_path)
            if os.path.exists(abs_path):
                self.config_path = abs_path
            else:
                return {}

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config_data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def get_all(self) -> Dict[str, Any]:
        return self.config_data
