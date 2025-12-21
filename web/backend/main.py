from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from typing import Dict, Any, List, Optional

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

# Import new modules
from holo.history import (
    ReadingSession,
    ReadingHistory,
    get_history_manager
)
from holo.bookmarks import (
    Bookmark,
    Favorite,
    get_bookmarks_manager
)
from holo.auth import (
    User,
    Session,
    get_auth_manager
)

# Import social, recommendations, notifications, database, and logging
from holo.social import (
    Comment,
    Share,
    get_social_manager
)
from holo.recommendations import (
    ContentItem,
    UserPreference,
    Recommendation,
    get_recommendation_engine
)
from holo.notifications import (
    Notification,
    NotificationPreferences,
    get_notification_manager
)
from holo.database import get_database_manager
from holo.logging import (
    get_app_logger,
    get_performance_monitor,
    get_request_logger
)

# Initialize logging
logger = get_app_logger()
perf_monitor = get_performance_monitor()
request_logger = get_request_logger()

app = FastAPI(
    title="Project-HOLO API",
    description="提供神經語意框架的多模態敘事沉浸體驗 API",
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
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

# Initialize new managers
history_manager = get_history_manager()
bookmarks_manager = get_bookmarks_manager()
auth_manager = get_auth_manager()
social_manager = get_social_manager()
recommendation_engine = get_recommendation_engine()
notification_manager = get_notification_manager()

logger.info("API initialized successfully")


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


# ============================================================
# Reading History API Endpoints
# ============================================================

class ReadingSessionRequest(BaseModel):
    session_id: str
    content_id: str
    content_title: str
    started_at: str
    ended_at: Optional[str] = None
    progress: float = 0.0
    duration_seconds: int = 0


@app.get("/history/{user_id}", summary="取得閱讀歷史", description="取得使用者的閱讀歷史記錄", tags=["閱讀歷史"])
async def get_reading_history(user_id: str = "default"):
    """取得使用者的閱讀歷史記錄。"""
    history = history_manager.get_history(user_id)
    return history.to_dict()


@app.post("/history/{user_id}/session", summary="新增閱讀記錄", description="新增一筆閱讀記錄", tags=["閱讀歷史"])
async def add_reading_session(user_id: str, request: ReadingSessionRequest):
    """新增一筆閱讀記錄。"""
    session = ReadingSession(
        session_id=request.session_id,
        content_id=request.content_id,
        content_title=request.content_title,
        started_at=request.started_at,
        ended_at=request.ended_at,
        progress=request.progress,
        duration_seconds=request.duration_seconds
    )
    history = history_manager.add_session(user_id, session)
    return history.to_dict()


@app.get("/history/{user_id}/recent", summary="取得最近閱讀", description="取得最近的閱讀記錄", tags=["閱讀歷史"])
async def get_recent_reading(user_id: str = "default", limit: int = 10):
    """取得最近的閱讀記錄。"""
    history = history_manager.get_history(user_id)
    recent = history.get_recent_sessions(limit)
    return {"sessions": [s.to_dict() for s in recent]}


@app.delete("/history/{user_id}", summary="清除閱讀歷史", description="清除使用者的閱讀歷史", tags=["閱讀歷史"])
async def clear_reading_history(user_id: str):
    """清除使用者的閱讀歷史。"""
    success = history_manager.clear_history(user_id)
    return {"success": success}


# ============================================================
# Bookmarks & Favorites API Endpoints
# ============================================================

class BookmarkRequest(BaseModel):
    bookmark_id: str
    content_id: str
    content_title: str
    position: str = ""
    note: str = ""
    tags: List[str] = []


class FavoriteRequest(BaseModel):
    favorite_id: str
    content_id: str
    content_title: str
    content_type: str = "book"
    rating: int = 0


@app.get("/bookmarks/{user_id}", summary="取得書籤", description="取得使用者的所有書籤和收藏", tags=["書籤與收藏"])
async def get_user_bookmarks(user_id: str = "default"):
    """取得使用者的所有書籤和收藏。"""
    user_bookmarks = bookmarks_manager.get_user_bookmarks(user_id)
    return user_bookmarks.to_dict()


@app.post("/bookmarks/{user_id}/bookmark", summary="新增書籤", description="新增一個書籤", tags=["書籤與收藏"])
async def add_bookmark(user_id: str, request: BookmarkRequest):
    """新增一個書籤。"""
    bookmark = Bookmark(
        bookmark_id=request.bookmark_id,
        content_id=request.content_id,
        content_title=request.content_title,
        position=request.position,
        note=request.note,
        tags=request.tags
    )
    user_bookmarks = bookmarks_manager.add_bookmark(user_id, bookmark)
    return user_bookmarks.to_dict()


@app.delete("/bookmarks/{user_id}/bookmark/{bookmark_id}", summary="刪除書籤", description="刪除一個書籤", tags=["書籤與收藏"])
async def remove_bookmark(user_id: str, bookmark_id: str):
    """刪除一個書籤。"""
    success = bookmarks_manager.remove_bookmark(user_id, bookmark_id)
    if not success:
        raise HTTPException(status_code=404, detail="書籤未找到")
    return {"success": True}


@app.post("/bookmarks/{user_id}/favorite", summary="新增收藏", description="新增到收藏清單", tags=["書籤與收藏"])
async def add_favorite(user_id: str, request: FavoriteRequest):
    """新增到收藏清單。"""
    favorite = Favorite(
        favorite_id=request.favorite_id,
        content_id=request.content_id,
        content_title=request.content_title,
        content_type=request.content_type,
        rating=request.rating
    )
    user_bookmarks = bookmarks_manager.add_favorite(user_id, favorite)
    return user_bookmarks.to_dict()


@app.delete("/bookmarks/{user_id}/favorite/{favorite_id}", summary="刪除收藏", description="從收藏清單移除", tags=["書籤與收藏"])
async def remove_favorite(user_id: str, favorite_id: str):
    """從收藏清單移除。"""
    success = bookmarks_manager.remove_favorite(user_id, favorite_id)
    if not success:
        raise HTTPException(status_code=404, detail="收藏未找到")
    return {"success": True}


@app.get("/bookmarks/{user_id}/content/{content_id}", summary="取得內容書籤", description="取得特定內容的所有書籤", tags=["書籤與收藏"])
async def get_content_bookmarks(user_id: str, content_id: str):
    """取得特定內容的所有書籤。"""
    user_bookmarks = bookmarks_manager.get_user_bookmarks(user_id)
    bookmarks = user_bookmarks.get_bookmarks_by_content(content_id)
    return {"bookmarks": [b.to_dict() for b in bookmarks]}


@app.get("/bookmarks/{user_id}/is-favorite/{content_id}", summary="檢查是否收藏", description="檢查內容是否已收藏", tags=["書籤與收藏"])
async def check_is_favorite(user_id: str, content_id: str):
    """檢查內容是否已收藏。"""
    user_bookmarks = bookmarks_manager.get_user_bookmarks(user_id)
    return {"is_favorite": user_bookmarks.is_favorite(content_id)}


# ============================================================
# Authentication API Endpoints
# ============================================================

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


@app.post("/auth/register", summary="用戶註冊", description="註冊新用戶帳號", tags=["認證系統"])
async def register_user(request: RegisterRequest):
    """註冊新用戶帳號。"""
    user = auth_manager.register(
        username=request.username,
        email=request.email,
        password=request.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="用戶名或電子郵件已存在")
    return user.to_dict()


@app.post("/auth/login", summary="用戶登入", description="用戶登入並取得會話令牌", tags=["認證系統"])
async def login_user(request: LoginRequest):
    """用戶登入並取得會話令牌。"""
    session = auth_manager.login(
        username_or_email=request.username_or_email,
        password=request.password
    )
    if not session:
        raise HTTPException(status_code=401, detail="無效的憑證")
    return {
        "session_id": session.session_id,
        "token": session.token,
        "user_id": session.user_id,
        "expires_at": session.expires_at
    }


@app.post("/auth/logout", summary="用戶登出", description="登出並使會話令牌失效", tags=["認證系統"])
async def logout_user(token: str):
    """登出並使會話令牌失效。"""
    success = auth_manager.logout(token)
    return {"success": success}


@app.get("/auth/validate", summary="驗證令牌", description="驗證會話令牌是否有效", tags=["認證系統"])
async def validate_token(token: str):
    """驗證會話令牌是否有效。"""
    user = auth_manager.validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="無效或過期的令牌")
    return user.to_dict()


