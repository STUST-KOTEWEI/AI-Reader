from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from typing import Dict, Any, List

# 將專案根目錄加入 Python 路徑，以便引用 holo 模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import Week 1 Sprint features
from holo.ingestion.text_segmenter import TextSegmenter
from holo.auditory.elevenlabs_tts import get_tts_engine
from holo.sensory.haptics_emulator import HapticsEmulator
from holo.profile.user_profile import (
    UserProfile,
    get_profile_manager
)

app = FastAPI(
    title="Project-HOLO API",
    description="提供神經語意框架的多模態敘事沉浸體驗 API",
    version="0.1.0",
)

# 設定 CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # React 前端開發伺服器
    "capacitor://localhost",  # Capacitor App
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize Week 1 Sprint components
text_segmenter = TextSegmenter()
tts_engine = get_tts_engine()
haptics_emulator = HapticsEmulator()
profile_manager = get_profile_manager()


class NarrativeRequest(BaseModel):
    text: str
    user_profile: Dict[str, Any] = {}


class ImmersionResponse(BaseModel):
    auditory_output: Dict[str, Any]
    sensory_output: Dict[str, Any]
    knowledge_graph: Dict[str, Any]


@app.get("/", summary="API 根目錄", description="檢查 API 是否正常運作")
async def read_root():
    return {"message": "歡迎使用 Project-HOLO API"}

@app.post("/generate_immersion", response_model=ImmersionResponse, summary="生成沉浸式體驗", description="輸入敘事文本，生成對應的聽覺、感官與知識圖譜輸出")
async def generate_immersion(request: NarrativeRequest):
    """
    接收一段敘事文本，並回傳一個多模態的沉浸式體驗資料。

    - **text**: 必要，要處理的敘事文本。
    - **user_profile**: 可選，使用者的個人化設定。
    """
    # Get user profile settings
    user_id = request.user_profile.get('user_id', 'default')
    profile = profile_manager.get_profile(user_id)
    
    # Apply any runtime profile updates from request
    if request.user_profile.get('accessibility'):
        profile.update_accessibility(**request.user_profile['accessibility'])
    if request.user_profile.get('preferences'):
        profile.update_preferences(**request.user_profile['preferences'])
    
    # Use Week 1 Sprint features: text segmentation and haptics
    segments_data = text_segmenter.get_segments_with_metadata(request.text)
    haptic_pattern = haptics_emulator.generate_from_text(request.text)
    
    # Apply haptic intensity from user profile
    haptic_multiplier = profile.get_haptic_multiplier()
    if haptic_pattern.get("events"):
        for event in haptic_pattern["events"]:
            event["intensity"] = event.get("intensity", 0.5) * haptic_multiplier
    
    # Build auditory output with TTS info
    auditory_data = {
        "tts_engine": "ElevenLabs" if not hasattr(tts_engine, 'is_fallback') else "gTTS (fallback)",
        "segments": segments_data["total_segments"],
        "available_voices": tts_engine.get_available_voices(),
        "audio_enabled": profile.accessibility.audio_enabled,
        "audio_speed": profile.get_audio_speed()
    }
    
    # Build sensory output with haptics
    sensory_data = {
        "haptic_pattern": haptic_pattern,
        "haptic_events_count": len(haptic_pattern.get("events", [])),
        "haptic_enabled": profile.accessibility.haptic_enabled,
        "haptic_intensity": profile.accessibility.haptic_intensity,
        "neuro": "calm_alpha_wave"
    }
    
    # Knowledge graph (placeholder for now)
    kg_data = {
        "segments": segments_data["segments"][:3],  # First 3 segments as example
        "text_length": segments_data["total_length"],
        "processing_strategy": segments_data["strategy_used"]
    }

    return ImmersionResponse(
        auditory_output=auditory_data,
        sensory_output=sensory_data,
        knowledge_graph=kg_data,
    )

# 若要直接執行此檔案進行測試: uvicorn main:app --reload

from fastapi import Response
from gtts import gTTS
import io

class TTSRequest(BaseModel):
    text: str
    lang: str = 'en'

@app.post("/tts", summary="Text-to-Speech", description="Converts text to speech and returns an audio file.")
async def text_to_speech(request: TTSRequest):
    """
    Converts text to speech using available TTS engine.

    - **text**: The text to convert.
    - **lang**: The language of the text.
    """
    # Use the TTS engine (ElevenLabs if available, gTTS as fallback)
    fp = tts_engine.text_to_speech(request.text)
    return Response(fp.read(), media_type="audio/mpeg")


