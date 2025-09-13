"""
Configuration management for the Nurse AI Assistant API.
"""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Nurse AI Assistant API"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Security
    secret_key: str = "change-this-in-production"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Rate limiting
    max_requests_per_minute: int = 60
    
    # NCBI/PubMed
    ncbi_api_key: Optional[str] = None
    ncbi_email: Optional[str] = None
    pubmed_api_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    # MyGene/MyChem
    mygene_api_url: str = "https://mygene.info/v3"
    mychem_api_url: str = "https://mychem.info/v1"
    
    # ClinicalTrials.gov
    clinicaltrials_api_url: str = "https://clinicaltrials.gov/api"
    
    # MedlinePlus
    medlineplus_api_url: str = "https://wsearch.nlm.nih.gov/ws/query"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()