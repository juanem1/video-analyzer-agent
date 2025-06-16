#!/usr/bin/env python3
"""
Video Analyzer CLI

Usage:
  python cli.py analyze --video /path/to/video.mp4 --mode "KeyMoments"
"""
import argparse
import os
import sys
from api import upload_file, generate_content
from modes import modes

def analyze_video(video_path, mode_key, custom_prompt):
    print(f"\n🔍 Analizing video: {video_path}")
    print(f"📊 Selected mode: {mode_key}")

    if not os.path.exists(video_path):
        print(f"❌ Error: The file {video_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    mode = modes.get(mode_key)
    if not mode:
        print(f"❌ Error: Invalid mode '{mode_key}'.", file=sys.stderr)
        print("Available modes:", ", ".join(modes.keys()))
        sys.exit(1)

    prompt = mode['prompt'](custom_prompt or "") if callable(mode.get('prompt')) else mode.get('prompt')

    print("\n🚀 Starting Gemini call...")
    try:
        video_file = upload_file(video_path)
        response = generate_content(prompt, video_file)

        print("\n✅ Response:")
        print("=" * 80)
        print(response)
        print("=" * 80)

    except Exception as error:
        print("❌ Error processing video:", error, file=sys.stderr)
        sys.exit(1)

def main():
    if 'GOOGLE_API_KEY' not in os.environ:
        print("❌ Error: The environment variable GOOGLE_API_KEY is not defined.", file=sys.stderr)
        print("Please set your Gemini API key with:")
        print("export GOOGLE_API_KEY=your_api_key_here")
        sys.exit(1)

    parser = argparse.ArgumentParser(prog='video-analyzer', description='Video Analyzer CLI')
    subparsers = parser.add_subparsers(dest='command')

    analyze_parser = subparsers.add_parser('analyze', help='Analyze a video')
    analyze_parser.add_argument('--video', '-v', required=True, help='Path to the video file to analyze')
    analyze_parser.add_argument('--mode', '-m', default='KeyMoments', choices=modes.keys(), help='Analysis mode')
    analyze_parser.add_argument('--custom-prompt', '-p', help='Custom prompt (only for Custom mode)')

    args = parser.parse_args()

    if args.command == 'analyze':
        analyze_video(args.video, args.mode, args.custom_prompt)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