class SegmentRequest(BaseModel):
    text: str
    strategy: str = "adaptive"


@app.post("/segment_text", summary="Segment Text", description="Segments narrative text into chunks for processing.")
async def segment_text(request: SegmentRequest):
    """
    Segments text into meaningful chunks.
    
    - **text**: The text to segment.
    - **strategy**: Segmentation strategy ("sentences", "paragraphs", "adaptive").
    """
    result = text_segmenter.get_segments_with_metadata(request.text, strategy=request.strategy)
    return result


class HapticRequest(BaseModel):
    text: str = None
    emotion: str = None
    intensity: float = 0.5
    pattern_name: str = None


@app.post("/generate_haptics", summary="Generate Haptic Pattern", description="Generates haptic feedback patterns from text or emotion.")
async def generate_haptics(request: HapticRequest):
    """
    Generates haptic patterns for immersive feedback.
    
    - **text**: Text to generate haptics from (optional).
    - **emotion**: Emotion to generate haptics from (optional).
    - **intensity**: Emotion intensity (0.0-1.0).
    - **pattern_name**: Name of predefined pattern to retrieve (optional).
    """
    if request.pattern_name:
        pattern = haptics_emulator.get_pattern(request.pattern_name)
        if not pattern:
            return {"error": "Pattern not found"}
        return pattern
    elif request.text:
        return haptics_emulator.generate_from_text(request.text)
    elif request.emotion:
        return haptics_emulator.generate_from_emotion(request.emotion, request.intensity)
    else:
        return {"error": "Must provide text, emotion, or pattern_name"}


@app.get("/haptic_patterns", summary="List Haptic Patterns", description="Lists all available haptic patterns.")
async def list_haptic_patterns():
    """
    Lists all available predefined and custom haptic patterns.
    """
    patterns = haptics_emulator.get_all_patterns()
    return {
        "patterns": list(patterns.keys()),
        "total": len(patterns)
    }


# User Profile API Endpoints

class ProfileUpdateRequest(BaseModel):
    display_name: str = None
    accessibility: Dict[str, Any] = None
    preferences: Dict[str, Any] = None


@app.get("/profile/{user_id}", summary="取得使用者設定檔", description="取得指定使用者的個人化設定")
async def get_profile(user_id: str = "default"):
    """
    取得使用者的個人化設定檔。

    - **user_id**: 使用者 ID (預設為 'default')
    """
    profile = profile_manager.get_profile(user_id)
    return profile.to_dict()


@app.put("/profile/{user_id}", summary="更新使用者設定檔", description="更新指定使用者的個人化設定")
async def update_profile(user_id: str, request: ProfileUpdateRequest):
    """
    更新使用者的個人化設定檔。

    - **user_id**: 使用者 ID
    - **display_name**: 顯示名稱 (可選)
    - **accessibility**: 無障礙設定 (可選)
    - **preferences**: 使用者偏好設定 (可選)
    """
    update_data = {}
    if request.display_name is not None:
        update_data['display_name'] = request.display_name
    if request.accessibility is not None:
        update_data['accessibility'] = request.accessibility
    if request.preferences is not None:
        update_data['preferences'] = request.preferences
    
    profile = profile_manager.update_profile(user_id, update_data)
    return profile.to_dict()


@app.get("/profile", summary="取得預設使用者設定檔", description="取得預設使用者的個人化設定")
async def get_default_profile():
    """
    取得預設使用者的個人化設定檔。
    """
    profile = profile_manager.get_profile("default")
    return profile.to_dict()


@app.put("/profile", summary="更新預設使用者設定檔", description="更新預設使用者的個人化設定")
async def update_default_profile(request: ProfileUpdateRequest):
    """
    更新預設使用者的個人化設定檔。

    - **display_name**: 顯示名稱 (可選)
    - **accessibility**: 無障礙設定 (可選)
    - **preferences**: 使用者偏好設定 (可選)
    """
    update_data = {}
    if request.display_name is not None:
        update_data['display_name'] = request.display_name
    if request.accessibility is not None:
        update_data['accessibility'] = request.accessibility
    if request.preferences is not None:
        update_data['preferences'] = request.preferences
    
    profile = profile_manager.update_profile("default", update_data)
    return profile.to_dict()
