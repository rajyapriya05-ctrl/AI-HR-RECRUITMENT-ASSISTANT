from tools.ollama_client import generate
import logging

logger = logging.getLogger(__name__)


def generate_interview_questions(jd_text: str, resume_excerpt: str, model: str = 'qwen') -> str:
    prompt = (
        "Generate 7 interview questions (technical, behavioral, situational) tailored to the job description and the candidate resume excerpts below. Label each question with its type. ONLY use the provided facts.\n\n"
        + jd_text + "\n\n" + resume_excerpt
    )
    try:
        return generate(prompt, model=model)
    except Exception as e:
        logger.exception("Interview generation failed: %s", e)
        return "Interview generation error: " + str(e)
