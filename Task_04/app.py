import streamlit as st
import asyncio
import json
import os
from agent import study_agent
from agents import Runner # Import Runner for agent execution

st.set_page_config(layout="wide")
st.title("📚 PDF Study Notes Summarizer & Quiz Generator")

# Initialize session state variables
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "results" not in st.session_state:
    st.session_state.results = {}
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# Function to run agent tasks
async def run_agent_task(agent, prompt):
    # For general agent conversation
    result = await Runner.run(agent, prompt)
    return result.final_output

# A) PDF Upload Section
st.header("1. Upload your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Save uploaded file to a temporary location
    file_path = os.path.join("./", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"Uploaded {uploaded_file.name}")

    if st.button("Extract and Summarize"):
        with st.spinner("Extracting text and generating summary..."):
            # Reset all states
            st.session_state.summary = ""
            st.session_state.quiz = []
            st.session_state.user_answers = {}
            st.session_state.results = {}
            st.session_state.pdf_text = ""

            # Extract text
            extract_result = asyncio.run(run_agent_task(study_agent, f"Extract text from: {file_path}",))
            raw_text = extract_result

            if "Error" in raw_text:
                st.error(f"Error extracting text: {raw_text}")
            else:
                st.session_state.pdf_text = raw_text
                # Clean text
                clean_result = asyncio.run(run_agent_task(study_agent, f"Clean the following text: {raw_text}"))
                cleaned_text = clean_result

                # Generate summary
                summary_prompt = f"Summarize the following text:\n\n{cleaned_text}"
                summary = asyncio.run(run_agent_task(study_agent, summary_prompt))
                st.session_state.summary = summary
                
                # Clean up the temporary file
                os.remove(file_path)
                st.rerun() # Rerun to display summary cleanly and avoid re-executing button logic

# Display summary
if st.session_state.summary:
    st.subheader("Summary")
    st.write(st.session_state.summary)

# B) Quiz Generation Section
st.header("2. Generate Quiz")
if st.session_state.pdf_text and st.button("Generate Quiz"):
    with st.spinner("Generating quiz questions..."):
        # Reset previous quiz states
        st.session_state.quiz = []
        st.session_state.user_answers = {}
        st.session_state.results = {}
        
        quiz_prompt = (
            f"Generate 5 multiple-choice questions (MCQs) from the following text. "
            f"Each MCQ must contain: 'question', 'options' (with keys A, B, C, D), and 'correct_answer' (A, B, C, or D). "
            f"Provide the output as a JSON array of objects. Do not invent content. "
            f"Text:\n\n{st.session_state.pdf_text}"
        )
        
        quiz_json_string = asyncio.run(run_agent_task(study_agent, quiz_prompt))
        
        try:
            # The agent might return additional text, so we need to extract the JSON part
            json_start = quiz_json_string.find("[")
            json_end = quiz_json_string.rfind("]") + 1
            if json_start != -1 and json_end != -1:
                quiz_json_string = quiz_json_string[json_start:json_end]
            
            quiz_data = json.loads(quiz_json_string)
            st.session_state.quiz = quiz_data
            st.rerun() # Rerun to display quiz form
            
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse quiz JSON. Please try generating the quiz again. Error: {e}")
            st.text_area("Raw quiz output from agent (for debugging):", quiz_json_string)
        except KeyError as e:
            st.error(f"Quiz data is missing a required key: {e}. Please try generating the quiz again.")
            st.text_area("Raw quiz output from agent (for debugging):", quiz_json_string)


# C) Display Quiz and Handle Answers
if st.session_state.quiz:
    st.subheader("Quiz Questions")
    
    with st.form(key='quiz_form'):
        user_selections = {}
        for i, q in enumerate(st.session_state.quiz):
            st.write(f"**Q{i+1}: {q['question']}**")
            options = [f"{key}. {value}" for key, value in q["options"].items()]
            user_selections[f"q{i}"] = st.radio(
                "Select your answer",
                options,
                key=f"quiz_radio_{i}",
                index=None # No option selected by default
            )
        
        submitted = st.form_submit_button("Check Answers")
        if submitted:
            st.session_state.user_answers = user_selections
            correct_count = 0
            total_questions = len(st.session_state.quiz)
            results_data = {}

            for i, q in enumerate(st.session_state.quiz):
                question_key = f"q{i}"
                selected_option = st.session_state.user_answers.get(question_key)
                
                user_answer_letter = selected_option[0] if selected_option else None

                is_correct = (user_answer_letter == q["correct_answer"])
                results_data[question_key] = {
                    "question": q["question"],
                    "selected": selected_option,
                    "correct_answer": f"{q['correct_answer']}. {q['options'][q['correct_answer']]}",
                    "is_correct": is_correct
                }
                if is_correct:
                    correct_count += 1
            
            st.session_state.results = {
                "data": results_data,
                "score": f"{correct_count} / {total_questions}"
            }
            st.rerun()

# D) Display Results
if st.session_state.results:
    st.subheader("Quiz Results")
    results_data = st.session_state.results.get("data", {})
    
    for i, q in enumerate(st.session_state.quiz):
        question_key = f"q{i}"
        result = results_data.get(question_key, {})
        
        if result:
            st.write(f"**Q{i+1}: {result.get('question')}**")
            if result.get('is_correct'):
                st.success(f"Your Answer: {result.get('selected')} - Correct!")
            else:
                st.error(f"Your Answer: {result.get('selected', 'No answer selected')} - Incorrect.")
            st.info(f"Correct Answer: {result.get('correct_answer')}")
            st.markdown("---")

    st.subheader(f"Final Score: {st.session_state.results.get('score')}")
