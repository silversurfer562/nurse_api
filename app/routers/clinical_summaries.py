"""Clinical summary generation endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from app.models.requests import ClinicalSummaryRequest
from app.models.responses import ClinicalSummaryResponse, ErrorResponse
from app.services.content_generator import ContentGeneratorService
from app.services.compliance_checker import ComplianceCheckerService

router = APIRouter()


def get_content_generator():
    """Dependency to get content generator service"""
    return ContentGeneratorService()


def get_compliance_checker():
    """Dependency to get compliance checker service"""
    return ComplianceCheckerService()


@router.post("/clinical-summary",
             response_model=ClinicalSummaryResponse,
             responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}})
async def generate_clinical_summary(
    request: ClinicalSummaryRequest,
    content_generator: ContentGeneratorService = Depends(get_content_generator),
    compliance_checker: ComplianceCheckerService = Depends(get_compliance_checker)
):
    """
    Generate clinical summaries from patient data with flexible word counts.
    
    This endpoint creates draft clinical summaries that:
    - Analyze provided patient data and clinical information
    - Generate summaries with flexible word count requirements
    - Identify key findings and risk factors
    - Provide clinical recommendations when requested
    - Apply strict compliance and privacy guardrails
    - Require clinical professional review before use
    
    **Important**: All generated summaries are for draft purposes only and must be 
    reviewed by qualified healthcare professionals. Clinical decisions should always 
    be based on professional judgment and direct patient assessment.
    
    **Privacy Notice**: Ensure all patient data is de-identified and complies with 
    HIPAA and other applicable privacy regulations before submission.
    """
    
    try:
        # Enhanced compliance checks for clinical data
        compliance_result = await compliance_checker.check_clinical_data(request.patient_data)
        if not compliance_result.is_compliant:
            raise HTTPException(
                status_code=400,
                detail=f"Clinical data failed compliance check: {compliance_result.reason}"
            )
        
        # Generate the clinical summary
        response = await content_generator.generate_clinical_summary(request)
        
        # Final compliance and safety check on generated summary
        content_compliance = await compliance_checker.check_clinical_content(response.summary)
        if not content_compliance.is_compliant:
            response.metadata.safety_flags.append(content_compliance.reason)
            response.metadata.requires_review = True
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error during summary generation")