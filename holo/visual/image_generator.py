"""
Image Concept Generator Module

Generates visual concepts and descriptions from narrative text.
Extracts visual elements, colors, moods, and composition suggestions.
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class VisualConcept:
    """A visual concept extracted from text."""
    element: str
    color_palette: List[str]
    mood: str
    composition: str


class ImageConceptGenerator:
    """
    Generates visual concepts from narrative text.
    
    Analyzes text to extract visual elements, suggest color palettes,
    determine mood, and provide composition recommendations.
    """
    
    # Default mood when no mood keywords are detected
    DEFAULT_MOOD = "peaceful"
    
    # Visual element keywords
    VISUAL_ELEMENTS = {
        "nature": {
            "keywords": ["forest", "tree", "mountain", "river", "ocean", "sky",
                        "sun", "moon", "star", "cloud", "rain", "snow", "flower",
                        "grass", "leaf", "garden", "lake", "waterfall", "beach"],
            "colors": ["#228B22", "#87CEEB", "#8FBC8F", "#4682B4", "#F0E68C"]
        },
        "architecture": {
            "keywords": ["building", "house", "castle", "tower", "bridge", "city",
                        "street", "road", "temple", "church", "palace", "ruins"],
            "colors": ["#696969", "#A9A9A9", "#D3D3D3", "#8B4513", "#CD853F"]
        },
        "interior": {
            "keywords": ["room", "door", "window", "chair", "table", "bed",
                        "lamp", "floor", "ceiling", "wall", "fireplace", "stairs"],
            "colors": ["#DEB887", "#F5DEB3", "#FAEBD7", "#8B4513", "#D2691E"]
        },
        "characters": {
            "keywords": ["person", "man", "woman", "child", "king", "queen",
                        "warrior", "hero", "villain", "wizard", "princess", "knight"],
            "colors": ["#FFE4C4", "#FFDAB9", "#FFE4E1", "#8B0000", "#4169E1"]
        },
        "creatures": {
            "keywords": ["dragon", "monster", "animal", "bird", "wolf", "horse",
                        "lion", "snake", "fish", "butterfly", "cat", "dog"],
            "colors": ["#800000", "#8B0000", "#FFD700", "#FF6347", "#4B0082"]
        },
        "magic": {
            "keywords": ["magic", "spell", "glow", "light", "fire", "energy",
                        "portal", "crystal", "aura", "mystical", "enchanted"],
            "colors": ["#9932CC", "#8A2BE2", "#00CED1", "#FFD700", "#FF69B4"]
        }
    }
    
    # Mood keywords and associated colors/lighting
    MOOD_MAPPING = {
        "peaceful": {
            "keywords": ["calm", "quiet", "serene", "gentle", "tranquil", "peaceful"],
            "lighting": "soft natural light",
            "colors": ["#E6F3FF", "#B0E0E6", "#98FB98", "#F0FFF0", "#FFFAF0"]
        },
        "dramatic": {
            "keywords": ["intense", "powerful", "dramatic", "epic", "grand", "mighty"],
            "lighting": "dramatic contrast lighting",
            "colors": ["#000000", "#8B0000", "#FFD700", "#4B0082", "#1C1C1C"]
        },
        "mysterious": {
            "keywords": ["mysterious", "dark", "shadow", "hidden", "secret", "unknown"],
            "lighting": "dim atmospheric lighting",
            "colors": ["#2F4F4F", "#191970", "#483D8B", "#4A4A4A", "#2E2E2E"]
        },
        "romantic": {
            "keywords": ["love", "romantic", "tender", "passionate", "warm", "intimate"],
            "lighting": "warm golden hour",
            "colors": ["#FF69B4", "#FFB6C1", "#FFC0CB", "#FFE4E1", "#FFD700"]
        },
        "adventurous": {
            "keywords": ["adventure", "journey", "quest", "explore", "discover", "brave"],
            "lighting": "bright dynamic lighting",
            "colors": ["#FF8C00", "#DAA520", "#32CD32", "#4169E1", "#20B2AA"]
        },
        "melancholic": {
            "keywords": ["sad", "lonely", "melancholy", "sorrow", "loss", "grief"],
            "lighting": "overcast diffused light",
            "colors": ["#708090", "#778899", "#B0C4DE", "#A9A9A9", "#696969"]
        },
        "joyful": {
            "keywords": ["happy", "joy", "celebration", "bright", "festive", "cheerful"],
            "lighting": "bright warm light",
            "colors": ["#FFD700", "#FFA500", "#FF6347", "#32CD32", "#00CED1"]
        },
        "eerie": {
            "keywords": ["strange", "eerie", "creepy", "ghostly", "haunted", "supernatural"],
            "lighting": "cold pale lighting",
            "colors": ["#00CED1", "#40E0D0", "#9370DB", "#6B8E23", "#2F4F4F"]
        }
    }
    
    # Composition suggestions
    COMPOSITION_TYPES = {
        "landscape": ["wide shot", "panoramic view", "horizon emphasis", "rule of thirds"],
        "portrait": ["centered subject", "close-up", "eye-level", "environmental portrait"],
        "action": ["dynamic angle", "motion blur", "diagonal lines", "low angle"],
        "atmospheric": ["depth of field", "silhouette", "foreground interest", "leading lines"],
        "intimate": ["close framing", "shallow depth", "warm tones", "soft focus background"]
    }
    
    # Visual style presets
    STYLES = {
        "realistic": {
            "description": "Photorealistic rendering with accurate lighting and textures",
            "characteristics": ["natural colors", "detailed textures", "accurate proportions"]
        },
        "artistic": {
            "description": "Painterly style with expressive brushstrokes",
            "characteristics": ["visible brushwork", "color harmony", "artistic interpretation"]
        },
        "abstract": {
            "description": "Non-representational focusing on shapes, colors, and emotions",
            "characteristics": ["geometric shapes", "bold colors", "conceptual elements"]
        },
        "minimalist": {
            "description": "Simple, clean designs with essential elements only",
            "characteristics": ["negative space", "limited palette", "clean lines"]
        }
    }
    
    def __init__(self):
        """Initialize the image concept generator."""
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching."""
        self.element_patterns = {}
        for category, data in self.VISUAL_ELEMENTS.items():
            pattern = r'\b(' + '|'.join(re.escape(k) for k in data["keywords"]) + r')\b'
            self.element_patterns[category] = re.compile(pattern, re.IGNORECASE)
        
        self.mood_patterns = {}
        for mood, data in self.MOOD_MAPPING.items():
            pattern = r'\b(' + '|'.join(re.escape(k) for k in data["keywords"]) + r')\b'
            self.mood_patterns[mood] = re.compile(pattern, re.IGNORECASE)
    
    def generate_concepts(
        self,
        text: str,
        style: str = "realistic",
        max_concepts: int = 5
    ) -> Dict[str, Any]:
        """
        Generate visual concepts from narrative text.
        
        Args:
            text: Text to analyze
            style: Visual style (realistic, artistic, abstract, minimalist)
            max_concepts: Maximum number of concepts to generate
            
        Returns:
            Dictionary containing visual concepts and metadata
        """
        if not text or not text.strip():
            return self._empty_result()
        
        # Extract visual elements
        elements = self._extract_elements(text)
        
        # Determine mood
        mood = self._determine_mood(text)
        
        # Generate color palette
        color_palette = self._generate_palette(elements, mood)
        
        # Suggest composition
        composition = self._suggest_composition(text, elements)
        
        # Generate scene description
        scene_description = self._generate_scene_description(text, elements, mood)
        
        # Get lighting suggestion
        lighting = self._suggest_lighting(mood)
        
        # Build concepts list
        concepts = self._build_concepts(elements, color_palette, mood, composition)[:max_concepts]
        
        return {
            "concepts": concepts,
            "scene_description": scene_description,
            "lighting": lighting,
            "mood": mood,
            "color_palette": color_palette,
            "style": self.STYLES.get(style, self.STYLES["realistic"]),
            "composition_suggestion": composition
        }
    
    def _extract_elements(self, text: str) -> Dict[str, List[str]]:
        """Extract visual elements from text."""
        elements = {}
        
        for category, pattern in self.element_patterns.items():
            matches = pattern.findall(text)
            if matches:
                elements[category] = list(set(m.lower() for m in matches))
        
        return elements
    
    def _determine_mood(self, text: str) -> str:
        """Determine the overall mood of the text."""
        mood_scores = {}
        
        for mood, pattern in self.mood_patterns.items():
            matches = pattern.findall(text)
            mood_scores[mood] = len(matches)
        
        if not mood_scores or all(v == 0 for v in mood_scores.values()):
            return self.DEFAULT_MOOD
        
        return max(mood_scores, key=mood_scores.get)
    
    def _generate_palette(self, elements: Dict[str, List[str]], mood: str) -> List[str]:
        """Generate a color palette based on elements and mood."""
        colors = set()
        
        # Add colors from detected elements
        for category in elements.keys():
            if category in self.VISUAL_ELEMENTS:
                colors.update(self.VISUAL_ELEMENTS[category]["colors"][:2])
        
        # Add colors from mood
        if mood in self.MOOD_MAPPING:
            colors.update(self.MOOD_MAPPING[mood]["colors"][:3])
        
        # Ensure we have at least 5 colors
        if len(colors) < 5:
            colors.update(["#FFFFFF", "#000000", "#808080"])
        
        return list(colors)[:7]
    
    def _suggest_composition(self, text: str, elements: Dict[str, List[str]]) -> str:
        """Suggest composition type based on content."""
        # Check for landscape indicators
        if "nature" in elements and len(elements.get("nature", [])) > 2:
            return "landscape - " + ", ".join(self.COMPOSITION_TYPES["landscape"][:2])
        
        # Check for character focus
        if "characters" in elements:
            return "portrait - " + ", ".join(self.COMPOSITION_TYPES["portrait"][:2])
        
        # Check for action words
        action_words = ["fight", "run", "chase", "battle", "fly", "escape"]
        if any(word in text.lower() for word in action_words):
            return "action - " + ", ".join(self.COMPOSITION_TYPES["action"][:2])
        
        # Default to atmospheric
        return "atmospheric - " + ", ".join(self.COMPOSITION_TYPES["atmospheric"][:2])
    
    def _suggest_lighting(self, mood: str) -> str:
        """Get lighting suggestion based on mood."""
        if mood in self.MOOD_MAPPING:
            return self.MOOD_MAPPING[mood]["lighting"]
        return "natural balanced lighting"
    
    def _generate_scene_description(
        self,
        text: str,
        elements: Dict[str, List[str]],
        mood: str
    ) -> str:
        """Generate a scene description for visualization."""
        parts = []
        
        # Add mood descriptor
        parts.append(f"A {mood} scene")
        
        # Add primary elements
        all_elements = []
        for category, items in elements.items():
            all_elements.extend(items[:2])
        
        if all_elements:
            parts.append(f"featuring {', '.join(all_elements[:4])}")
        
        # Add lighting
        lighting = self._suggest_lighting(mood)
        parts.append(f"with {lighting}")
        
        return " ".join(parts) + "."
    
    def _build_concepts(
        self,
        elements: Dict[str, List[str]],
        colors: List[str],
        mood: str,
        composition: str
    ) -> List[Dict[str, Any]]:
        """Build list of visual concepts."""
        concepts = []
        
        for category, items in elements.items():
            for item in items[:2]:  # Max 2 items per category
                concept = {
                    "element": item,
                    "category": category,
                    "color_palette": colors[:5],
                    "mood": mood,
                    "composition": composition
                }
                concepts.append(concept)
        
        return concepts
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result for empty input."""
        return {
            "concepts": [],
            "scene_description": "Empty scene.",
            "lighting": "neutral lighting",
            "mood": "neutral",
            "color_palette": ["#FFFFFF", "#000000", "#808080"],
            "style": self.STYLES["realistic"],
            "composition_suggestion": "standard framing"
        }
    
    def get_style_info(self, style: str) -> Dict[str, Any]:
        """Get information about a visual style."""
        return self.STYLES.get(style, self.STYLES["realistic"])
    
    def list_available_styles(self) -> List[str]:
        """List all available visual styles."""
        return list(self.STYLES.keys())


def generate_visual_concepts(
    text: str,
    style: str = "realistic",
    max_concepts: int = 5
) -> Dict[str, Any]:
    """
    Convenience function to generate visual concepts.
    
    Args:
        text: Text to analyze
        style: Visual style
        max_concepts: Maximum concepts to return
        
    Returns:
        Visual concepts dictionary
    """
    generator = ImageConceptGenerator()
    return generator.generate_concepts(text, style, max_concepts)
