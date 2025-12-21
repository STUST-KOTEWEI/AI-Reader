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

# Import new modules
from holo.nlp.emotion_analyzer import EmotionAnalyzer
from holo.visual.image_generator import ImageConceptGenerator
from holo.olfactory.scent_mapper import ScentMapper

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

# Initialize new components
emotion_analyzer = EmotionAnalyzer()
image_generator = ImageConceptGenerator()
scent_mapper = ScentMapper()


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
    # Use Week 1 Sprint features: text segmentation and haptics
    segments_data = text_segmenter.get_segments_with_metadata(request.text)
    haptic_pattern = haptics_emulator.generate_from_text(request.text)
    
    # Build auditory output with TTS info
    auditory_data = {
        "tts_engine": "ElevenLabs" if not hasattr(tts_engine, 'is_fallback') else "gTTS (fallback)",
        "segments": segments_data["total_segments"],
        "available_voices": tts_engine.get_available_voices()
    }
    
    # Build sensory output with haptics
    sensory_data = {
        "haptic_pattern": haptic_pattern,
        "haptic_events_count": len(haptic_pattern.get("events", [])),
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


# ==================== NEW ENDPOINTS ====================

class EmotionRequest(BaseModel):
    text: str
    detailed: bool = False


@app.post("/analyze_emotion", summary="Analyze Emotion", description="Analyzes emotional content in text.")
async def analyze_emotion(request: EmotionRequest):
    """
    Analyzes text to detect emotions and sentiment.
    
    - **text**: The text to analyze.
    - **detailed**: Whether to return detailed analysis with keyword counts.
    """
    if not request.text or not request.text.strip():
        return {"error": "Text is required"}
    
    result = emotion_analyzer.analyze(request.text, detailed=request.detailed)
    return result


class VisualRequest(BaseModel):
    text: str
    style: str = "realistic"
    max_concepts: int = 5


@app.post("/generate_visual", summary="Generate Visual Concepts", description="Generates visual concepts from narrative text.")
async def generate_visual(request: VisualRequest):
    """
    Generates visual concepts and scene descriptions from text.
    
    - **text**: The narrative text to visualize.
    - **style**: Visual style ('realistic', 'artistic', 'abstract', 'minimalist').
    - **max_concepts**: Maximum number of concepts to return.
    """
    if not request.text or not request.text.strip():
        return {"error": "Text is required"}
    
    result = image_generator.generate_concepts(
        request.text,
        style=request.style,
        max_concepts=request.max_concepts
    )
    return result


class ScentRequest(BaseModel):
    text: str
    intensity: float = 0.5
    emotion: str = None


@app.post("/generate_scent", summary="Generate Scent Profile", description="Maps narrative elements to scent profiles.")
async def generate_scent(request: ScentRequest):
    """
    Generates scent profiles from narrative text.
    
    - **text**: The text to analyze for scent mapping.
    - **intensity**: Base intensity multiplier (0.0-1.0).
    - **emotion**: Optional emotion to influence scent selection.
    """
    if not request.text or not request.text.strip():
        return {"error": "Text is required"}
    
    result = scent_mapper.generate_profile(
        request.text,
        intensity=request.intensity,
        emotion=request.emotion
    )
    return result


@app.get("/scent_families", summary="List Scent Families", description="Lists all available scent families.")
async def list_scent_families():
    """
    Lists all available scent families and their descriptions.
    """
    families = scent_mapper.list_families()
    return {
        "families": families,
        "total": len(families)
    }


@app.get("/visual_styles", summary="List Visual Styles", description="Lists all available visual styles.")
async def list_visual_styles():
    """
    Lists all available visual styles for concept generation.
    """
    styles = image_generator.list_available_styles()
    return {
        "styles": styles,
        "total": len(styles)
    }


class FullImmersionRequest(BaseModel):
    text: str
    user_profile: Dict[str, Any] = {}
    visual_style: str = "realistic"
    scent_intensity: float = 0.5


@app.post("/generate_full_immersion", summary="Generate Full Immersion", description="Generates complete multi-sensory immersion experience.")
async def generate_full_immersion(request: FullImmersionRequest):
    """
    Generates a complete multi-sensory immersion experience including:
    - Text segmentation
    - Emotion analysis
    - Haptic patterns
    - Visual concepts
    - Scent profiles
    - Audio configuration
    
    - **text**: The narrative text to process.
    - **user_profile**: Optional user preferences.
    - **visual_style**: Visual style for concept generation.
    - **scent_intensity**: Base intensity for scent profiles.
    """
    if not request.text or not request.text.strip():
        return {"error": "Text is required"}
    
    # Analyze emotion first to inform other modules
    emotion_result = emotion_analyzer.analyze(request.text)
    primary_emotion, emotion_intensity = emotion_analyzer.get_emotion_for_haptics(request.text)
    
    # Generate all components
    segments_data = text_segmenter.get_segments_with_metadata(request.text)
    haptic_pattern = haptics_emulator.generate_from_emotion(primary_emotion, emotion_intensity)
    visual_concepts = image_generator.generate_concepts(request.text, style=request.visual_style)
    scent_profile = scent_mapper.generate_profile(request.text, intensity=request.scent_intensity, emotion=primary_emotion)
    
    return {
        "text_analysis": {
            "segments": segments_data["segments"][:5],
            "total_segments": segments_data["total_segments"],
            "strategy": segments_data["strategy_used"]
        },
        "emotion_analysis": {
            "primary_emotion": emotion_result["primary_emotion"],
            "confidence": emotion_result["confidence"],
            "sentiment": emotion_result["sentiment"],
            "intensity": emotion_result["intensity"]
        },
        "auditory": {
            "tts_engine": "gTTS (fallback)" if hasattr(tts_engine, 'is_fallback') else "ElevenLabs",
            "available_voices": tts_engine.get_available_voices()
        },
        "haptic": {
            "pattern_name": haptic_pattern.get("name"),
            "events_count": len(haptic_pattern.get("events", [])),
            "pattern": haptic_pattern
        },
        "visual": {
            "scene_description": visual_concepts.get("scene_description"),
            "mood": visual_concepts.get("mood"),
            "lighting": visual_concepts.get("lighting"),
            "color_palette": visual_concepts.get("color_palette"),
            "concepts": visual_concepts.get("concepts", [])[:3]
        },
        "olfactory": {
            "primary_scent": scent_profile.get("primary_scent"),
            "ambient_scents": scent_profile.get("ambient_scents"),
            "blend_recipe": scent_profile.get("blend_recipe")
        }
    }
