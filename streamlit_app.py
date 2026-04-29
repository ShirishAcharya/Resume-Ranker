import streamlit as st
from app.services.parser import parse_pdf, parse_docx
from app.services.ranking import rank_resumes

st.set_page_config(page_title="Resume Ranker", layout="wide")
st.title("Resume Ranker")

job_desc = st.text_area("Job Description", height=200)
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF or DOCX)",
    type=['pdf', 'docx'],
    accept_multiple_files=True
)

if st.button("Rank Resumes"):
    if not job_desc.strip() or not uploaded_files:
        st.warning("Please provide a job description and at least one resume.")
    else:
        resumes = []
        for file in uploaded_files:
            content = file.read()
            if file.name.endswith(".pdf"):
                name, text = parse_pdf(content)
            elif file.name.endswith(".docx"):
                name, text = parse_docx(content)
            else:
                continue
            resumes.append((name, text))

        with st.spinner("Ranking resumes..."):
            ranked = rank_resumes(job_desc, resumes, explain_top_n=3)

        for i, r in enumerate(ranked):
            st.markdown(f"### #{i+1} — {r['name']} &nbsp; `{r['final_score']:.3f}`")
            col1, col2, col3 = st.columns(3)
            col1.metric("Semantic", f"{r['semantic_score']:.3f}")
            col2.metric("Skill Match", f"{r['skill_score']:.3f}")
            col3.metric("Keyword", f"{r['keyword_score']:.3f}")

            if r.get("matched_skills"):
                st.markdown("**Matched Skills:** " + ", ".join(
                    f"`{s}`" for s in r["matched_skills"]
                ))

            if r["reasoning"]:
                with st.expander("View Reasoning"):
                    st.markdown(r["reasoning"])

            st.markdown("---")