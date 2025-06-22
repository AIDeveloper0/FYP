"""
Configuration settings for the application
"""
from pydantic import BaseSettings, validator
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    PROJECT_NAME: str = "Diagram Converter API"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    
    # Pattern files
    PATTERNS_DIR: Path = DATA_DIR / "patterns"
    FLOWCHART_PATTERNS_FILE: Path = PATTERNS_DIR / "flowchart_patterns.json"
    
    # Examples files
    EXAMPLES_DIR: Path = DATA_DIR / "examples"
    FLOWCHART_EXAMPLES_FILE: Path = EXAMPLES_DIR / "flowchart_examples.json"
    
    @validator("*")
    def ensure_paths_exist(cls, v):
        """Ensure all paths exist"""
        if isinstance(v, Path) and not v.exists():
            os.makedirs(v, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()