# Project-HOLO API Reference

## Overview

Project-HOLO provides a RESTful API for multi-modal narrative immersion. This document describes all available endpoints, request/response formats, and usage examples.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

#### GET `/`

Check if the API is running.

**Response:**
```json
{
  "message": "歡迎使用 Project-HOLO API"
}
```

---

### Immersion Generation

#### POST `/generate_immersion`

Generate a complete multi-modal immersion experience from narrative text.

**Request Body:**
```json
{
  "text": "string (required) - The narrative text to process",
  "user_profile": "object (optional) - User preferences and settings"
}
```

**Response:**
```json
{
  "auditory_output": {
    "tts_engine": "string - Active TTS engine name",
    "segments": "number - Number of text segments",
    "available_voices": "object - Available voice options"
  },
  "sensory_output": {
    "haptic_pattern": "object - Generated haptic pattern",
    "haptic_events_count": "number - Number of haptic events",
    "neuro": "string - Neuro stimulation pattern"
  },
  "knowledge_graph": {
    "segments": "array - Text segments",
    "text_length": "number - Total character count",
    "processing_strategy": "string - Segmentation strategy used"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/generate_immersion \
  -H "Content-Type: application/json" \
  -d '{"text": "The adventure begins! Are you ready?"}'
```

---

### Text Segmentation

#### POST `/segment_text`

Segment narrative text into meaningful chunks.

**Request Body:**
```json
{
  "text": "string (required) - Text to segment",
  "strategy": "string (optional) - Segmentation strategy: 'sentences', 'paragraphs', 'adaptive' (default: 'adaptive')"
}
```

**Response:**
```json
{
  "segments": [
    {
      "text": "string - Segment content",
      "index": "number - Segment index",
      "type": "string - Segment type",
      "length": "number - Character count"
    }
  ],
  "total_segments": "number",
  "total_length": "number",
  "strategy_used": "string",
  "metadata": {
    "max_chunk_size": "number",
    "average_segment_length": "number"
  }
}
```

---

### Text-to-Speech

#### POST `/tts`

Convert text to speech audio.

**Request Body:**
```json
{
  "text": "string (required) - Text to convert",
  "lang": "string (optional) - Language code (default: 'en')"
}
```

**Response:**
- Content-Type: `audio/mpeg`
- Body: Audio file binary data

---

### Haptic Patterns

#### POST `/generate_haptics`

Generate haptic feedback patterns from text or emotion.

**Request Body (one of):**
```json
{
  "text": "string - Generate haptics from text punctuation"
}
```
```json
{
  "emotion": "string - Emotion type: 'happy', 'sad', 'excited', 'calm', 'tense', 'surprised'",
  "intensity": "number (0.0-1.0) - Emotion intensity"
}
```
```json
{
  "pattern_name": "string - Name of predefined pattern"
}
```

**Response:**
```json
{
  "name": "string - Pattern name",
  "description": "string - Pattern description",
  "events": [
    {
      "time": "number - Event start time (ms)",
      "intensity": "number (0.0-1.0) - Vibration intensity",
      "duration": "number - Event duration (ms)"
    }
  ],
  "repeat": "boolean - Whether pattern repeats",
  "repeat_interval": "number (optional) - Repeat interval (ms)"
}
```

#### GET `/haptic_patterns`

List all available haptic patterns.

**Response:**
```json
{
  "patterns": ["heartbeat", "gentle_pulse", "sharp_tap", "rumble", "wave", "breathe"],
  "total": 6
}
```

---

### Emotion Analysis

#### POST `/analyze_emotion`

Analyze emotional content in text.

**Request Body:**
```json
{
  "text": "string (required) - Text to analyze",
  "detailed": "boolean (optional) - Return detailed analysis"
}
```

**Response:**
```json
{
  "primary_emotion": "string - Dominant emotion",
  "confidence": "number (0.0-1.0) - Analysis confidence",
  "emotions": {
    "joy": "number",
    "sadness": "number",
    "anger": "number",
    "fear": "number",
    "surprise": "number",
    "disgust": "number"
  },
  "sentiment": {
    "polarity": "number (-1.0 to 1.0)",
    "subjectivity": "number (0.0-1.0)"
  }
}
```

---

### Visual Generation

#### POST `/generate_visual`

Generate visual concepts from narrative text.

**Request Body:**
```json
{
  "text": "string (required) - Text to visualize",
  "style": "string (optional) - Visual style: 'realistic', 'artistic', 'abstract'"
}
```

**Response:**
```json
{
  "concepts": [
    {
      "element": "string - Visual element description",
      "color_palette": ["string - Hex colors"],
      "mood": "string - Visual mood",
      "composition": "string - Suggested composition"
    }
  ],
  "scene_description": "string - Overall scene description",
  "lighting": "string - Suggested lighting"
}
```

---

### Scent Mapping

#### POST `/generate_scent`

Map narrative elements to scent profiles.

**Request Body:**
```json
{
  "text": "string (required) - Text to analyze",
  "intensity": "number (0.0-1.0) (optional) - Scent intensity"
}
```

**Response:**
```json
{
  "primary_scent": {
    "name": "string - Scent name",
    "family": "string - Scent family",
    "intensity": "number (0.0-1.0)"
  },
  "ambient_scents": [
    {
      "name": "string",
      "family": "string",
      "intensity": "number"
    }
  ],
  "blend_recipe": "object - Hardware-compatible blend ratios"
}
```

---

## Error Handling

All endpoints return errors in a consistent format:

```json
{
  "error": "string - Error message",
  "detail": "string (optional) - Detailed error information"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `422` - Validation Error
- `500` - Internal Server Error

---

## Rate Limiting

Currently, there are no rate limits in development mode. Production deployments should implement appropriate rate limiting.

---

## Authentication

Authentication is not required for development. Production deployments should implement appropriate authentication mechanisms.
