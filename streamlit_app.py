from dotenv import load_dotenv
import os
import anthropic
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Verify API key
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

def get_response(learning_targets):
    """Send user input to the AI model and get a response using the Messages API."""
    client = anthropic.Anthropic(api_key=api_key)  # Pass the API key
    
    # Constructing the refined prompt
    user_content = f"""
    ##CONTEXT##
    I'm developing clear learning goals and structured section narratives from provided learning targets.
    
    ##OBJECTIVE##
    1. **Learning Goals Generation**
       - Analyze all learning targets to identify:
         - Core skills being developed
         - Major concepts being taught
         - Expected final outcomes
         - Progression of complexity
       - Synthesize 2-3 broad goals that:
         - Start with action verbs
         - Encompass multiple targets
         - Focus on major outcomes
         - Are measurable
       - Format under the heading "**Learning Goals**" as bullet points.
    
    2. **Section Narrative Generation**
       - Follow a structured four-paragraph format under the heading "**Section Narrative**":
         
         **Paragraph 1: Introduction**
         - Begin with "In this section, students..."
         - Introduce the main concept/skill
         - Describe the starting point
         - Reference initial tools or approaches
         
         **Paragraph 2: Early Development**
         - Describe how students begin working with the concept
         - Explain initial strategies or representations
         - Show progression to slightly more complex ideas
         - Connect to specific mathematical notation or vocabulary
         
         **Paragraph 3: Continued Development**
         - Begin with "Throughout the section..."
         - Describe how students expand their understanding
         - Include key connections or relationships
         - Reference specific mathematical practices or skills
         
         **Paragraph 4: Advanced Application**
         - Begin with "As students become more confident..."
         - Describe culminating work
         - Show how skills come together
         - Reference any real-world connections or extensions
         
    3. **Style and Formatting Guidelines**
       - Use present tense, third-person narration
       - Avoid technical jargon unless necessary
       - Use clear transitional phrases
       - No teacher guidance, bullet points, or special formatting except bold titles
    
    ##INPUT##
    Learning Targets:
    {learning_targets}
    
    ##SAMPLE OUTPUT FORMAT##
    **Learning Goals**
    * [First broad learning goal]
    * [Second broad learning goal]
    
    **Section Narrative**
    In this section, students...
    [Four structured paragraphs following the defined format]
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that generates structured learning goals and section narratives for lesson planning.",
        messages=[
            {"role": "user", "content": user_content}
        ],
        max_tokens=1000,
        stream=False
    )
    
    return response.content[0].text

# Streamlit app UI
st.title("Learning Goal and Narrative Generator")
st.subheader("Generate structured learning goals and section narratives from learning targets.")

# Text input for learning targets
learning_targets = st.text_area("Enter the learning targets:")

# Generate response
if st.button("Generate Content"):
    if learning_targets:
        with st.spinner("Generating learning goals and section narrative..."):
            try:
                response = get_response(learning_targets)
                st.success("Output Generated Successfully!")
                st.text_area("Generated Output", value=response, height=600)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter learning targets to process.")
