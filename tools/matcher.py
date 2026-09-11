from tools.ollama_client import generate
import re, json
import logging

logger = logging.getLogger(__name__)


def simple_skill_match(skills, text):
    if not skills:
        return 0.0
    t = text.lower()
    hits = sum(1 for s in skills if s.lower() in t)
    return round(100.0 * hits / len(skills), 2)


def score_candidate(name, retrieved_text, jd_text, jd_fields, model: str = 'qwen'):
    req = jd_fields.get('required_skills', [])
    pref = jd_fields.get('preferred_skills', [])
    skills_score = simple_skill_match(req + pref, retrieved_text)

    prompt = (
        "You are an HR assistant. Given the job description and resume excerpts, produce JSON: OverallMatch (0-100), SkillsMatch, ExperienceMatch, EducationMatch, Strengths (list), Weaknesses (list), Recommendation (Strong/Neutral/Weak). ONLY use provided excerpts.\n\n"
        + jd_text[:2000] + "\n\n" + retrieved_text[:4000] + "\n\nReturn only JSON."
    )
    try:
        resp = generate(prompt, model=model)
    except Exception as e:
        logger.exception("Ollama generate failed: %s", e)
        resp = ""
    try:
        m = re.search(r"\{.*\}", resp, re.S)
        if m:
            j = json.loads(m.group(0))
            return j
    except Exception:
        pass

    overall = min(100.0, skills_score * 0.8 + 20.0)
    return {'Candidate': name, 'OverallMatch': overall, 'SkillsMatch': skills_score, 'ExperienceMatch': 0, 'EducationMatch': 0, 'Strengths': [], 'Weaknesses': [], 'Recommendation': 'Strong' if overall>70 else 'Neutral'}
