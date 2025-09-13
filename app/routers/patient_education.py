"""Patient education material generation endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import PatientEducationRequest
from app.models.responses import PatientEducationResponse, ErrorResponse
from app.services.content_generator import ContentGeneratorService
from app.services.compliance_checker import ComplianceCheckerService

router = APIRouter()


def get_content_generator():
    """Dependency to get content generator service"""
    return ContentGeneratorService()


def get_compliance_checker():
    """Dependency to get compliance checker service"""
    return ComplianceCheckerService()


@router.post("/patient-education", 
             response_model=PatientEducationResponse,
             responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def generate_patient_education(
    request: PatientEducationRequest,
    content_generator: ContentGeneratorService = Depends(get_content_generator),
    compliance_checker: ComplianceCheckerService = Depends(get_compliance_checker)
):
    """
    Generate patient education materials with specified reading level and word count.
    
    This endpoint creates draft patient education content that:
    - Adapts to the specified reading level (elementary through professional)
    - Meets the requested word count requirements
    - Includes evidence-based sources when requested
    - Applies safety and compliance guardrails
    - Requires clinician review before use
    
    **Important**: All generated content is for draft purposes only and must be 
    reviewed and approved by qualified healthcare professionals before patient use.
    """
    
    try:
        # Run compliance checks on the request
        compliance_result = await compliance_checker.check_request(request.model_dump())
        if not compliance_result.is_compliant:
            raise HTTPException(
                status_code=400,
                detail=f"Request failed compliance check: {compliance_result.reason}"
            )
        
        # Generate the patient education content
        response = await content_generator.generate_patient_education(request)
        
        # Final compliance check on generated content
        content_compliance = await compliance_checker.check_content(response.content)
        if not content_compliance.is_compliant:
            response.metadata.safety_flags.append(content_compliance.reason)
            response.metadata.requires_review = True
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during content generation")