@app.get("/auth/user/{user_id}", summary="取得用戶資訊", description="取得指定用戶的資訊", tags=["認證系統"])
async def get_user_info(user_id: str):
    """取得指定用戶的資訊。"""
    user = auth_manager.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用戶未找到")
    return user.to_dict()


@app.put("/auth/password/{user_id}", summary="更改密碼", description="更改用戶密碼", tags=["認證系統"])
async def change_password(user_id: str, request: PasswordChangeRequest):
    """更改用戶密碼。"""
    success = auth_manager.update_password(
        user_id=user_id,
        old_password=request.old_password,
        new_password=request.new_password
    )
    if not success:
        raise HTTPException(status_code=400, detail="舊密碼不正確")
    return {"success": True}


@app.delete("/auth/user/{user_id}", summary="停用帳號", description="停用用戶帳號", tags=["認證系統"])
async def deactivate_user(user_id: str):
    """停用用戶帳號。"""
    success = auth_manager.deactivate_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用戶未找到")
    return {"success": True}


# ============================================================
# Social Features API Endpoints
# ============================================================

class CommentRequest(BaseModel):
    comment_id: str
    user_id: str
    content_id: str
    text: str
    parent_id: Optional[str] = None


class ShareRequest(BaseModel):
    share_id: str
    user_id: str
    content_id: str
    platform: str
    message: str = ""


