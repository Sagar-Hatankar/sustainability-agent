import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Import the workflow function from your agent.py file
from agent import run_agent_workflow

st.set_page_config(page_title="AI Research Agent", page_icon="🌍")

st.title("🌍 Sustainability Research Agent")
st.markdown("This agent performs parallel research on Energy, EVs, and Carbon Capture.")

# Input
query = st.text_input("Enter your research goal:", value="Summarize latest tech")

if st.button("Start Research"):
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("❌ GOOGLE_API_KEY not found in .env file.")
    else:
        with st.spinner("🤖 Agents are working in parallel..."):
            try:
                # Run the async workflow
                result = asyncio.run(run_agent_workflow(query))
                st.markdown("### 📝 Final Report")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")