"""
Definition of modes for Video Analyzer CLI.
Each mode includes an emoji and a prompt, which can be static or a function.
"""

modes = {
    "Paragraph": {
        "emoji": "📝",
        "prompt": (
            "Generate a paragraph that summarizes this video. Keep it to 3 to 5 "
            "sentences. Place each sentence of the summary into an object sent to "
            "set_timecodes with the timecode of the sentence in the video."
        ),
    },
    "KeyMoments": {
        "emoji": "🔑",
        "prompt": (
            "Generate bullet points for the video. Place each bullet point into an "
            "object sent to set_timecodes with the timecode of the bullet point in the video."
        ),
    },
    "Custom": {
        "emoji": "🔧",
        "prompt": lambda user_input: (
            f"Call set_timecodes once using the following instructions: {user_input}"
        ),
    },
}