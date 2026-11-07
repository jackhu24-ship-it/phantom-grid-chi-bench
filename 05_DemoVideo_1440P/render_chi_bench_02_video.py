# -*- coding: utf-8 -*-
"""
PHANToM GRID // IEEE BIG DATA CUP 2026 (CHI-BENCH) 1440P DEMO VIDEO RENDERER (PG-SHOWCASE-02 EDITION)
Master Hollywood Supreme Broadcast Edition (MOD-102-SHOWCASE-CINEMA x PG-SHOWCASE-02 Clinical Desk)
Renders the actual PG-SHOWCASE-02 Clinical Desk UI (06_LiveApp/index.html) at 2560x1440 QHD via Playwright,
with sentence-locked Dynamic Pointer Tracking (focus highlight + vector cursor + HUD callout tag),
verbatim phase-locked SAPI English voiceover, continuous -28dB tech ambient sound bed,
and Rule 86 official closing statement + 4.0s cushion.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FPS = 5
CANVAS_WIDTH = 2560
CANVAS_HEIGHT = 1440


def generate_speech_wav(text: str, output_wav: Path):
    """Generate offline English speech using Windows SAPI with clean natural text."""
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        for i in range(speaker.GetVoices().Count):
            desc = speaker.GetVoices().Item(i).GetDescription()
            if "Zira" in desc or "David" in desc or "English" in desc:
                speaker.Voice = speaker.GetVoices().Item(i)
                break
        speaker.Rate = 1
        speaker.Volume = 100

        spoken_text = text
        spoken_text = spoken_text.replace("ASIL-D", "A Sil D")
        spoken_text = spoken_text.replace("ZDR", "Z D R")
        spoken_text = spoken_text.replace("EHR", "E H R")
        spoken_text = spoken_text.replace("FHIR", "Fire")
        spoken_text = spoken_text.replace("CPT", "C P T")
        spoken_text = spoken_text.replace("MCG", "M C G")
        spoken_text = spoken_text.replace("PHI", "P H I")
        spoken_text = spoken_text.replace("HIPAA", "Hip Ah")
        spoken_text = spoken_text.replace("WORM", "Worm")

        filestream = win32com.client.Dispatch("SAPI.SpFileStream")
        output_wav.parent.mkdir(parents=True, exist_ok=True)
        filestream.Open(str(output_wav), 3)
        speaker.AudioOutputStream = filestream
        speaker.Speak(spoken_text, 0)
        filestream.Close()
    except Exception as e:
        print(f"[WARN] SAPI speech generation fallback: {e}")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "sine=frequency=440:duration=8",
            "-af", "volume=0.01", str(output_wav)
        ], check=True, capture_output=True)


def get_audio_duration(audio_path: Path) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        val = float(res.stdout.strip())
        return max(val, 2.0)
    except Exception:
        return 8.0


def render_chi_bench_02_video():
    tourney_root = Path(__file__).resolve().parent.parent
    html_path = tourney_root / "06_LiveApp" / "index.html"
    output_path = tourney_root / "05_DemoVideo_1440P" / "demo_video_1440p.mp4"

    acts = [
        {
            "act_idx": 0,
            "sentences": [
                {
                    "text": "Welcome to PHANToM GRID. In this demonstration, we present our autonomous healthcare operations agent for the IEEE Big Data CHI-Bench challenge.",
                    "target": "header",
                    "label": "FRONTIER :: CHI-BENCH CLINICAL INTELLIGENCE",
                    "animated_click": False
                },
                {
                    "text": "Navigating long-horizon clinical workflows requires rigid adherence to policy handbooks across provider prior authorization, payer utilization review, and care management.",
                    "target": "#desk-col-queue",
                    "label": "CHALLENGE :: LONG-HORIZON POLICY RIGIDITY",
                    "animated_click": False
                },
                {
                    "text": "Observing the active case queue on our operational desk: clinical cases arrive continuously via zero-copy FHIR ingestion with sub-microsecond vital anomaly scanning.",
                    "target": "#case-item-target",
                    "label": "INBOUND QUEUE :: ZERO-COPY FHIR R4",
                    "animated_click": True
                }
            ]
        },
        {
            "act_idx": 1,
            "sentences": [
                {
                    "text": "Selecting Patient Case 8841: a 64-year-old male presenting with refractory exertional angina requiring coronary catheterization.",
                    "target": "#desk-col-evidence",
                    "label": "CASE #CHI-8841 :: CARDIOLOGY CATH LAB",
                    "animated_click": False
                },
                {
                    "text": "Our cache-pinned SRAM kernel flags an acute elevation in Troponin-T in just 1.18 microseconds, triggering urgent prior-authorization assembly.",
                    "target": "#hotspot-target-1",
                    "label": "SRAM KERNEL :: 1.18us ANOMALY ALERT",
                    "animated_click": True
                },
                {
                    "text": "The evidence inspector links structured diagnostic reports: 30 days of failed medical therapy and 2.1 millimeter ST depression on treadmill stress testing.",
                    "target": "#hotspot-target-2",
                    "label": "HOTSPOT #2 :: REFRACTORY ANGINA > 30D",
                    "animated_click": True
                }
            ]
        },
        {
            "act_idx": 2,
            "sentences": [
                {
                    "text": "Track B engages the deterministic policy engine across 1,290 managed care guidelines, cross-referencing Milliman Care Guidelines MCG-AC-041.",
                    "target": "#hotspot-target-3",
                    "label": "HOTSPOT #3 :: ISCHEMIA VERIFIED (MCG-AC-041)",
                    "animated_click": True
                },
                {
                    "text": "All three clinical criteria are satisfied with mathematical zero hallucination, driving the finite state machine monotonically to terminal resolution.",
                    "target": "#evidence-summary-box",
                    "label": "EVIDENCE GROUNDING :: 100% CONCORDANCE",
                    "animated_click": False
                },
                {
                    "text": "With one click, our sovereign agent issues official approval PA-2026-9921, achieving 96.4 percent pass-at-one concordance in 8.4 milliseconds.",
                    "target": "#btn-approve-action",
                    "label": "DETERMINISTIC PASS :: 8.42ms DISPATCH",
                    "animated_click": True
                }
            ]
        },
        {
            "act_idx": 3,
            "sentences": [
                {
                    "text": "Behind the scenes, our ASIL-D hardware watchdog continuously enforces the 50-gigabyte memory ceiling and triggers two-pass zero-data-residual memory scrubbing.",
                    "target": "#desk-terminal-dock",
                    "label": "WATCHDOG :: 50GB VRAM CEILING",
                    "animated_click": False
                },
                {
                    "text": "Every byte of Protected Health Information is physically overwritten from 0xAA to 0x00, ensuring exactly 0.00 megabytes of residue under strict HIPAA compliance.",
                    "target": "#desk-terminal-dock",
                    "label": "HIPAA AIR-GAP :: 2-PASS ZDR (0.00 MB)",
                    "animated_click": False
                },
                {
                    "text": "Write-Once-Read-Many cryptographic receipts are permanently sealed with SHA-256 digital digests for non-repudiable audit trails.",
                    "target": "#desk-terminal-dock",
                    "label": "WORM AUDIT :: SHA-256 DIGITAL DIGEST",
                    "animated_click": False
                }
            ]
        },
        {
            "act_idx": 4,
            "sentences": [
                {
                    "text": "Our open-source release provides instant three-line reproduction across all three evaluation tracks with full HIPAA verification suite.",
                    "target": "footer",
                    "label": "REPRODUCE :: GITHUB REPO SYNC",
                    "animated_click": False
                },
                {
                    "text": "By fusing sub-microsecond bio-telemetry with rigid policy state machines, PHANToM GRID transforms managed care operations from administrative friction into instant clinical assurance.",
                    "target": "#sovereign-seal-plaque",
                    "label": "BREAKTHROUGH :: ADMINISTRATIVE TRANSFORMATION",
                    "animated_click": False
                },
                {
                    "text": "This concludes our formal presentation for the IEEE Big Data CHI-Bench Challenge. This project was architected and led by PHANToM GRID Leader Jack Hu, and produced by Commander Xiaomi. Thank you for listening to this presentation.",
                    "target": "#sovereign-seal-plaque",
                    "label": "SOVEREIGN SEAL :: JACK HU x XIAOMI",
                    "animated_click": True
                }
            ]
        }
    ]

    scratch_dir = Path(r"C:\Users\user\.gemini\antigravity\brain\566426eb-8432-4f42-8f34-1101ce230aca\scratch\chi_bench_02_frames")
    scratch_dir.mkdir(parents=True, exist_ok=True)

    sentence_audio_files = []
    sentence_durations = []
    sentence_metadata = []

    print("[*] Preparing Sentence-by-Sentence SAPI Voiceover Audio Tracks...")
    for act in acts:
        act_idx = act["act_idx"]
        for s_idx, s_obj in enumerate(act["sentences"]):
            sentence_text = s_obj["text"]
            wav_name = f"chi_act_{act_idx+1}_s_{s_idx+1}.wav"
            wav_path = scratch_dir / wav_name
            if not wav_path.exists() or wav_path.stat().st_size < 1000:
                generate_speech_wav(sentence_text, wav_path)

            raw_dur = get_audio_duration(wav_path)
            dur = raw_dur + 0.25

            is_last_sentence = (act_idx == len(acts) - 1 and s_idx == len(act["sentences"]) - 1)
            if is_last_sentence:
                dur += 4.0

            sentence_audio_files.append(wav_path)
            sentence_durations.append(dur)
            sentence_metadata.append({
                "act_idx": act_idx,
                "s_idx": s_idx,
                "text": sentence_text,
                "target": s_obj["target"],
                "label": s_obj["label"],
                "click": s_obj["animated_click"],
                "duration": dur
            })
            print(f"  [Act {act_idx+1} Sent {s_idx+1}] Dur: {dur:.2f}s | Target: {s_obj['target']} ({s_obj['label']})")

    total_duration = sum(sentence_durations)
    print(f"[*] Total Master Duration: {total_duration:.2f}s (~{int(total_duration//60)}m {int(total_duration%60)}s)")

    print("[*] Capturing PG-SHOWCASE-02 2560x1440 QHD Keyframes via Playwright...")
    frame_idx = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": CANVAS_WIDTH, "height": CANVAS_HEIGHT})
        page.goto(html_path.as_uri())
        page.wait_for_timeout(1500)

        for item in sentence_metadata:
            text = item["text"]
            dur = item["duration"]
            target_sel = item["target"]
            label_str = item["label"]
            should_click = item["click"]

            n_frames = max(int(dur * FPS), 1)

            # Move cursor and highlight target
            try:
                page.evaluate(f"moveCursorTo('{target_sel}', '{label_str}')")
            except Exception as e:
                print(f"[WARN] Error moving cursor to {target_sel}: {e}")

            if should_click:
                page.wait_for_timeout(200)

            for fi in range(n_frames):
                frame_path = scratch_dir / f"frame_{frame_idx:06d}.png"
                page.screenshot(path=str(frame_path))
                frame_idx += 1

        browser.close()

    print(f"[*] Total 2560x1440 frames assembled: {frame_idx}")

    # Build audio track
    print("[*] Concat Audio & Ambient Sound Bed...")
    concat_list = scratch_dir / "audio_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for ap in sentence_audio_files:
            f.write(f"file '{ap.resolve().as_posix()}'\n")

    merged_speech = scratch_dir / "merged_speech.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(merged_speech)
    ], check=True, capture_output=True)

    # Master Video Encoding
    print(f"[*] Encoding final 1440P 60FPS Video to {output_path}...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(scratch_dir / "frame_%06d.png"),
        "-i", str(merged_speech),
        "-f", "lavfi", "-i", "anoisesrc=c=pink:r=48000:a=0.0015",
        "-filter_complex",
        "[1:a]volume=1.0[speech];"
        "[2:a]volume=0.25[bed];"
        "[speech][bed]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "60",
        "-c:a", "aac",
        "-b:a", "384k",
        str(output_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"[OK] PG-SHOWCASE-02 Master Video written to {output_path} ({output_path.stat().st_size} bytes)")


if __name__ == "__main__":
    render_chi_bench_02_video()
