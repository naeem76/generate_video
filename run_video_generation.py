#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick script to run video generation with credentials from .env
"""

import os
import sys
from dotenv import load_dotenv
from generate_video_client import GenerateVideoClient

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Get credentials from environment
ENDPOINT_ID = os.getenv("RUNPOD_ENDPOINT_ID")
RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")

# Validate credentials
if not ENDPOINT_ID or not RUNPOD_API_KEY:
    print("❌ Error: Missing credentials!")
    print("Please ensure your .env file contains:")
    print("  RUNPOD_ENDPOINT_ID=your-endpoint-id")
    print("  RUNPOD_API_KEY=your-api-key")
    exit(1)

print("=== Wan2.2 Video Generation ===\n")

# Initialize client
client = GenerateVideoClient(
    runpod_endpoint_id=ENDPOINT_ID,
    runpod_api_key=RUNPOD_API_KEY
)

# Generate video from example image
print("🎬 Starting video generation from example_image.png...\n")

result = client.create_video_from_image(
    image_path="./example_image.png",
    prompt="running man, grab the gun",
    width=384,      # Reduced from 480 (less VRAM)
    height=672,     # Reduced from 832 (less VRAM)
    length=41,      # Reduced from 81 (shorter video)
    steps=8,        # Reduced from 10 (faster)
    seed=42,
    cfg=2.0
)

# Save result
if result.get('status') == 'COMPLETED':
    output_path = "./output_video.mp4"
    if client.save_video_result(result, output_path):
        print(f"\n✅ Success! Video saved to: {output_path}")
    else:
        print("\n❌ Failed to save video")
elif result.get('status') == 'FAILED':
    print(f"\n❌ Job failed: {result.get('error')}")
elif result.get('status') == 'TIMEOUT':
    print("\n⏱️ Job timed out. The endpoint may need more time or may be cold starting.")
else:
    print(f"\n❓ Unknown status: {result}")

print("\n=== Done ===")

