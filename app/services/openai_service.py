"""
OpenAI service for content generation.
"""
import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from app.config import settings
from app.models.schemas import ReadingLevel, ContentType, SourceInfo
from loguru import logger


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        self.client: Optional[AsyncOpenAI] = None
        self.model = "gpt-4-turbo-preview"
    
    def initialize(self):
        """Initialize OpenAI client."""
        if settings.openai_api_key:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI client initialized")
        else:
            logger.warning("OpenAI API key not provided. Content generation will be mocked.")
    
    def _get_reading_level_description(self, reading_level: ReadingLevel) -> str:
        """Get description for reading level."""
        descriptions = {
            ReadingLevel.ELEMENTARY: "elementary school level (grades 1-5), very simple language",
            ReadingLevel.MIDDLE_SCHOOL: "middle school level (grades 6-8), simple language with basic medical terms",
            ReadingLevel.HIGH_SCHOOL: "high school level (grades 9-12), moderate complexity",
            ReadingLevel.COLLEGE: "college level, more sophisticated vocabulary and concepts",
            ReadingLevel.GRADUATE: "graduate level, advanced terminology and concepts",
            ReadingLevel.PROFESSIONAL: "professional healthcare level, full medical terminology"
        }
        return descriptions.get(reading_level, "high school level")
    
    def _get_content_type_prompt(self, content_type: ContentType) -> str:
        """Get specific prompt for content type."""
        prompts = {
            ContentType.PATIENT_EDUCATION: "Create patient-friendly educational material that explains the condition, symptoms, treatment options, and self-care tips.",
            ContentType.CLINICAL_SUMMARY: "Create a clinical summary for healthcare professionals with key diagnostic criteria, treatment protocols, and clinical considerations.",
            ContentType.RESEARCH_SUMMARY: "Create a research summary highlighting key findings, methodology, and clinical implications from recent studies.",
            ContentType.MEDICATION_INFO: "Create medication information including mechanism of action, dosing, side effects, and patient counseling points.",
            ContentType.CONDITION_OVERVIEW: "Create a comprehensive condition overview covering pathophysiology, epidemiology, diagnosis, and management."
        }
        return prompts.get(content_type, "Create educational content about the medical topic")
    
    async def generate_content(
        self,
        query: str,
        content_type: ContentType,
        reading_level: ReadingLevel,
        word_count: int,
        sources: List[SourceInfo],
        audience: Optional[str] = None
    ) -> str:
        """Generate content using OpenAI."""
        
        if not self.client:
            # Return mock content if OpenAI is not available
            return self._generate_mock_content(query, content_type, reading_level, word_count)
        
        try:
            # Build the prompt
            reading_level_desc = self._get_reading_level_description(reading_level)
            content_prompt = self._get_content_type_prompt(content_type)
            
            audience_text = f" for {audience}" if audience else ""
            
            sources_text = ""
            if sources:
                sources_text = "\n\nBase your content on these sources:\n"
                for i, source in enumerate(sources[:5], 1):  # Limit to top 5 sources
                    sources_text += f"{i}. {source.title}"
                    if source.authors:
                        sources_text += f" by {', '.join(source.authors[:3])}"
                    if source.publication_date:
                        sources_text += f" ({source.publication_date})"
                    sources_text += "\n"
            
            system_prompt = f"""You are a medical writing assistant helping nurses and healthcare professionals create evidence-based content. 

IMPORTANT SAFETY GUIDELINES:
- Always include a disclaimer that this is draft content requiring clinical review
- Do not provide specific medical advice or diagnoses
- Focus on educational and informational content
- Emphasize the need for professional medical consultation

Write at a {reading_level_desc} reading level{audience_text}."""

            user_prompt = f"""{content_prompt}

Topic: {query}
Target word count: {word_count} words
Reading level: {reading_level_desc}

{sources_text}

Format the response as clear, well-structured content with appropriate headings and bullet points where helpful. Include a disclaimer at the end about consulting healthcare professionals."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=min(word_count * 2, 4000),  # Rough estimate
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            logger.info(f"Generated content for query: {query}")
            return content
            
        except Exception as e:
            logger.error(f"OpenAI content generation error: {e}")
            return self._generate_mock_content(query, content_type, reading_level, word_count)
    
    def _generate_mock_content(
        self, 
        query: str, 
        content_type: ContentType, 
        reading_level: ReadingLevel, 
        word_count: int
    ) -> str:
        """Generate mock content when OpenAI is not available."""
        
        mock_content = f"""# {query.title()}

This is a draft {content_type.value.replace('_', ' ')} about {query}, written at {reading_level.value.replace('_', ' ')} level.

## Overview
This content would normally be generated by AI to provide evidence-based information about {query}. The system would integrate information from multiple biomedical sources to create comprehensive, accurate content.

## Key Points
- Information would be sourced from PubMed research articles
- Clinical trial data from ClinicalTrials.gov would be included
- Patient education resources from MedlinePlus would be referenced
- Gene and drug information from MyGene and MyChem databases would be incorporated

## Target Audience
This content is designed for {reading_level.value.replace('_', ' ')} reading comprehension and would typically contain approximately {word_count} words.

**IMPORTANT DISCLAIMER:** This is draft content for educational purposes only. All medical information should be reviewed by qualified healthcare professionals before use. Patients should consult with their healthcare providers for personalized medical advice and treatment decisions."""
        
        return mock_content


# Global OpenAI service instance
openai_service = OpenAIService()