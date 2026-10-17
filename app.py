import streamlit as st
from groq import Groq

# Configure page settings
st.set_page_config(page_title="Campus Academic Companion", layout="wide")

st.title("Campus Academic Companion")
st.write("Analyze, optimize, and improve your code using Groq LLM.")

# Sidebar for API Configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Groq API Key:", type="password")

# Input field for user code
code_input = st.text_area("Enter your code here:", height=250, placeholder="// Paste your code here...")

# Button to trigger optimization
if st.button("Optimize Code"):
    if not api_key:
        st.error("⚠️ Please paste your Groq API key in the sidebar.")
    elif not code_input.strip():
        st.warning("⚠️ Please provide some code to optimize.")
    else:
        with st.spinner("Analyzing complexity and optimizing..."):
            try:
                client = Groq(api_key=api_key)

                prompt = f"""You are an expert compiler and software optimization engineer.
Analyze the input code:
{code_input}

Suggest performance improvements, optimize it, and output the clean, improved code with explanations."""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                st.subheader("Optimization Results")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"An error occurred: {e}")