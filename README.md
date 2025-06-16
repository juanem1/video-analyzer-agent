# Video Content Agent

A Python-based agent for analyzing video content using Google's Gemini API. This agent can process videos, extract insights, and generate content based on video analysis.

## Features

- Video file upload and processing using Gemini API
- Content generation based on video analysis
- Timecode extraction and management
- Caching system for uploaded files
- Integration with Google's Gemini 2.0 Flash Lite model

## Prerequisites

- Python 3.8+
- Google API Key (set as GOOGLE_API_KEY environment variable)
- ADK (Agent Development Kit) installed

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/juanem1/video-analyzer-agent.git
   cd video-analyzer-agent
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Google API Key:
   Add `.env` file with:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=<your_api_key>
   ```
   or:
   ```bash
   export GOOGLE_API_KEY='your-api-key-here'
   ```

## Usage

Run the video content agent using ADK:
```bash
adk run video_content_agent
```

The agent provides the following tools:
- `upload_file_tool`: Uploads and processes video files
- `generate_content_tool`: Generates content based on video analysis
- `set_timecodes`: Manages video timecodes

## Project Structure

- `video_content_agent/`: Main package directory
  - `agent.py`: Core agent implementation
  - `prompts.py`: Agent prompts and instructions
  - `tools/`: Tool implementations for video processing
- `requirements.txt`: Project dependencies

