import streamlit as st
import io
import PyPDF2 # For PDF text extraction
# import docx # Uncomment and install if you want to add .docx support

# --- Helper Functions for Text Extraction ---

def extract_text_from_txt(file_content):
    """Extracts text from a .txt file."""
    try:
        return io.StringIO(file_content.getvalue().decode("utf-8")).read()
    except Exception as e:
        st.error(f"Error reading text file: {e}")
        return None

def extract_text_from_pdf(file_content):
    """
    Extracts text from a PDF file using PyPDF2.
    NOTE: This is a basic implementation. Complex PDFs (scanned, images)
    might not extract text well.
    """
    text = ""
    try:
        # Use PdfReader instead of PdfFileReader for PyPDF2 v6+
        reader = PyPDF2.PdfReader(file_content)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() if page.extract_text() else ""
        return text
    except PyPDF2.errors.PdfReadError:
        st.error("Invalid PDF file. Please upload a readable PDF.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while reading PDF: {e}")
        return None

def extract_text_from_docx(file_content):
    """
    Placeholder for .docx text extraction.
    Requires 'python-docx' library (pip install python-docx).
    """
    # from docx import Document # Uncomment if you install python-docx
    st.warning("'.docx' file extraction is complex and requires the 'python-docx' library. This is a placeholder.")
    # In a real implementation:
    # try:
    #     document = Document(file_content)
    #     full_text = []
    #     for para in document.paragraphs:
    #         full_text.append(para.text)
    #     return '\n'.join(full_text)
    # except Exception as e:
    #     st.error(f"Error reading Word document: {e}")
    return None # Return None for now as it's not fully implemented


# --- AI Summarization Placeholder ---

