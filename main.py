import streamlit as st
import requests

# Constants for the AIMLAPI
BASE_URL = "https://api.aimlapi.com/v1"  # Ensure this is the correct endpoint for AIMLAPI

# User input for the API key
api_key = st.text_input("Enter your AIMLAPI API key:", type="password")

def generate_gui_code(prompt, framework):
    headers = {
        "Authorization": f"Bearer {api_key}"  # Use Bearer token for authentication
    }
    payload = {
        "prompt": f"Generate a {framework} GUI application code based on the following prompt: {prompt}",
        "temperature": 0.7,
        "max_tokens": 512,
    }

    # Make the API call to AIMLAPI
    response = requests.post(f"{BASE_URL}/generate", json=payload, headers=headers)

    # Check for successful response
    if response.status_code == 200:
        return response.json().get("data", {}).get("text", "No code generated.")
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.title("PyGUI Generator 🐍")

    prompt = st.text_area("Describe the GUI you want to create:")
    frameworks = ["Tkinter", "CustomTkinter", "PyQt6", "wxPython", "Kivy"]
    selected_framework = st.selectbox("Choose a GUI framework:", frameworks)

    if st.button("Generate Code"):
        if prompt and api_key:
            with st.spinner("Generating code..."):
                code = generate_gui_code(prompt, selected_framework)
                st.success("Code generated successfully!")

                # Display the generated code
                st.markdown("### Generated Code:")
                st.markdown("```python\n" + code + "\n```")
        else:
            st.error("Please provide both a prompt and API key.")

if __name__ == "__main__":
    main()
