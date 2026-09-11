from tools.ollama_client import generate
import re
import json
import logging

logger = logging.getLogger(__name__)


def analyze_job_description(jd_text: str, model: str = 'qwen') -> dict:
    prompt = f"Extract required_skills, preferred_skills, min_years_experience, education from the job description as JSON.\n\n{jd_text}\n\nReturn only JSON."
    try:
        resp = generate(prompt, model=model)
    except Exception as e:
        logger.exception("Ollama generate failed: %s", e)
        resp = ""
    try:
        m = re.search(r"\{.*\}", resp, re.S)
        if m:
            return json.loads(m.group(0))
    except Exception:
        pass
    lines = jd_text.splitlines()
    req = []
    pref = []
    years = 0
    for ln in lines:
        if 'required' in ln.lower():
            req.extend(re.findall(r"[A-Za-z+#\.\- ]{2,40}", ln))
        if 'preferred' in ln.lower():
            pref.extend(re.findall(r"[A-Za-z+#\.\- ]{2,40}", ln))
        if 'years' in ln.lower():
            nums = re.findall(r"(\d+)", ln)
            if nums:
                years = int(nums[0])
    return {'required_skills': req, 'preferred_skills': pref, 'min_years_experience': years, 'education': ''}
