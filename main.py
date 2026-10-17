import os
import sys
import pathlib
from dotenv import load_dotenv

# Load credentials securely from .env.local
env_file = pathlib.Path(__file__).parent / ".env.local"
if env_file.exists():
    load_dotenv(dotenv_path=env_file)

import higgsfield_client
from higgsfield_client import Completed, Failed, Cancelled, NSFW
from higgsfield_client.exceptions import HiggsfieldClientError


def extract_video_url(result: dict) -> str | None:
    """Helper to extract video URL from various response payload structures."""
    if not isinstance(result, dict):
        return None

    # Common payload structures: {"video": {"url": "..."}} or {"video": "..."}
    video = result.get("video")
    if isinstance(video, dict) and "url" in video:
        return video["url"]
    if isinstance(video, str) and video.startswith("http"):
        return video

    # {"videos": [{"url": "..."}, ...]}
    videos = result.get("videos")
    if isinstance(videos, list) and len(videos) > 0:
        first = videos[0]
        if isinstance(first, dict) and "url" in first:
            return first["url"]
        if isinstance(first, str) and first.startswith("http"):
            return first

    # {"url": "..."}
    if "url" in result and isinstance(result["url"], str):
        return result["url"]

    # {"output": {"video": ...}}
    output = result.get("output")
    if isinstance(output, dict):
        return extract_video_url(output)

    return None


def main():
    if not os.getenv("HF_KEY"):
        print("Error: HF_KEY is missing from environment and .env.local", file=sys.stderr)
        sys.exit(1)

    model = "bytedance/seedance-2.5/text-to-video"
    arguments = {
        "prompt": "A cinematic scene at sunset",
        "duration": 5,
        "resolution": "720p",
        "aspect_ratio": "16:9",
    }

    print(f"Submitting request to model '{model}'...")
    print(f"Prompt: \"{arguments['prompt']}\" (duration={arguments['duration']}s, resolution={arguments['resolution']}, aspect_ratio={arguments['aspect_ratio']})")

    def on_enqueue(request_id: str):
        print(f"Request enqueued with ID: {request_id}")

    def on_queue_update(status):
        status_name = status.__class__.__name__
        print(f"Status update: {status_name}")

    try:
        result = higgsfield_client.subscribe(
            model,
            arguments=arguments,
            on_enqueue=on_enqueue,
            on_queue_update=on_queue_update,
        )

        status_str = str(result.get("status", "")).lower()

        # Handle failed, canceled, or moderated/nsfw requests
        if status_str == "failed":
            error_msg = result.get("error") or result.get("message") or "Unknown failure from model."
            print(f"Generation failed: {error_msg}", file=sys.stderr)
            sys.exit(1)

        if status_str in ("nsfw", "moderated"):
            print("Generation was blocked by content moderation (NSFW/moderated).", file=sys.stderr)
            sys.exit(1)

        if status_str in ("canceled", "cancelled"):
            print("Generation was canceled before completion.", file=sys.stderr)
            sys.exit(1)

        # Successful completion
        video_url = extract_video_url(result)
        if not video_url:
            print("Request completed but no video URL was found in the response payload:", file=sys.stderr)
            print(result, file=sys.stderr)
            sys.exit(1)

        print("\n=== Generation Succeeded ===")
        print(f"Generated Video URL: {video_url}")
        return video_url

    except HiggsfieldClientError as err:
        print(f"Higgsfield Client Error: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected error during generation: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
