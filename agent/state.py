from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class State:
    job_description: str = ""
    uploaded_resumes: List[Dict[str, Any]] = field(default_factory=list)
    extracted_texts: Dict[str, str] = field(default_factory=dict)
    retrieved_documents: Dict[str, List[str]] = field(default_factory=dict)
    candidate_profiles: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    matching_scores: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    ranking: List[str] = field(default_factory=list)
    interview_questions: Dict[str, List[str]] = field(default_factory=dict)
