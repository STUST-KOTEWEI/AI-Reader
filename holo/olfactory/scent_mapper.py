"""
Scent Mapper Module

Maps narrative elements to scent profiles for olfactory feedback.
Provides scent family detection, blending recipes, and intensity mapping.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ScentProfile:
    """A scent profile with name, family, and intensity."""
    name: str
    family: str
    intensity: float
    notes: List[str]


class ScentMapper:
    """
    Maps narrative text to scent profiles.
    
    Analyzes text to detect scent-related keywords and generates
    appropriate scent profiles for olfactory feedback devices.
    """
    
    # Scent families with associated keywords and scent names
    SCENT_FAMILIES = {
        "floral": {
            "keywords": ["flower", "rose", "jasmine", "lavender", "lily", "garden",
                        "blossom", "bloom", "petal", "bouquet", "orchid", "violet"],
            "scents": [
                {"name": "Rose Garden", "notes": ["rose", "green leaf", "morning dew"]},
                {"name": "Jasmine Night", "notes": ["jasmine", "white flower", "honey"]},
                {"name": "Lavender Fields", "notes": ["lavender", "herb", "soft musk"]}
            ],
            "base_intensity": 0.6
        },
        "woody": {
            "keywords": ["forest", "tree", "wood", "oak", "pine", "cedar",
                        "bark", "timber", "trunk", "log", "cabin"],
            "scents": [
                {"name": "Deep Forest", "notes": ["pine", "cedar", "earth"]},
                {"name": "Oak Study", "notes": ["oak", "leather", "paper"]},
                {"name": "Sandalwood Dream", "notes": ["sandalwood", "cream", "warmth"]}
            ],
            "base_intensity": 0.5
        },
        "citrus": {
            "keywords": ["lemon", "orange", "lime", "citrus", "grapefruit",
                        "tangerine", "zest", "fresh", "bright", "sunny"],
            "scents": [
                {"name": "Morning Citrus", "notes": ["lemon", "bergamot", "fresh air"]},
                {"name": "Orange Grove", "notes": ["orange", "neroli", "green"]},
                {"name": "Lime Burst", "notes": ["lime", "mint", "sparkling"]}
            ],
            "base_intensity": 0.7
        },
        "spicy": {
            "keywords": ["spice", "cinnamon", "pepper", "ginger", "clove",
                        "cardamom", "exotic", "warm", "market", "bazaar"],
            "scents": [
                {"name": "Spice Market", "notes": ["cinnamon", "cardamom", "saffron"]},
                {"name": "Warm Ginger", "notes": ["ginger", "pepper", "honey"]},
                {"name": "Exotic Blend", "notes": ["clove", "nutmeg", "vanilla"]}
            ],
            "base_intensity": 0.6
        },
        "fresh": {
            "keywords": ["clean", "air", "breeze", "wind", "morning", "rain",
                        "dew", "mist", "crisp", "cool", "refreshing"],
            "scents": [
                {"name": "Mountain Air", "notes": ["clean air", "pine", "ice"]},
                {"name": "After Rain", "notes": ["petrichor", "wet earth", "ozone"]},
                {"name": "Morning Dew", "notes": ["green", "water", "fresh grass"]}
            ],
            "base_intensity": 0.4
        },
        "sweet": {
            "keywords": ["sweet", "candy", "sugar", "honey", "vanilla", "cake",
                        "dessert", "chocolate", "caramel", "cookie"],
            "scents": [
                {"name": "Vanilla Dream", "notes": ["vanilla", "cream", "sugar"]},
                {"name": "Honey Nectar", "notes": ["honey", "flower", "warmth"]},
                {"name": "Chocolate Warmth", "notes": ["cocoa", "milk", "caramel"]}
            ],
            "base_intensity": 0.6
        },
        "earthy": {
            "keywords": ["earth", "soil", "ground", "mud", "dirt", "cave",
                        "stone", "rock", "mineral", "ancient", "roots"],
            "scents": [
                {"name": "Deep Earth", "notes": ["soil", "roots", "mushroom"]},
                {"name": "Stone Cave", "notes": ["mineral", "moss", "damp"]},
                {"name": "Ancient Ground", "notes": ["patchouli", "vetiver", "earth"]}
            ],
            "base_intensity": 0.5
        },
        "oceanic": {
            "keywords": ["ocean", "sea", "beach", "wave", "salt", "marine",
                        "coastal", "shore", "tide", "seaweed", "coral"],
            "scents": [
                {"name": "Ocean Breeze", "notes": ["sea salt", "marine", "driftwood"]},
                {"name": "Beach Morning", "notes": ["sand", "coconut", "sun"]},
                {"name": "Deep Sea", "notes": ["algae", "water", "mineral"]}
            ],
            "base_intensity": 0.5
        },
        "smoky": {
            "keywords": ["smoke", "fire", "burn", "ash", "ember", "flame",
                        "campfire", "incense", "charcoal", "bonfire"],
            "scents": [
                {"name": "Campfire Night", "notes": ["smoke", "wood", "embers"]},
                {"name": "Incense Temple", "notes": ["frankincense", "myrrh", "smoke"]},
                {"name": "Ember Glow", "notes": ["burnt wood", "warmth", "ash"]}
            ],
            "base_intensity": 0.6
        },
        "herbal": {
            "keywords": ["herb", "mint", "basil", "sage", "thyme", "rosemary",
                        "eucalyptus", "tea", "medicine", "apothecary"],
            "scents": [
                {"name": "Herb Garden", "notes": ["basil", "thyme", "rosemary"]},
                {"name": "Mint Fresh", "notes": ["mint", "eucalyptus", "green"]},
                {"name": "Sage Wisdom", "notes": ["sage", "cedar", "dry grass"]}
            ],
            "base_intensity": 0.5
        }
    }
    
    # Emotion to scent mapping
    EMOTION_SCENTS = {
        "joy": ["citrus", "floral", "fresh"],
        "sadness": ["woody", "earthy", "oceanic"],
        "anger": ["spicy", "smoky", "earthy"],
        "fear": ["smoky", "earthy", "herbal"],
        "surprise": ["citrus", "fresh", "herbal"],
        "calm": ["floral", "herbal", "woody"],
        "excitement": ["citrus", "spicy", "sweet"],
        "romance": ["floral", "sweet", "spicy"]
    }
    
    # Hardware channel mapping for scent families
    CHANNEL_MAP = {
        "floral": 1,
        "woody": 2,
        "citrus": 3,
        "spicy": 4,
        "fresh": 5,
        "sweet": 6,
        "earthy": 7,
        "oceanic": 8,
        "smoky": 9,
        "herbal": 10
    }
    
    def __init__(self):
        """Initialize the scent mapper."""
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for efficient matching."""
        self.family_patterns = {}
        for family, data in self.SCENT_FAMILIES.items():
            pattern = r'\b(' + '|'.join(re.escape(k) for k in data["keywords"]) + r')\b'
            self.family_patterns[family] = re.compile(pattern, re.IGNORECASE)
    
    def generate_profile(
        self,
        text: str,
        intensity: float = 0.5,
        emotion: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate scent profile from narrative text.
        
        Args:
            text: Text to analyze
            intensity: Base intensity multiplier (0.0-1.0)
            emotion: Optional emotion to influence scent selection
            
        Returns:
            Dictionary containing scent profile
        """
        if not text or not text.strip():
            return self._empty_result()
        
        # Detect scent families in text
        detected_families = self._detect_families(text)
        
        # Apply emotion bias if provided
        if emotion:
            detected_families = self._apply_emotion_bias(detected_families, emotion)
        
        # Get primary scent
        primary_scent = self._get_primary_scent(detected_families, intensity)
        
        # Get ambient scents
        ambient_scents = self._get_ambient_scents(detected_families, intensity)
        
        # Generate blend recipe
        blend_recipe = self._generate_blend_recipe(detected_families, intensity)
        
        return {
            "primary_scent": primary_scent,
            "ambient_scents": ambient_scents,
            "blend_recipe": blend_recipe,
            "detected_families": list(detected_families.keys()),
            "overall_intensity": intensity
        }
    
    def _detect_families(self, text: str) -> Dict[str, int]:
        """Detect scent families from text keywords."""
        families = {}
        
        for family, pattern in self.family_patterns.items():
            matches = pattern.findall(text)
            if matches:
                families[family] = len(matches)
        
        return families
    
    def _apply_emotion_bias(
        self,
        families: Dict[str, int],
        emotion: str
    ) -> Dict[str, int]:
        """Apply emotion-based bias to scent selection."""
        emotion = emotion.lower()
        
        if emotion not in self.EMOTION_SCENTS:
            return families
        
        preferred_families = self.EMOTION_SCENTS[emotion]
        
        # Boost preferred families
        for family in preferred_families:
            if family in families:
                families[family] += 2
            else:
                families[family] = 1
        
        return families
    
    def _get_primary_scent(
        self,
        families: Dict[str, int],
        intensity: float
    ) -> Dict[str, Any]:
        """Get the primary scent based on detected families."""
        if not families:
            # Default to fresh scent
            family = "fresh"
        else:
            family = max(families, key=families.get)
        
        family_data = self.SCENT_FAMILIES[family]
        scent_data = family_data["scents"][0]  # Primary scent from family
        
        final_intensity = min(1.0, family_data["base_intensity"] * intensity * 1.5)
        
        return {
            "name": scent_data["name"],
            "family": family,
            "intensity": round(final_intensity, 2),
            "notes": scent_data["notes"]
        }
    
    def _get_ambient_scents(
        self,
        families: Dict[str, int],
        intensity: float
    ) -> List[Dict[str, Any]]:
        """Get ambient/background scents."""
        ambient = []
        
        # Sort families by score, skip the primary
        sorted_families = sorted(families.items(), key=lambda x: x[1], reverse=True)
        
        for family, score in sorted_families[1:4]:  # Up to 3 ambient scents
            family_data = self.SCENT_FAMILIES[family]
            scent_data = family_data["scents"][-1]  # Secondary scent from family
            
            # Ambient scents are lower intensity
            final_intensity = min(1.0, family_data["base_intensity"] * intensity * 0.5)
            
            ambient.append({
                "name": scent_data["name"],
                "family": family,
                "intensity": round(final_intensity, 2),
                "notes": scent_data["notes"]
            })
        
        return ambient
    
    def _generate_blend_recipe(
        self,
        families: Dict[str, int],
        intensity: float
    ) -> Dict[str, Any]:
        """Generate a blend recipe for hardware devices."""
        if not families:
            return {"channels": [], "total_intensity": 0}
        
        total_score = sum(families.values())
        channels = []
        
        for family, score in families.items():
            # Calculate percentage for this family
            percentage = (score / total_score) * 100
            channel_intensity = min(1.0, intensity * (score / total_score) * 2)
            
            channels.append({
                "family": family,
                "percentage": round(percentage, 1),
                "intensity": round(channel_intensity, 2),
                "channel_id": self._get_channel_id(family)
            })
        
        return {
            "channels": sorted(channels, key=lambda x: x["percentage"], reverse=True),
            "total_intensity": round(intensity, 2),
            "blend_time_ms": 500  # Time to achieve blend
        }
    
    def _get_channel_id(self, family: str) -> int:
        """Map scent family to hardware channel ID."""
        return self.CHANNEL_MAP.get(family, 0)
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result for empty input."""
        return {
            "primary_scent": {
                "name": "Neutral",
                "family": "fresh",
                "intensity": 0.0,
                "notes": []
            },
            "ambient_scents": [],
            "blend_recipe": {"channels": [], "total_intensity": 0},
            "detected_families": [],
            "overall_intensity": 0.0
        }
    
    def get_family_info(self, family: str) -> Optional[Dict[str, Any]]:
        """Get information about a scent family."""
        if family not in self.SCENT_FAMILIES:
            return None
        
        data = self.SCENT_FAMILIES[family]
        return {
            "name": family,
            "keywords": data["keywords"],
            "available_scents": [s["name"] for s in data["scents"]],
            "base_intensity": data["base_intensity"]
        }
    
    def list_families(self) -> List[str]:
        """List all available scent families."""
        return list(self.SCENT_FAMILIES.keys())
    
    def get_emotion_suggestions(self, emotion: str) -> List[str]:
        """Get suggested scent families for an emotion."""
        return self.EMOTION_SCENTS.get(emotion.lower(), ["fresh"])


def generate_scent_profile(
    text: str,
    intensity: float = 0.5,
    emotion: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to generate scent profile.
    
    Args:
        text: Text to analyze
        intensity: Base intensity (0.0-1.0)
        emotion: Optional emotion for bias
        
    Returns:
        Scent profile dictionary
    """
    mapper = ScentMapper()
    return mapper.generate_profile(text, intensity, emotion)
