import streamlit as st
from app.services.parser import parse_pdf, parse_docx
from app.services.ranking import rank_resumes

st.set_page_config(page_title="AI Resume Ranker", layout="wide")
st.title("AI Resume Ranker")

# Job description input
job_desc = st.text_area("Job Description", height=200)

# Resume upload
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF or DOCX)", 
    type=['pdf', 'docx'], 
    accept_multiple_files=True
)

if st.button("Rank Resumes"):
    if not job_desc.strip() or not uploaded_files:
        st.warning("Please provide a job description and at least one resume.")
    else:
        # Parse resumes
        resumes_text = []
        for file in uploaded_files:
            content = file.read()
            if file.name.endswith(".pdf"):
                text = parse_pdf(content)
            elif file.name.endswith(".docx"):
                text = parse_docx(content)
            else:
                continue
            resumes_text.append(text)

        with st.spinner("Ranking resumes..."):
            ranked = rank_resumes(job_desc, resumes_text, explain_top_n=3)

        # Display results
        for i, r in enumerate(ranked):
            st.markdown(f"### Candidate {i+1}: **Score {r['final_score']:.3f}**")
            st.markdown(
                f"""
            **Semantic Score:** {r['semantic_score']:.3f}  
            **Skill Score:** {r['skill_score']:.3f}  
            **Keyword Score:** {r['keyword_score']:.3f}
            """
            )
            if r['reasoning']:
                st.markdown(f"**Reasoning:** {r['reasoning']}")
            st.markdown("---")