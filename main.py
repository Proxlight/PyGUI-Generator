import streamlit as st
import openai

# Constants
BASE_URL = "https://api.aimlapi.com/v1"  # Adjust base URL as needed

# User input for the API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Initialize OpenAI only if API key is provided
api = None
if api_key:
    api = OpenAI(api_key=api_key, base_url=BASE_URL)

def generate_gui_code(prompt, framework):
    # Prepare the request to OpenAI
    response = api.chat.completions.create(
        model="gpt-3.5-turbo",  # or use your desired model
        messages=[{
            "role": "system",
            "content": "You are an assistant that generates GUI code."
        }, {
            "role": "user",
            "content": f"Generate a {framework} GUI application code based on the following prompt: {prompt}"
        }],
        temperature=0.7,
        max_tokens=512,
    )
    return response.choices[0].message.content

def main():
    st.title("PyGUI Generator 🐍")

    # User input for the prompt
    prompt = st.text_area("Describe the GUI you want to create:")

    # Dropdown for framework selection
    frameworks = [
        "Tkinter", "CustomTkinter", "PyQt6", "wxPython", "Kivy", "Flask",
        "Dash", "GTK", "Pygame"
    ]
    selected_framework = st.selectbox("Choose a GUI framework:", frameworks)

    # Button to generate code
    if st.button("Generate Code"):
        if prompt and api:
            with st.spinner("Generating code..."):
                try:
                    code = generate_gui_code(prompt, selected_framework)
                    st.success("Code generated successfully!")

                    # Display the generated code in markdown format
                    st.markdown("### Generated Code:")
                    st.markdown("```python\n" + code + "\n```")  # Display code in a markdown block

                    # Create a download button for the generated code
                    code_filename = "generated_gui_app.py"
                    with open(code_filename, "w") as code_file:
                        code_file.write(code)
                    with open(code_filename, "rb") as code_file:
                        st.download_button(
                            label="Download Python Code",
                            data=code_file,
                            file_name=code_filename,
                            mime="application/octet-stream",
                        )
                except Exception as e:
                    st.error(f"Error generating code: {e}")
        else:
            if not api:
                st.error("Please enter a valid OpenAI API key.")
            else:
                st.error("Please enter a prompt.")

if __name__ == "__main__":
    main()
