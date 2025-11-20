# karen/style_adapter.py
import json, os, re
from pathlib import Path

IDENTITY_PATH = Path("karen/identity.json")
PROFILE_PATH = Path("karen/style_profile.json")

def load_identity():
    if not IDENTITY_PATH.exists():
        raise FileNotFoundError(f"{IDENTITY_PATH} not found")
    return json.load(open(IDENTITY_PATH, "r", encoding="utf-8"))

def build_style_profile(identity):
    p = identity.get("personality", {})
    sp = {
        "tone": p.get("core_tone", "neutral"),
        "formality": p.get("formality", "neutral"),
        "emotion_level": p.get("emotion_level", "low"),
        "greetings": identity.get("speech_style", {}).get("greeting_examples", []),
        "farewells": identity.get("speech_style", {}).get("farewell_examples", []),
        "emojis": identity.get("speech_style", {}).get("default_emojis", []),
        "rules": identity.get("dialogue_constraints", {}),
        "memory_preferences": identity.get("memory_preferences", {})
    }
    return sp

def save_profile(profile):
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

def load_or_build_profile():
    if PROFILE_PATH.exists():
        return json.load(open(PROFILE_PATH, "r", encoding="utf-8"))
    identity = load_identity()
    profile = build_style_profile(identity)
    save_profile(profile)
    return profile

def apply_style_to_text(text, profile, user_name="Женя"):
    text = text.strip()
    # optionally insert a softening prefix
    if profile.get("rules", {}).get("insert_softeners", True):
        # add "Дорогой," only if not already intimate
        if not text.lower().startswith(("дорог", "мило", "люб")):
            text = "Дорогой, " + text
    # add emoji if allowed
    emojis = profile.get("emojis", [])
    if emojis:
        text = text + " " + emojis[0]
    # capitalize user name if required
    if profile.get("rules", {}).get("capitalize_user_name", True):
        text = text.replace(user_name, user_name.capitalize())
    # enforce no direct mention of being AI
    if profile.get("rules", {}).get("no_reference_to_being_ai", True):
        text = text.replace("я — ИИ", "я").replace("я ИИ", "я")
    return text
