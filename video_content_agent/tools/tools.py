import os
import json
import time
from google.genai import Client, types
from google.genai.types import Part

# Initialize Gemini Client
client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# Cache for file uploads
CACHE_FILE = ".upload_cache.json"


def load_upload_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_upload_cache(cache: dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def set_timecodes(timecodes: list[dict]) -> list[dict]:
    """
    Handler for 'set_timecodes'. Returns the provided timecodes.
    """
    return timecodes


def upload_file_tool(file_path: str, display_name: str = "video.mp4") -> dict:
    """
    Uploads a video file to the Gemini API and waits for processing to complete.
    Caches uploads based on file_path.

    Args:
        file_path (str): The local path to the video file.
        display_name (str): Name to display in Gemini.

    Returns:
        dict: A dictionary containing the 'uri' and 'mimeType' of the uploaded file.
              Example: {"uri": "files/...", "mimeType": "video/mp4"}
    
    Raises:
        RuntimeError: If the file upload fails or processing fails.
        FileNotFoundError: If the file_path does not exist.
    """
    cache = load_upload_cache()
    if file_path in cache:
        print(f"🗄 Using cached file for {file_path}")
        return cache[file_path]

    print(f"📤 Reading file for upload: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ Error: The file {file_path} does not exist.")
        raise

    print(f"📤 Uploading {file_path} to Gemini as {display_name}...")
    uploaded_file = client.files.upload(
        file=file_path,
        config={"displayName": display_name}
    )

    get_file = client.files.get(name=uploaded_file.name)
    while get_file.state.name == "PROCESSING":
        print(f"Current file status for {uploaded_file.name}: {get_file.state.name}")
        print("File is still processing, retrying in 5 seconds")
        time.sleep(5)
        get_file = client.files.get(name=uploaded_file.name)

    if get_file.state.name == "FAILED":
        print(f"❌ File processing failed for {uploaded_file.name}: {get_file.state}")
        raise RuntimeError(f"File processing failed for {uploaded_file.name}. State: {get_file.state.name}")

    print(f"✅ File {file_path} uploaded successfully as {uploaded_file.name}")
    
    file_info = {
        "uri": get_file.uri,
        "mimeType": get_file.mime_type,
    }
    cache[file_path] = file_info
    save_upload_cache(cache)

    return file_info


def generate_content_tool(text: str, file_info: dict) -> str | list[dict]:
    """
    Generates content using the Gemini API based on text and an optional file.
    Can handle a function call to 'set_timecodes'.

    Args:
        text (str): Text prompt.
        file_info (dict): Dictionary with 'uri' and 'mimeType' keys for a file.
                          Example: {"uri": "files/...", "mimeType": "video/mp4"}

    Returns:
        str | list[dict]: API response (text or the result of set_timecodes function).
    
    Raises:
        ValueError: If an unexpected function call is received from the API.
    """
    contents = [text]
    if file_info and file_info.get('uri') and file_info.get('mimeType'):
        part = Part.from_uri(file_uri=file_info['uri'], mime_type=file_info['mimeType'])
        contents.append(part)

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.5,
            tools=[set_timecodes],
        ),
    )

    # Process possible function call
    if response.function_calls:
        for call in response.function_calls:
            if call.name == "set_timecodes":
                # Assuming set_timecodes returns list[dict] as per common usage
                return set_timecodes(call.args["timecodes"]) 
            else:
                raise ValueError(f"Unexpected function call: {call.name}")
    
    return response.text or ""

