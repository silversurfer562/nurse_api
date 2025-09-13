"""
Summary generation endpoints.
"""
import json
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.schemas import SummaryRequest, SummaryResponse, SourceInfo
from app.services.cache_service import cache_service
from app.services.openai_service import openai_service
from app.services.biomedical_service import biomedical_service
from loguru import logger

router = APIRouter()


@router.post("/summaries", response_model=SummaryResponse)
async def generate_summary(
    request: SummaryRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate an AI-powered summary based on biomedical research.
    
    This endpoint creates draft content by:
    1. Searching biomedical databases (PubMed, ClinicalTrials.gov, etc.)
    2. Using AI to synthesize information into readable summaries
    3. Applying reading level and word count customizations
    4. Including proper source citations and disclaimers
    
    **⚠️ Important Safety Notice:**
    - All content is generated for draft purposes only
    - Requires review by qualified healthcare professionals
    - Not intended for direct patient care decisions
    - Does not replace clinical judgment
    """
    try:
        # Check cache first
        cache_key = {
            "query": request.query,
            "content_type": request.content_type.value,
            "reading_level": request.reading_level.value,
            "word_count": request.word_count,
            "audience": request.audience
        }
        
        cached_result = await cache_service.get("summary", cache_key)
        if cached_result:
            logger.info(f"Returning cached summary for query: {request.query}")
            return SummaryResponse.model_validate(json.loads(cached_result))
        
        # Fetch sources from biomedical databases
        logger.info(f"Fetching sources for query: {request.query}")
        sources = await biomedical_service.get_all_sources(request.query)
        
        if not sources:
            logger.warning(f"No sources found for query: {request.query}")
            sources = []
        
        # Generate content using OpenAI
        content = await openai_service.generate_content(
            query=request.query,
            content_type=request.content_type,
            reading_level=request.reading_level,
            word_count=request.word_count,
            sources=sources,
            audience=request.audience
        )
        
        # Count actual words in generated content
        actual_word_count = len(content.split())
        
        # Prepare response
        response = SummaryResponse(
            content=content,
            word_count=actual_word_count,
            reading_level=request.reading_level,
            content_type=request.content_type,
            sources=sources if request.include_sources else [],
            metadata={
                "query": request.query,
                "target_word_count": request.word_count,
                "generation_timestamp": datetime.utcnow().isoformat(),
                "sources_count": len(sources)
            }
        )
        
        # Cache the result in the background
        background_tasks.add_task(
            cache_service.set,
            "summary",
            cache_key,
            response.model_dump_json(),
            3600  # 1 hour TTL
        )
        
        logger.info(f"Generated summary for query: {request.query}")
        return response
        
    except Exception as e:
        logger.error(f"Summary generation error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate summary. Please try again later."
        )


@router.get("/summaries/sources/{query}")
async def get_sources(query: str) -> List[SourceInfo]:
    """
    Get available sources for a given query without generating content.
    
    This endpoint searches biomedical databases and returns available sources
    that would be used for content generation. Useful for previewing source
    quality before generating expensive AI content.
    """
    try:
        # Check cache
        cache_key = {"query": query, "endpoint": "sources"}
        cached_result = await cache_service.get("sources", cache_key)
        
        if cached_result:
            sources_data = json.loads(cached_result)
            return [SourceInfo.model_validate(source) for source in sources_data]
        
        # Fetch sources
        sources = await biomedical_service.get_all_sources(query)
        
        # Cache the result
        await cache_service.set(
            "sources", 
            cache_key, 
            json.dumps([source.model_dump() for source in sources]),
            1800  # 30 minutes TTL
        )
        
        return sources
        
    except Exception as e:
        logger.error(f"Sources fetch error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch sources. Please try again later."
        )