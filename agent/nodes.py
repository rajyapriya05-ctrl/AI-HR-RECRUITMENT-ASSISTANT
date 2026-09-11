from typing import Dict, Any
from rag.vector_store import VectorStore
from tools.resume_parser import extract_text, chunk_text, EmbeddingGenerator
from tools.jd_analyzer import analyze_job_description
from tools.matcher import score_candidate
from tools.interview_generator import generate_interview_questions


def document_processing_node(state: Dict[str, Any]) -> Dict[str, Any]:
    files = state.get('uploaded_files', [])
    embedder = EmbeddingGenerator()
    vs = VectorStore(persist_directory=state.get('vector_dir', './data/chroma'))
    for p in files:
        text = extract_text(p)
        chunks = chunk_text(text)
        embs = embedder.embed_texts(chunks)
        ids = [f"{p}_{i}" for i in range(len(chunks))]
        metas = [{"candidate": p} for _ in chunks]
        vs.add(ids, chunks, embs, metas)
    return {'processed': True}


def rag_retrieval_node(state: Dict[str, Any]) -> Dict[str, Any]:
    vs = VectorStore(persist_directory=state.get('vector_dir', './data/chroma'))
    jd = state.get('job_description', '')
    candidates = state.get('candidates', [])
    retrieved = {}
    for c in candidates:
        docs = vs.query_candidate(jd, candidate=c, top_k=5)
        retrieved[c] = docs
    return {'retrieved_documents': retrieved}


def matching_node(state: Dict[str, Any]) -> Dict[str, Any]:
    jd = state.get('job_description', '')
    jd_fields = analyze_job_description(jd)
    scores = {}
    for c, docs in state.get('retrieved_documents', {}).items():
        text = "\n\n".join(docs)
        scores[c] = score_candidate(c, text, jd, jd_fields)
    return {'matching_scores': scores}


def ranking_node(state: Dict[str, Any]) -> Dict[str, Any]:
    scores = state.get('matching_scores', {})
    ordered = sorted(scores.items(), key=lambda kv: float(kv[1].get('OverallMatch', 0)), reverse=True)
    ranking = [k for k, _ in ordered]
    return {'ranking': ranking}


def interview_node(state: Dict[str, Any]) -> Dict[str, Any]:
    jd = state.get('job_description', '')
    iq = {}
    for c, docs in state.get('retrieved_documents', {}).items():
        text = "\n\n".join(docs)
        iq[c] = generate_interview_questions(jd, text)
    return {'interview_questions': iq}
