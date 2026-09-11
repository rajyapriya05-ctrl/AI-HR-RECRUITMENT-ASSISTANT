import streamlit as st
from tools.resume_parser import extract_text, chunk_text, EmbeddingGenerator
from rag.vector_store import VectorStore
from tools.jd_analyzer import analyze_job_description
from tools.matcher import score_candidate
from tools.interview_generator import generate_interview_questions
import os

st.set_page_config(page_title="AI HR Recruitment Assistant", layout="wide")

def main():
    st.title("AI HR Recruitment Assistant")
    st.sidebar.header("Settings")
    model = st.sidebar.text_input("Ollama model", value="qwen")
    host = st.sidebar.text_input("Ollama host (HTTP)", value="http://127.0.0.1:11434")
    storage = st.sidebar.text_input("Vector storage dir", value="./data/chroma")

    st.header("Upload Job Description")
    jd_text = st.text_area("Paste job description")
    jd_file = st.file_uploader("Or upload JD file", type=["txt","pdf","docx"]) 
    if jd_file and not jd_text:
        tmp = os.path.join("./", jd_file.name)
        with open(tmp, "wb") as f:
            f.write(jd_file.read())
        jd_text = extract_text(tmp)
        os.remove(tmp)

    st.header("Upload Resumes")
    uploaded = st.file_uploader("Upload resumes", type=["pdf","docx","txt"], accept_multiple_files=True)

    if st.button("Analyze Candidates"):
        if not jd_text or not uploaded:
            st.error("Please provide a job description and at least one resume.")
            return

        # Export chosen model and host so the shared Ollama client will use them
        if model:
            os.environ['OLLAMA_MODEL'] = model
        if host:
            os.environ['OLLAMA_HOST'] = host

        vs = VectorStore(persist_directory=storage)
        embedder = EmbeddingGenerator()

        candidates = []
        for f in uploaded:
            tmp = os.path.join("./", f.name)
            with open(tmp, "wb") as out:
                out.write(f.read())
            text = extract_text(tmp)
            os.remove(tmp)
            if not text.strip():
                st.warning(f"{f.name} could not be parsed")
                continue
            chunks = chunk_text(text)
            embs = embedder.embed_texts(chunks)
            ids = [f"{f.name}_{i}" for i in range(len(chunks))]
            metas = [{"candidate": f.name, "source": f.name} for _ in chunks]
            vs.add(ids, chunks, embs, metas)
            candidates.append(f.name)

        jd_fields = analyze_job_description(jd_text, model=model)

        results = []
        for cand in candidates:
            retrieved = vs.query_candidate(jd_text, candidate=cand, top_k=5)
            retrieved_text = "\n\n".join(retrieved)
            scored = score_candidate(cand, retrieved_text, jd_text, jd_fields, model=model)
            results.append((cand, scored, retrieved_text))

        results_sorted = sorted(results, key=lambda r: float(r[1].get("OverallMatch", 0)), reverse=True)

        st.header("Ranking")
        for cand, score, _ in results_sorted:
            st.write(cand, score.get("OverallMatch"))

        st.header("Candidate Details")
        sel = st.selectbox("Select candidate", [r[0] for r in results_sorted])
        for cand, scored, retrieved in results_sorted:
            if cand == sel:
                st.write(scored)
                st.write("Retrieved excerpts:")
                st.write(retrieved)
                if st.button("Generate Interview Questions"):
                    q = generate_interview_questions(jd_text, retrieved, model=model)
                    st.write(q)

if __name__ == '__main__':
    main()
