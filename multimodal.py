"""
Multimodal Parser
-----------------
Converts speech, image, and text inputs into structured observations.
"""
import re, random

def asr_to_text(audio_path: str) -> str:
    """Mock ASR transcription (replace with Whisper)."""
    return "User said: error E23, pump not starting."

def ocr_image(image_path: str) -> dict:
    """Extract error codes and visible readings."""
    m = re.search(r"(E\d{2,3})", image_path.upper())
    voltage = round(random.uniform(20, 26), 1)
    return {
        "error_code": m.group(1) if m else None,
        "pump_voltage": voltage
    }

def vision_hint(image_path: str) -> dict:
    """Lightweight hint from Vision-LLM (placeholder)."""
    return {"ui_window": "Cooling Panel", "confidence": 0.7}