@app.get("/social/comments/{content_id}", summary="取得留言", description="取得內容的所有留言", tags=["社交功能"])
async def get_comments(content_id: str):
    """取得內容的所有留言。"""
    comments = social_manager.get_comments(content_id)
    return {"comments": [c.to_dict() for c in comments]}


@app.post("/social/comments", summary="新增留言", description="新增留言", tags=["社交功能"])
async def add_comment(request: CommentRequest):
    """新增留言。"""
    comment = social_manager.add_comment(
        comment_id=request.comment_id,
        user_id=request.user_id,
        content_id=request.content_id,
        text=request.text,
        parent_id=request.parent_id
    )
    return comment.to_dict()


@app.delete("/social/comments/{content_id}/{comment_id}", summary="刪除留言", description="刪除留言", tags=["社交功能"])
async def delete_comment(content_id: str, comment_id: str):
    """刪除留言。"""
    success = social_manager.delete_comment(content_id, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="留言未找到")
    return {"success": True}


@app.post("/social/comments/{content_id}/{comment_id}/like", summary="按讚留言", description="對留言按讚", tags=["社交功能"])
async def like_comment(content_id: str, comment_id: str, user_id: str):
    """對留言按讚。"""
    success = social_manager.like_comment(user_id, comment_id, content_id)
    return {"success": success}


@app.post("/social/share", summary="分享內容", description="分享內容到社交平台", tags=["社交功能"])
async def share_content(request: ShareRequest):
    """分享內容到社交平台。"""
    share = social_manager.share_content(
        share_id=request.share_id,
        user_id=request.user_id,
        content_id=request.content_id,
        platform=request.platform,
        message=request.message
    )
    return share.to_dict()


@app.get("/social/share-url/{content_id}/{platform}", summary="取得分享連結", description="取得社交平台分享連結", tags=["社交功能"])
async def get_share_url(content_id: str, platform: str):
    """取得社交平台分享連結。"""
    url = social_manager.get_share_url(content_id, platform)
    return {"url": url}


@app.get("/social/stats/{content_id}", summary="取得內容統計", description="取得內容的社交統計", tags=["社交功能"])
async def get_content_stats(content_id: str):
    """取得內容的社交統計。"""
    stats = social_manager.get_stats(content_id)
    return stats.to_dict()


@app.post("/social/view/{content_id}", summary="記錄瀏覽", description="記錄內容瀏覽", tags=["社交功能"])
async def record_view(content_id: str):
    """記錄內容瀏覽。"""
    social_manager.record_view(content_id)
    return {"success": True}


# ============================================================
# Recommendation API Endpoints
# ============================================================

class ContentItemRequest(BaseModel):
    content_id: str
    title: str
    author: str = ""
    genre: str = ""
    tags: List[str] = []
    rating: float = 0.0
    popularity_score: float = 0.0


class UserPreferenceRequest(BaseModel):
    user_id: str
    favorite_genres: List[str] = []
    favorite_authors: List[str] = []
    favorite_tags: List[str] = []


