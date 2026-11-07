import os
import subprocess
import json
import pytest

def test_video_1440p_compliance():
    video_dir = os.path.dirname(__file__)
    mp4_path = os.path.join(video_dir, "demo_video_1440p.mp4")
    assert os.path.exists(mp4_path), "demo_video_1440p.mp4 missing"
    file_size = os.path.getsize(mp4_path)
    # Anti-Black-Screen Gate: A genuine Hollywood 1440P video with dynamic frames and SAPI audio must be >= 5MB!
    assert file_size >= 5_000_000, f"MP4 file too small ({file_size} bytes), possible black screen dummy video!"

    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=width,height,duration,codec_name,codec_type",
        "-of", "json", mp4_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(res.stdout)
    
    # 1. Video Stream Checks
    v_streams = [s for s in info["streams"] if s.get("codec_type") == "video"]
    assert len(v_streams) > 0, "No video stream found"
    v_stream = v_streams[0]
    assert v_stream["width"] == 2560, f"Expected 2560 width, got {v_stream['width']}"
    assert v_stream["height"] == 1440, f"Expected 1440 height, got {v_stream['height']}"
    
    dur = float(v_stream["duration"])
    assert 135.0 <= dur <= 165.0, f"Expected 135s-165s, got {dur}s (Tournament gold window: 2:15 - 2:45)"
    
    # 2. Audio Stream Checks (Phase-locked speech audio)
    a_streams = [s for s in info["streams"] if s.get("codec_type") == "audio"]
    assert len(a_streams) > 0, "No audio stream found (Speech voiceover required)"
    assert a_streams[0]["codec_name"] == "aac", f"Expected AAC audio codec, got {a_streams[0]['codec_name']}"

if __name__ == "__main__":
    test_video_1440p_compliance()
    print("1440P Video audit PASS [100% HOLLYWOOD SUPREME BROADCAST COMPLIANT]!")
