import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Code Optimizer", page_icon="⚡", layout="wide")

st.title("⚡ AI Code Optimizer & Complexity Analyzer")
st.write(
    "Refactor code for performance, memory efficiency, and cleaner design using **Llama 3**."
)

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Groq API Key:", type="password")
    st.caption("Get a free key from [console.groq.com](https://console.groq.com)")

    model_choice = st.selectbox(
        "Select Model:",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
    )

    language = st.selectbox(
        "Programming Language:",
        ["C", "Java", "Python", "C++", "JavaScript"]
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Input Code ({language})")
    
    # Corrected: added opening triple quotes """
    default_c_code = """// Inefficient O(n^2) search
int findMax(int arr[], int n) {
    int max = arr[0];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (arr[j] > max) {
                max = arr[j];
            }
        }
    }
    return max;
}"""
    
    code_input = st.text_area("Paste code here:", value=default_c_code, height=360)
    optimize_btn = st.button("🚀 Optimize Code", type="primary")

with col2:
    st.subheader("Optimized Solution & Analysis")

    if optimize_btn:
        if not api_key:
            st.error("⚠️ Please paste your Groq API key in the sidebar.")
        elif not code_input.strip():
            st.warning("⚠️ Please provide some code to optimize.")
        else:
            with st.spinner("Analyzing complexity and optimizing..."):
                try:
                    client = Groq(api_key=api_key)

                    # Corrected prompt formatting
                    prompt = f"""You are an expert compiler and software optimization engineer.
Analyze this {language} code:

```{language.lower()}
{code_input}