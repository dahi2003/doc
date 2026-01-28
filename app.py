import streamlit as st
import os
from utils.extract_docx import extract_text_docx
from utils.extract_pdf import extract_text_pdf
from utils.extract_pptx import extract_text_pptx
from utils.extract_txt import extract_text_txt
from summarizer.summarizer import summarize_text

# Page configuration
st.set_page_config(
    page_title="Document Summarizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 1.2rem;
        }
        .success-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .info-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📄 Document Summarizer Bot")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    max_length = st.slider("Summary Length", min_value=50, max_value=500, value=150, step=10)
    st.markdown("---")
    st.info("Supported formats:\n- 📄 .txt\n- 📑 .pdf\n- 📊 .pptx\n- 📋 .docx")

# Main content
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📤 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose a file to summarize",
        type=["txt", "pdf", "pptx", "docx"],
        help="Upload any supported document format"
    )

with col2:
    st.subheader("📝 Or Select Sample")
    sample_files = []
    if os.path.exists("samples"):
        sample_files = [f for f in os.listdir("samples") if os.path.isfile(os.path.join("samples", f))]
    
    if sample_files:
        selected_sample = st.selectbox("Choose a sample file", ["None"] + sample_files)
    else:
        selected_sample = "None"

st.markdown("---")

def get_text_from_file(path):
    """Extract text from various file formats"""
    if path.endswith(".docx"):
        return extract_text_docx(path)
    elif path.endswith(".pdf"):
        return extract_text_pdf(path)
    elif path.endswith(".pptx"):
        return extract_text_pptx(path)
    elif path.endswith(".txt"):
        return extract_text_txt(path)
    else:
        raise ValueError("Unsupported file format")

# Process uploaded file or sample
file_to_process = None
file_name = None

if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    file_to_process = temp_path
    file_name = uploaded_file.name
elif selected_sample != "None":
    file_to_process = os.path.join("samples", selected_sample)
    file_name = selected_sample

if file_to_process:
    try:
        with st.spinner("🔄 Processing document..."):
            # Extract text
            extracted_text = get_text_from_file(file_to_process)
            
            # Summarize
            summary = summarize_text(extracted_text, max_len=max_length)
        
        st.success("✅ Processing complete!")
        
        # Display results in tabs
        tab1, tab2, tab3 = st.tabs(["📋 Summary", "📄 Full Text", "📊 Statistics"])
        
        with tab1:
            st.markdown("### Document Summary")
            st.markdown(f"""
                <div class="success-box">
                    {summary}
                </div>
            """, unsafe_allow_html=True)
            
            # Copy to clipboard button
            col1, col2 = st.columns([3, 1])
            with col2:
                st.button("📋 Copy Summary", use_container_width=True)
        
        with tab2:
            st.markdown("### Full Text")
            with st.expander("Click to expand full text", expanded=False):
                st.text_area("Extracted Text", extracted_text, height=300, disabled=True)
        
        with tab3:
            st.markdown("### Document Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Words", len(extracted_text.split()))
            with col2:
                st.metric("Total Characters", len(extracted_text))
            with col3:
                st.metric("Summary Words", len(summary.split()))
            with col4:
                compression_ratio = (len(extracted_text) / len(summary)) if summary else 0
                st.metric("Compression Ratio", f"{compression_ratio:.1f}x")
        
        # Clean up temp file
        if uploaded_file is not None and os.path.exists(file_to_process):
            os.remove(file_to_process)
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload a document or select a sample file to get started!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Made for document summarization</p>",
    unsafe_allow_html=True
)