def summarize_text_with_ai_placeholder(
    text_content: str,
    summary_length: str = "medium",
    bullet_points: bool = False,
    focus_themes: str = ""
):
    """
    PLACEHOLDER for AI summarization.
    In a real application, you would integrate with a powerful LLM API
    (e.g., Google's Gemini API, OpenAI GPT, etc.) here.

    This function simulates summarization based on simple heuristics.
    """
    if not text_content or len(text_content.strip()) < 100:
        return (
            "Not enough content provided to generate a meaningful summary.",
            [],
            [],
            "Insufficient Content"
        )

    words = text_content.split()
    total_words = len(words)

    # Simulate summary length based on percentage of original words
    if summary_length == "short":
        summary_word_count = int(total_words * 0.15)
    elif summary_length == "medium":
        summary_word_count = int(total_words * 0.25)
    else: # detailed
        summary_word_count = int(total_words * 0.35)

    # Basic simulation of summary, focusing on the beginning and some "keywords"
    simulated_summary_intro = " ".join(words[:min(summary_word_count // 2, total_words)])
    simulated_summary_body = " ".join(words[total_words // 2 : min(total_words // 2 + summary_word_count // 2, total_words)])

    final_summary_text = f"{simulated_summary_intro.strip()}... {simulated_summary_body.strip()}."

    # Simulate key takeaways
    simulated_key_takeaways = [
        "Identified main subject based on initial text.",
        "Crucial data mentioned early in the document (simulated).",
        "Recommendations derived from the summary context (simulated)."
    ]
    if focus_themes:
        simulated_key_takeaways.append(f"Emphasized theme: '{focus_themes}' (simulated recognition).")


    # Simulate tags based on common words or predefined categories
    all_tags = ["AI", "Technology", "Software", "Development", "Data", "Analysis", "Research", "Project", "Report"]
    relevant_tags = [tag for tag in all_tags if tag.lower() in text_content.lower()][:5]
    if not relevant_tags:
        relevant_tags = ["General Document"]

    if bullet_points:
        final_summary_text = [f"- {s.strip()}" for s in final_summary_text.split("...") if s.strip()]
        if not final_summary_text: # Ensure there's at least one bullet
            final_summary_text = ["- Summarized content in bullet points (simulated)."]

    # Simulate conclusion/recommendation
    conclusion = "Based on the content provided, the primary focus seems to be on [simulated core topic]. Further analysis would require a deeper understanding of [simulated missing detail]."

    return final_summary_text, simulated_key_takeaways, relevant_tags, conclusion


# --- Streamlit Application Layout ---

st.set_page_config(page_title="AI File Summarizer", layout="wide", initial_sidebar_state="expanded")

st.title("📄 AI File Summarizer")
st.markdown("Upload your document or paste text to get a concise summary, key takeaways, and relevant tags.")

# --- Input Handling ---
st.subheader("1. Input Document")

input_method = st.radio(
    "Choose your input method:",
    ("Upload File", "Paste Text"),
    index=0
)

extracted_text = ""
file_name = "Pasted Content"

if input_method == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload your document (.txt, .pdf)",
        type=["txt", "pdf"] # Add "docx" here if you implement docx parsing
    )
    if uploaded_file is not None:
        file_name = uploaded_file.name
        with st.spinner(f"Extracting text from {file_name}..."):
            if uploaded_file.type == "text/plain":
                extracted_text = extract_text_from_txt(uploaded_file)
            elif uploaded_file.type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            # elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            #     extracted_text = extract_text_from_docx(uploaded_file)
            else:
                st.warning("Unsupported file type. Please upload a .txt or .pdf file.")

elif input_method == "Paste Text":
    extracted_text = st.text_area(
        "Paste your document content here:",
        height=300,
        placeholder="E.g., 'Chapter 1: The Quantum Realm. Quantum mechanics is a fundamental theory in physics that describes the properties of nature at the scale of atoms and subatomic particles...'"
    )
    file_name = "Pasted Content"

if extracted_text:
    st.info(f"Text loaded. Original content length: {len(extracted_text.split())} words.")
else:
    st.info("Awaiting file upload or text input...")

# --- Summarization Options ---
st.subheader("2. Summarization Options")

col1, col2 = st.columns(2)
with col1:
    summary_length = st.selectbox(
        "Select Summary Length:",
        ("short", "medium", "detailed"),
        index=1,
        help="Short (~15% of original), Medium (~25%), Detailed (~35%)"
    )
with col2:
    bullet_points = st.checkbox(
        "Generate Bullet-Point Summary?",
        value=False,
        help="Summarize content in bullet points instead of paragraphs."
    )

focus_themes = st.text_input(
    "Optional: Emphasize themes or points (comma-separated):",
    placeholder="E.g., 'impact on environment, future projections'"
)

# --- Generate Summary Button ---
if st.button("Generate Summary", type="primary", use_container_width=True):
    if extracted_text:
        with st.spinner("Generating summary... This might take a moment if using a real AI model."):
            summary, key_takeaways, tags, conclusion = summarize_text_with_ai_placeholder(
                extracted_text,
                summary_length,
                bullet_points,
                focus_themes
            )

            st.subheader("3. Summary Results")
            st.markdown(f"### Summary for: *{file_name}*")

            if isinstance(summary, list): # If bullet points were requested
                for item in summary:
                    st.write(item)
            else:
                st.write(summary)

            st.markdown("---")
            st.subheader("Key Takeaways:")
            for i, takeaway in enumerate(key_takeaways):
                st.write(f"- {takeaway}")

            st.markdown("---")
            st.subheader("Important Conclusions and Recommendations:")
            st.write(conclusion)

            st.markdown("---")
            st.subheader("Relevant Tags:")
            st.markdown(f"**{', '.join(tags)}**")

            st.success("Summary generated successfully!")
    else:
        st.warning("Please upload a file or paste content to summarize.")


# --- User Feedback Mechanism ---
st.subheader("4. Provide Feedback & Request Revisions")
st.info("Your feedback helps us improve the summarization quality!")

feedback_text = st.text_area(
    "Enter your feedback or revision requests here:",
    placeholder="e.g., 'The summary missed the section on economic impact. Please revise to include it.'",
    height=100
)

if st.button("Submit Feedback", use_container_width=True):
    if feedback_text:
        # In a real app, this feedback would be sent to a database or logging system
        st.success("Thank you for your feedback! Your input is valuable for continuous improvement.")
        # You would typically clear the feedback_text area after submission
        # st.session_state.feedback_text = "" # Requires state management
    else:
        st.warning("Please enter some feedback before submitting.")


# --- Example Outputs (Simulated) ---
st.sidebar.subheader("Example Outputs")
st.sidebar.markdown(
    """
This section demonstrates how a summary *would* look.
To truly test, upload a text file or paste content.
"""
)

# --- Disclaimer ---
st.markdown("""
---
**Disclaimer:**
This application is a conceptual framework. The core AI summarization logic
in `summarize_text_with_ai_placeholder` is simulated for demonstration.
For actual high-quality summarization, integration with a powerful Large Language Model
(like Google's Gemini API) is required. File parsing for complex PDFs and Word documents
also requires robust external libraries or services.
""")

# Instructions to run:
# 1. Save this code as `summarizer_app.py`
# 2. Open your terminal or command prompt.
# 3. Navigate to the directory where you saved the file.
# 4. Install Streamlit and PyPDF2: `pip install streamlit PyPDF2`
# 5. Run the app: `streamlit run summarizer_app.py`