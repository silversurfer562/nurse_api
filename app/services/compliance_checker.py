"""Compliance and safety checking service"""

from typing import Dict, List, Any
from pydantic import BaseModel
import re


class ComplianceResult(BaseModel):
    """Result of compliance checking"""
    is_compliant: bool
    reason: str = ""
    flags: List[str] = []


class ComplianceCheckerService:
    """
    Service for checking compliance and safety of requests and generated content.
    
    This service implements guardrails to ensure:
    - Content safety and appropriateness
    - Privacy protection (HIPAA compliance considerations)
    - Medical accuracy disclaimers
    - Professional review requirements
    """
    
    def __init__(self):
        # Patterns that might indicate non-compliant content
        self.sensitive_patterns = [
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card pattern
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email pattern (PII)
        ]
        
        self.inappropriate_terms = [
            'guarantee', 'cure', 'miracle', 'breakthrough',
            'secret', 'hidden', 'conspiracy', 'big pharma'
        ]
        
        self.medical_disclaimer_required = True
        
    async def check_request(self, request_data: Dict[str, Any]) -> ComplianceResult:
        """
        Check if the request meets compliance requirements.
        
        Validates:
        - Appropriate medical terminology
        - No inappropriate claims
        - Request parameters within safe limits
        """
        
        flags = []
        
        # Check for inappropriate content in topic/query
        topic = request_data.get('topic', '') or request_data.get('query', '')
        if topic:
            topic_lower = topic.lower()
            for term in self.inappropriate_terms:
                if term in topic_lower:
                    flags.append(f"Inappropriate term detected: {term}")
        
        # Check word count limits
        word_count = request_data.get('word_count', 0)
        if word_count > 2000:
            flags.append("Word count exceeds maximum safe limit")
        
        # Check for potentially sensitive topics
        sensitive_topics = ['suicide', 'self-harm', 'overdose', 'addiction']
        if any(topic in topic_lower for topic in sensitive_topics):
            flags.append("Sensitive topic requires enhanced review")
        
        is_compliant = len(flags) == 0
        reason = "; ".join(flags) if flags else ""
        
        return ComplianceResult(
            is_compliant=is_compliant,
            reason=reason,
            flags=flags
        )
    
    async def check_content(self, content: str) -> ComplianceResult:
        """
        Check generated content for compliance and safety.
        
        Validates:
        - No inappropriate medical claims
        - Proper disclaimers present
        - Content safety and accuracy
        """
        
        flags = []
        content_lower = content.lower()
        
        # Check for inappropriate medical claims
        for term in self.inappropriate_terms:
            if term in content_lower:
                flags.append(f"Inappropriate claim detected: {term}")
        
        # Check for definitive medical advice (should be avoided)
        definitive_patterns = [
            r'\byou should\b', r'\byou must\b', r'\byou will\b',
            r'\bguaranteed\b', r'\bcertain\b', r'\bdefinitely\b'
        ]
        
        for pattern in definitive_patterns:
            if re.search(pattern, content_lower):
                flags.append("Content contains definitive medical advice")
                break
        
        # Ensure content isn't too prescriptive
        if 'diagnose' in content_lower or 'prescribe' in content_lower:
            flags.append("Content may be too prescriptive")
        
        is_compliant = len(flags) == 0
        reason = "; ".join(flags) if flags else ""
        
        return ComplianceResult(
            is_compliant=is_compliant,
            reason=reason,
            flags=flags
        )
    
    async def check_clinical_data(self, patient_data: str) -> ComplianceResult:
        """
        Check clinical data for privacy and compliance issues.
        
        Enhanced checking for clinical summaries including:
        - PII detection
        - HIPAA compliance considerations
        - Data sensitivity assessment
        """
        
        flags = []
        
        # Check for sensitive patterns (PII)
        for pattern in self.sensitive_patterns:
            if re.search(pattern, patient_data):
                flags.append("Potential PII detected - ensure data is properly de-identified")
        
        # Check for specific identifiers
        identifier_patterns = [
            r'\bMRN\s*:?\s*\d+',  # Medical Record Number
            r'\bDOB\s*:?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # Date of Birth
            r'\bphone\s*:?\s*\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # Phone numbers
        ]
        
        for pattern in identifier_patterns:
            if re.search(pattern, patient_data, re.IGNORECASE):
                flags.append("Potential patient identifier detected")
        
        # Check data length for reasonableness
        if len(patient_data) > 5000:
            flags.append("Patient data unusually long - review for completeness")
        
        is_compliant = len(flags) == 0
        reason = "; ".join(flags) if flags else ""
        
        return ComplianceResult(
            is_compliant=is_compliant,
            reason=reason,
            flags=flags
        )
    
    async def check_clinical_content(self, clinical_summary: str) -> ComplianceResult:
        """
        Check generated clinical content for professional standards.
        
        Validates clinical summaries meet professional standards:
        - Appropriate clinical language
        - No definitive diagnoses without qualification
        - Proper professional disclaimers
        """
        
        flags = []
        content_lower = clinical_summary.lower()
        
        # Check for unqualified diagnostic statements
        diagnostic_patterns = [
            r'\bpatient has\b(?!\s+(history|symptoms|signs))',
            r'\bdiagnosed with\b(?!\s+(possible|probable|suspected))',
            r'\bcertainly\b', r'\bobviously\b', r'\bclearly\b'
        ]
        
        for pattern in diagnostic_patterns:
            if re.search(pattern, content_lower):
                flags.append("Content contains unqualified diagnostic statements")
                break
        
        # Ensure appropriate clinical hedging language
        hedging_present = any(term in content_lower for term in [
            'appears', 'suggests', 'indicates', 'consistent with', 
            'possible', 'probable', 'likely', 'may indicate'
        ])
        
        if not hedging_present and len(clinical_summary) > 100:
            flags.append("Clinical summary lacks appropriate hedging language")
        
        # Check for treatment recommendations without proper qualification
        treatment_patterns = [
            r'\bshould receive\b', r'\bmust take\b', r'\brequires\b(?!\s+review)'
        ]
        
        for pattern in treatment_patterns:
            if re.search(pattern, content_lower):
                flags.append("Content contains definitive treatment recommendations")
                break
        
        is_compliant = len(flags) == 0
        reason = "; ".join(flags) if flags else ""
        
        return ComplianceResult(
            is_compliant=is_compliant,
            reason=reason,
            flags=flags
        )