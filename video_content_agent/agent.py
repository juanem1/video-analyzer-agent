from google.adk.agents import Agent
from . import prompts
from .tools.tools import (
    upload_file_tool,
    generate_content_tool,
    set_timecodes,
)

root_agent = Agent(
    name="video_content_agent",
    model="gemini-2.0-flash-lite",
    description=prompts.ROOT_PROMPT,
    instruction=prompts.INSTRUCTIONS,
    tools=[upload_file_tool, generate_content_tool, set_timecodes],
)
