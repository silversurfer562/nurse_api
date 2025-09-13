"""Configuration settings for the Nurse's AI Assistant API"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # API Configuration
    api_title: str = "Nurse's AI Assistant API"
    api_version: str = "1.0.0"
    debug_mode: bool = False
    
    # Security and Compliance
    max_content_length: int = 10000  # Maximum word count for generated content
    enable_content_filtering: bool = True
    require_clinician_review: bool = True
    
    # LLM Configuration (placeholder for future integration)
    llm_model: str = "gpt-3.5-turbo"  # Default model
    llm_api_key: Optional[str] = None
    llm_max_tokens: int = 2000
    
    # Biomedical Data Sources (placeholder for future integration)
    pubmed_api_key: Optional[str] = None
    enable_live_data: bool = False
    
    # Reading Levels
    available_reading_levels: list = ["elementary", "middle-school", "high-school", "college", "professional"]
    default_reading_level: str = "high-school"
    
    model_config = {"env_file": ".env", "case_sensitive": False}


# Global settings instance
settings = Settings()