import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = Path("config.json")
        if not config_path.exists():
            # Fallback defaults if config.json is missing
            self._config = {
                "BASE_URL": "http://127.0.0.1:8000",
                "UPLOAD_DIR": "data/sites",
                "DB_PATH": "data/db/app.db",
                "LOG_LEVEL": "INFO"
            }
            return

        with open(config_path, "r") as f:
            self._config = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    @property
    def base_url(self) -> str:
        return self.get("BASE_URL", "http://127.0.0.1:8000")

    @property
    def upload_dir(self) -> Path:
        return Path(self.get("UPLOAD_DIR", "data/sites"))

    @property
    def db_path(self) -> Path:
        return Path(self.get("DB_PATH", "data/db/app.db"))
    
    @property
    def log_level(self) -> str:
        return self.get("LOG_LEVEL", "INFO")

    @property
    def upload_password(self) -> str:
        return self.get("UPLOAD_PASSWORD", "admin")

    @property
    def cf_zone_id(self) -> str:
        return self.get("CF_ZONE_ID", "")

    @property
    def cf_api_token(self) -> str:
        return self.get("CF_API_TOKEN", "")

    @property
    def domain_name(self) -> str:
        return self.get("DOMAIN_NAME", "a.104800.xyz")

    @property
    def iflow_api_key(self) -> str:
        return self.get("IFLOW_API_KEY", "")

    def update_iflow_key(self, key: str):
        self._config["IFLOW_API_KEY"] = key
        config_path = Path("config.json")
        with open(config_path, "w") as f:
            json.dump(self._config, f, indent=4)

config = ConfigManager()
