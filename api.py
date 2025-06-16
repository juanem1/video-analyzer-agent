"""
Functions upload_file and generate_content to interact with the Gemini API.
"""
import os
import time
import json
from types import SimpleNamespace
from google.genai import Client
from google.genai.types import Part
from google.genai import types
from functions import set_timecodes

CACHE_FILE = ".upload_cache.json"

SYSTEM_INSTRUCTION = (
    "When given a video and a query, call the relevant "
    "function only once with the appropriate timecodes and text for the video"
)

client = Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def load_upload_cache() -> dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_upload_cache(cache: dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def generate_content(text: str, file: dict) -> str:
    """
    Generates content using the Gemini API.

    :param text: Text prompt.
    :param file: Dictionary with 'uri' and 'mimeType' keys.
    :return: API response (text or result of the set_timecodes function).
    """
    contents = [text]
    if file.uri and file.mime_type:
        part = Part.from_uri(file_uri=file.uri, mime_type=file.mime_type)
        contents.append(part)

    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.5,
            tools=[set_timecodes],
        ),
    )

    # print(response)

    # Process possible function call
    call = next(iter(response.function_calls or []), None)
    if call is None:
        return response.text or ""

    if call.name == "set_timecodes":
        return set_timecodes(call.args["timecodes"])

    raise ValueError(f"Invalid function call: {call.name}")


def upload_file(file_data: bytes, display_name: str = "video.mp4") -> dict:
    """
    Uploads a video file to the Gemini API and waits for processing to complete.

    :param file_data: Bytes of the video file.
    :param display_name: Name to display in Gemini.
    :return: Dictionary with final file information.
    """
    cache = load_upload_cache()
    if file_data in cache:
        print("🗄 Using cached file istead of uploading")
        return SimpleNamespace(uri=cache[file_data]["uri"], mime_type=cache[file_data]["mimeType"])


    print("📤 Uploading to Gemini...")
    uploaded = client.files.upload(
        file=file_data,
        config={"displayName": display_name}
    )

    get_file = client.files.get(name=uploaded.name)
    while get_file.state == "PROCESSING":
        print(f"Current file status: {get_file.state}")
        print("File is still processing, retrying in 5 seconds")
        time.sleep(5)
        get_file = client.files.get(name=uploaded.name)

    state = get_file.state
    if state == "FAILED":
        raise RuntimeError("File processing failed.")

    print("File upload successfully")

    file_info = {
        "uri": get_file.uri,
        "mimeType": get_file.mime_type,
    }
    cache[file_data] = file_info
    save_upload_cache(cache)

    return get_file