@app.get("/recommendations/{user_id}", summary="取得推薦", description="取得個人化推薦內容", tags=["推薦系統"])
async def get_recommendations(user_id: str, limit: int = 10):
    """取得個人化推薦內容。"""
    recommendations = recommendation_engine.get_recommendations(user_id, limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.get("/recommendations/similar/{content_id}", summary="取得相似內容", description="取得相似內容推薦", tags=["推薦系統"])
async def get_similar_content(content_id: str, limit: int = 5):
    """取得相似內容推薦。"""
    recommendations = recommendation_engine.get_similar_content(content_id, limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.get("/recommendations/popular", summary="取得熱門內容", description="取得熱門內容", tags=["推薦系統"])
async def get_popular_content(limit: int = 10):
    """取得熱門內容。"""
    recommendations = recommendation_engine.get_popular_content(limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.get("/recommendations/trending", summary="取得最新熱門", description="取得最新熱門內容", tags=["推薦系統"])
async def get_trending_content(limit: int = 10):
    """取得最新熱門內容。"""
    recommendations = recommendation_engine.get_trending_content(limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.post("/recommendations/content", summary="新增內容", description="新增內容到目錄", tags=["推薦系統"])
async def add_content_item(request: ContentItemRequest):
    """新增內容到目錄。"""
    from holo.recommendations import ContentItem
    content = ContentItem(
        content_id=request.content_id,
        title=request.title,
        author=request.author,
        genre=request.genre,
        tags=request.tags,
        rating=request.rating,
        popularity_score=request.popularity_score
    )
    recommendation_engine.add_content(content)
    return content.to_dict()


@app.put("/recommendations/preferences/{user_id}", summary="設定偏好", description="設定使用者推薦偏好", tags=["推薦系統"])
async def set_user_preferences(user_id: str, request: UserPreferenceRequest):
    """設定使用者推薦偏好。"""
    from holo.recommendations import UserPreference
    preference = UserPreference(
        user_id=user_id,
        favorite_genres=request.favorite_genres,
        favorite_authors=request.favorite_authors,
        favorite_tags=request.favorite_tags
    )
    recommendation_engine.set_user_preference(preference)
    return preference.to_dict()


@app.post("/recommendations/rate/{user_id}/{content_id}", summary="評分內容", description="對內容評分", tags=["推薦系統"])
async def rate_content(user_id: str, content_id: str, rating: float):
    """對內容評分。"""
    recommendation_engine.rate_content(user_id, content_id, rating)
    return {"success": True}


# ============================================================
# Notification API Endpoints
# ============================================================

class NotificationRequest(BaseModel):
    notification_id: str
    user_id: str
    title: str
    message: str
    type: str = "info"
    action_url: Optional[str] = None
    metadata: Dict[str, Any] = {}


class NotificationPreferencesRequest(BaseModel):
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    social_notifications: bool = True
    recommendation_notifications: bool = True
    system_notifications: bool = True


@app.get("/notifications/{user_id}", summary="取得通知", description="取得使用者通知", tags=["通知系統"])
async def get_notifications(user_id: str, unread_only: bool = False, limit: int = 50):
    """取得使用者通知。"""
    notifications = notification_manager.get_notifications(user_id, unread_only, limit)
    return {"notifications": [n.to_dict() for n in notifications]}


@app.get("/notifications/{user_id}/unread-count", summary="取得未讀數", description="取得未讀通知數量", tags=["通知系統"])
async def get_unread_count(user_id: str):
    """取得未讀通知數量。"""
    count = notification_manager.get_unread_count(user_id)
    return {"count": count}


@app.post("/notifications", summary="發送通知", description="發送通知給使用者", tags=["通知系統"])
async def send_notification(request: NotificationRequest):
    """發送通知給使用者。"""
    notification = notification_manager.send_notification(
        notification_id=request.notification_id,
        user_id=request.user_id,
        title=request.title,
        message=request.message,
        notification_type=request.type,
        action_url=request.action_url,
        metadata=request.metadata
    )
    if notification:
        return notification.to_dict()
    return {"message": "通知未發送（使用者設定關閉）"}


@app.put("/notifications/{user_id}/{notification_id}/read", summary="標記已讀", description="標記通知為已讀", tags=["通知系統"])
async def mark_notification_read(user_id: str, notification_id: str):
    """標記通知為已讀。"""
    success = notification_manager.mark_as_read(user_id, notification_id)
    return {"success": success}


@app.put("/notifications/{user_id}/read-all", summary="全部標記已讀", description="標記所有通知為已讀", tags=["通知系統"])
async def mark_all_notifications_read(user_id: str):
    """標記所有通知為已讀。"""
    count = notification_manager.mark_all_as_read(user_id)
    return {"count": count}


@app.delete("/notifications/{user_id}/{notification_id}", summary="刪除通知", description="刪除通知", tags=["通知系統"])
async def delete_notification(user_id: str, notification_id: str):
    """刪除通知。"""
    success = notification_manager.delete_notification(user_id, notification_id)
    return {"success": success}


@app.delete("/notifications/{user_id}", summary="清除通知", description="清除所有通知", tags=["通知系統"])
async def clear_notifications(user_id: str):
    """清除所有通知。"""
    count = notification_manager.clear_notifications(user_id)
    return {"count": count}


@app.get("/notifications/{user_id}/preferences", summary="取得通知設定", description="取得通知偏好設定", tags=["通知系統"])
async def get_notification_preferences(user_id: str):
    """取得通知偏好設定。"""
    prefs = notification_manager.get_preferences(user_id)
    return prefs.to_dict()


@app.put("/notifications/{user_id}/preferences", summary="更新通知設定", description="更新通知偏好設定", tags=["通知系統"])
async def update_notification_preferences(user_id: str, request: NotificationPreferencesRequest):
    """更新通知偏好設定。"""
    from holo.notifications import NotificationPreferences
    prefs = NotificationPreferences(
        user_id=user_id,
        email_enabled=request.email_enabled,
        push_enabled=request.push_enabled,
        in_app_enabled=request.in_app_enabled,
        social_notifications=request.social_notifications,
        recommendation_notifications=request.recommendation_notifications,
        system_notifications=request.system_notifications
    )
    notification_manager.set_preferences(prefs)
    return prefs.to_dict()


# ============================================================
# System & Monitoring API Endpoints
# ============================================================

@app.get("/system/health", summary="健康檢查", description="檢查系統健康狀態", tags=["系統監控"])
async def health_check():
    """檢查系統健康狀態。"""
    return {
        "status": "healthy",
        "version": "0.3.0",
        "services": {
            "api": "up",
            "database": "up",
            "cache": "up"
        }
    }


@app.get("/system/metrics", summary="系統指標", description="取得系統效能指標", tags=["系統監控"])
async def get_metrics():
    """取得系統效能指標。"""
    metrics = perf_monitor.get_all_metrics()
    return metrics


# ============================================================
# Social Features API Endpoints
# ============================================================

class CommentRequest(BaseModel):
    comment_id: str
    user_id: str
    content_id: str
    text: str
    parent_id: Optional[str] = None


class ShareRequest(BaseModel):
    share_id: str
    user_id: str
    content_id: str
    platform: str
    message: str = ""


@app.get("/social/comments/{content_id}", summary="取得留言", description="取得內容的所有留言", tags=["社交功能"])
async def get_comments(content_id: str):
    """取得內容的所有留言。"""
    comments = social_manager.get_comments(content_id)
    return {"comments": [c.to_dict() for c in comments]}


@app.post("/social/comments", summary="新增留言", description="新增留言", tags=["社交功能"])
async def add_comment(request: CommentRequest):
    """新增留言。"""
    comment = social_manager.add_comment(
        comment_id=request.comment_id,
        user_id=request.user_id,
        content_id=request.content_id,
        text=request.text,
        parent_id=request.parent_id
    )
    return comment.to_dict()


@app.delete("/social/comments/{content_id}/{comment_id}", summary="刪除留言", description="刪除留言", tags=["社交功能"])
async def delete_comment(content_id: str, comment_id: str):
    """刪除留言。"""
    success = social_manager.delete_comment(content_id, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="留言未找到")
    return {"success": True}


@app.post("/social/comments/{content_id}/{comment_id}/like", summary="按讚留言", description="對留言按讚", tags=["社交功能"])
async def like_comment(content_id: str, comment_id: str, user_id: str):
    """對留言按讚。"""
    success = social_manager.like_comment(user_id, comment_id, content_id)
    return {"success": success}


@app.post("/social/share", summary="分享內容", description="分享內容到社交平台", tags=["社交功能"])
async def share_content(request: ShareRequest):
    """分享內容到社交平台。"""
    share = social_manager.share_content(
        share_id=request.share_id,
        user_id=request.user_id,
        content_id=request.content_id,
        platform=request.platform,
        message=request.message
    )
    return share.to_dict()


@app.get("/social/share-url/{content_id}/{platform}", summary="取得分享連結", description="取得社交平台分享連結", tags=["社交功能"])
async def get_share_url(content_id: str, platform: str):
    """取得社交平台分享連結。"""
    url = social_manager.get_share_url(content_id, platform)
    return {"url": url}


@app.get("/social/stats/{content_id}", summary="取得內容統計", description="取得內容的社交統計", tags=["社交功能"])
async def get_content_stats(content_id: str):
    """取得內容的社交統計。"""
    stats = social_manager.get_stats(content_id)
    return stats.to_dict()


@app.post("/social/view/{content_id}", summary="記錄瀏覽", description="記錄內容瀏覽", tags=["社交功能"])
async def record_view(content_id: str):
    """記錄內容瀏覽。"""
    social_manager.record_view(content_id)
    return {"success": True}


# ============================================================
# Recommendation API Endpoints
# ============================================================

class ContentItemRequest(BaseModel):
    content_id: str
    title: str
    author: str = ""
    genre: str = ""
    tags: List[str] = []
    rating: float = 0.0
    popularity_score: float = 0.0


class UserPreferenceRequest(BaseModel):
    user_id: str
    favorite_genres: List[str] = []
    favorite_authors: List[str] = []
    favorite_tags: List[str] = []


@app.get("/recommendations/{user_id}", summary="取得推薦", description="取得個人化推薦內容", tags=["推薦系統"])
async def get_recommendations(user_id: str, limit: int = 10):
    """取得個人化推薦內容。"""
    recommendations = recommendation_engine.get_recommendations(user_id, limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.get("/recommendations/similar/{content_id}", summary="取得相似內容", description="取得相似內容推薦", tags=["推薦系統"])
async def get_similar_content(content_id: str, limit: int = 5):
    """取得相似內容推薦。"""
    recommendations = recommendation_engine.get_similar_content(content_id, limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.get("/recommendations/popular", summary="取得熱門內容", description="取得熱門內容", tags=["推薦系統"])
async def get_popular_content(limit: int = 10):
    """取得熱門內容。"""
    recommendations = recommendation_engine.get_popular_content(limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.get("/recommendations/trending", summary="取得最新熱門", description="取得最新熱門內容", tags=["推薦系統"])
async def get_trending_content(limit: int = 10):
    """取得最新熱門內容。"""
    recommendations = recommendation_engine.get_trending_content(limit)
    return {"recommendations": [r.to_dict() for r in recommendations]}


@app.post("/recommendations/content", summary="新增內容", description="新增內容到目錄", tags=["推薦系統"])
async def add_content_item(request: ContentItemRequest):
    """新增內容到目錄。"""
    from holo.recommendations import ContentItem
    content = ContentItem(
        content_id=request.content_id,
        title=request.title,
        author=request.author,
        genre=request.genre,
        tags=request.tags,
        rating=request.rating,
        popularity_score=request.popularity_score
    )
    recommendation_engine.add_content(content)
    return content.to_dict()


@app.put("/recommendations/preferences/{user_id}", summary="設定偏好", description="設定使用者推薦偏好", tags=["推薦系統"])
async def set_user_preferences(user_id: str, request: UserPreferenceRequest):
    """設定使用者推薦偏好。"""
    from holo.recommendations import UserPreference
    preference = UserPreference(
        user_id=user_id,
        favorite_genres=request.favorite_genres,
        favorite_authors=request.favorite_authors,
        favorite_tags=request.favorite_tags
    )
    recommendation_engine.set_user_preference(preference)
    return preference.to_dict()


@app.post("/recommendations/rate/{user_id}/{content_id}", summary="評分內容", description="對內容評分", tags=["推薦系統"])
async def rate_content(user_id: str, content_id: str, rating: float):
    """對內容評分。"""
    recommendation_engine.rate_content(user_id, content_id, rating)
    return {"success": True}


# ============================================================
# Notification API Endpoints
# ============================================================

class NotificationRequest(BaseModel):
    notification_id: str
    user_id: str
    title: str
    message: str
    type: str = "info"
    action_url: Optional[str] = None
    metadata: Dict[str, Any] = {}


class NotificationPreferencesRequest(BaseModel):
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True
    social_notifications: bool = True
    recommendation_notifications: bool = True
    system_notifications: bool = True


@app.get("/notifications/{user_id}", summary="取得通知", description="取得使用者通知", tags=["通知系統"])
async def get_notifications(user_id: str, unread_only: bool = False, limit: int = 50):
    """取得使用者通知。"""
    notifications = notification_manager.get_notifications(user_id, unread_only, limit)
    return {"notifications": [n.to_dict() for n in notifications]}


@app.get("/notifications/{user_id}/unread-count", summary="取得未讀數", description="取得未讀通知數量", tags=["通知系統"])
async def get_unread_count(user_id: str):
    """取得未讀通知數量。"""
    count = notification_manager.get_unread_count(user_id)
    return {"count": count}


@app.post("/notifications", summary="發送通知", description="發送通知給使用者", tags=["通知系統"])
async def send_notification(request: NotificationRequest):
    """發送通知給使用者。"""
    notification = notification_manager.send_notification(
        notification_id=request.notification_id,
        user_id=request.user_id,
        title=request.title,
        message=request.message,
        notification_type=request.type,
        action_url=request.action_url,
        metadata=request.metadata
    )
    if notification:
        return notification.to_dict()
    return {"message": "通知未發送（使用者設定關閉）"}


@app.put("/notifications/{user_id}/{notification_id}/read", summary="標記已讀", description="標記通知為已讀", tags=["通知系統"])
async def mark_notification_read(user_id: str, notification_id: str):
    """標記通知為已讀。"""
    success = notification_manager.mark_as_read(user_id, notification_id)
    return {"success": success}


@app.put("/notifications/{user_id}/read-all", summary="全部標記已讀", description="標記所有通知為已讀", tags=["通知系統"])
async def mark_all_notifications_read(user_id: str):
    """標記所有通知為已讀。"""
    count = notification_manager.mark_all_as_read(user_id)
    return {"count": count}


@app.delete("/notifications/{user_id}/{notification_id}", summary="刪除通知", description="刪除通知", tags=["通知系統"])
async def delete_notification(user_id: str, notification_id: str):
    """刪除通知。"""
    success = notification_manager.delete_notification(user_id, notification_id)
    return {"success": success}


@app.delete("/notifications/{user_id}", summary="清除通知", description="清除所有通知", tags=["通知系統"])
async def clear_notifications(user_id: str):
    """清除所有通知。"""
    count = notification_manager.clear_notifications(user_id)
    return {"count": count}


@app.get("/notifications/{user_id}/preferences", summary="取得通知設定", description="取得通知偏好設定", tags=["通知系統"])
async def get_notification_preferences(user_id: str):
    """取得通知偏好設定。"""
    prefs = notification_manager.get_preferences(user_id)
    return prefs.to_dict()


@app.put("/notifications/{user_id}/preferences", summary="更新通知設定", description="更新通知偏好設定", tags=["通知系統"])
async def update_notification_preferences(user_id: str, request: NotificationPreferencesRequest):
    """更新通知偏好設定。"""
    from holo.notifications import NotificationPreferences
    prefs = NotificationPreferences(
        user_id=user_id,
        email_enabled=request.email_enabled,
        push_enabled=request.push_enabled,
        in_app_enabled=request.in_app_enabled,
        social_notifications=request.social_notifications,
        recommendation_notifications=request.recommendation_notifications,
        system_notifications=request.system_notifications
    )
    notification_manager.set_preferences(prefs)
    return prefs.to_dict()


# ============================================================
# System & Monitoring API Endpoints
# ============================================================

@app.get("/system/health", summary="健康檢查", description="檢查系統健康狀態", tags=["系統監控"])
async def health_check():
    """檢查系統健康狀態。"""
    return {
        "status": "healthy",
        "version": "0.3.0",
        "services": {
            "api": "up",
            "database": "up",
            "cache": "up"
        }
    }


@app.get("/system/metrics", summary="系統指標", description="取得系統效能指標", tags=["系統監控"])
async def get_metrics():
    """取得系統效能指標。"""
    metrics = perf_monitor.get_all_metrics()
    return metrics
