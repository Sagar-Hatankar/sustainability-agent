import os
import asyncio
import logging
from dotenv import load_dotenv  # IMPORTING THE LOADER

# --- 1. LOAD ENVIRONMENT VARIABLES IMMEDIATELY ---
# This forces Python to read your .env file before doing anything else.
load_dotenv()

# Check if key is loaded (for debugging)
if not os.getenv("GOOGLE_API_KEY"):
    # Try to warn the user but don't crash yet, let the main check handle it
    print("⚠️ Warning: .env file loaded, but GOOGLE_API_KEY seems missing or empty.")

# Standard ADK imports
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# --- 2. Define Researcher Sub-Agents ---

researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in energy.
    Research the latest advancements in 'renewable energy sources'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.""",
    description="Researches renewable energy sources.",
    tools=[google_search],
    output_key="renewable_energy_result"
)

researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in transportation.
    Research the latest developments in 'electric vehicle technology'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.""",
    description="Researches electric vehicle technology.",
    tools=[google_search],
    output_key="ev_technology_result"
)

researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in climate solutions.
    Research the current state of 'carbon capture methods'.
    Use the Google Search tool provided.
    Summarize your key findings concisely (1-2 sentences).
    Output *only* the summary.""",
    description="Researches carbon capture methods.",
    tools=[google_search],
    output_key="carbon_capture_result"
)

# --- 3. Define Orchestrators ---

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
    description="Runs multiple research agents in parallel."
)

merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=GEMINI_MODEL,
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.
    
    **Input Summaries:**
    * Renewable Energy: {renewable_energy_result}
    * Electric Vehicles: {ev_technology_result}
    * Carbon Capture: {carbon_capture_result}

    **Output Format:**
    ## Summary of Recent Sustainable Technology Advancements
    
    ### Renewable Energy Findings
    [Synthesize findings]
    
    ### Electric Vehicle Findings
    [Synthesize findings]
    
    ### Carbon Capture Findings
    [Synthesize findings]
    
    ### Overall Conclusion
    [1-2 sentence conclusion]
    
    Output *only* the structured report.
    """,
    description="Synthesizes research findings.",
)

# The Main Pipeline
sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    sub_agents=[parallel_research_agent, merger_agent],
    description="Coordinates parallel research and synthesizes the results."
)

# --- 4. Execution Logic (The 'Runner') ---

async def run_agent_workflow(user_request: str):
    """
    Sets up the runner and executes the workflow for a single user request.
    """
    session_service = InMemorySessionService()
    
    runner = Runner(
        agent=sequential_pipeline_agent,
        app_name="Sustainability_Research_Bot",
        session_service=session_service
    )

    import uuid
    session_id = str(uuid.uuid4())
    user_id = "demo_user"

    print(f"--- Starting Session: {session_id} ---")

    await session_service.create_session(
        app_name="Sustainability_Research_Bot",
        user_id=user_id,
        session_id=session_id
    )

    response_stream = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=user_request)]
        )
    )

    final_output = ""
    async for event in response_stream:
        if event.content and event.content.parts:
            # Simple loading indicator
            print(".", end="", flush=True) 
            if event.is_final_response():
                final_output = event.content.parts[0].text
    
    return final_output

# --- 5. Main Entry Point (CLI) ---

if __name__ == "__main__":
    # Now that we called load_dotenv() at the top, this check should PASS.
    if "GOOGLE_API_KEY" not in os.environ:
        print("\n❌ Error: GOOGLE_API_KEY still not found.")
        print("👉 Double check that your file is named exactly '.env' (no .txt extension!)")
        print("👉 Check that the content inside is: GOOGLE_API_KEY=AIzaSy...")
    else:
        try:
            print("✅ API Key found. Starting Agent...")
            user_input = "Generate the sustainability report."
            result = asyncio.run(run_agent_workflow(user_input))
            print("\n" + "="*40)
            print("FINAL REPORT")
            print("="*40 + "\n")
            print(result)
        except Exception as e:
            logger.error(f"Workflow failed: {e}")