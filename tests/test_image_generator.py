"""
Tests for Image Concept Generator Module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from holo.visual.image_generator import ImageConceptGenerator, generate_visual_concepts


class TestImageConceptGenerator:
    """Test cases for ImageConceptGenerator."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = ImageConceptGenerator()
    
    def test_initialization(self):
        """Test generator initialization."""
        assert self.generator is not None
        assert self.generator.VISUAL_ELEMENTS is not None
        assert self.generator.MOOD_MAPPING is not None
    
    def test_generate_nature_concepts(self):
        """Test concept generation for nature text."""
        text = "The ancient forest stretched endlessly, with towering trees reaching the sky."
        result = self.generator.generate_concepts(text)
        
        assert "concepts" in result
        assert "scene_description" in result
        assert "mood" in result
        assert "lighting" in result
        assert "color_palette" in result
    
    def test_generate_architecture_concepts(self):
        """Test concept generation for architecture text."""
        text = "The old castle stood on the hill, its tall tower overlooking the city streets."
        result = self.generator.generate_concepts(text)
        
        assert len(result["concepts"]) > 0
    
    def test_generate_character_concepts(self):
        """Test concept generation for character text."""
        text = "The brave warrior faced the ancient king, sword drawn."
        result = self.generator.generate_concepts(text)
        
        assert len(result["concepts"]) > 0
    
    def test_mood_detection_peaceful(self):
        """Test peaceful mood detection."""
        text = "The serene lake was calm and quiet, a gentle breeze stirring the water."
        result = self.generator.generate_concepts(text)
        
        assert result["mood"] == "peaceful"
    
    def test_mood_detection_dramatic(self):
        """Test dramatic mood detection."""
        text = "The powerful storm brought intense lightning and epic thunder."
        result = self.generator.generate_concepts(text)
        
        assert result["mood"] == "dramatic"
    
    def test_mood_detection_mysterious(self):
        """Test mysterious mood detection."""
        text = "In the dark shadows, hidden secrets awaited discovery."
        result = self.generator.generate_concepts(text)
        
        assert result["mood"] == "mysterious"
    
    def test_empty_text(self):
        """Test handling of empty text."""
        result = self.generator.generate_concepts("")
        
        assert result["concepts"] == []
        assert result["scene_description"] == "Empty scene."
    
    def test_color_palette_generation(self):
        """Test color palette generation."""
        text = "The forest was full of flowers and trees."
        result = self.generator.generate_concepts(text)
        
        assert "color_palette" in result
        assert len(result["color_palette"]) > 0
        # Colors should be hex format
        for color in result["color_palette"]:
            assert color.startswith("#")
    
    def test_composition_suggestion(self):
        """Test composition suggestion."""
        text = "The mountain landscape stretched far into the distance."
        result = self.generator.generate_concepts(text)
        
        assert "composition_suggestion" in result
        assert len(result["composition_suggestion"]) > 0
    
    def test_lighting_suggestion(self):
        """Test lighting suggestion."""
        text = "The romantic sunset painted the sky in warm colors."
        result = self.generator.generate_concepts(text)
        
        assert "lighting" in result
    
    def test_style_realistic(self):
        """Test realistic style."""
        text = "A beautiful forest scene."
        result = self.generator.generate_concepts(text, style="realistic")
        
        assert result["style"]["description"] is not None
    
    def test_style_artistic(self):
        """Test artistic style."""
        text = "A beautiful forest scene."
        result = self.generator.generate_concepts(text, style="artistic")
        
        assert "style" in result
    
    def test_max_concepts_limit(self):
        """Test max concepts limit."""
        text = "Forest trees mountain river ocean sky sun moon stars flowers garden lake."
        result = self.generator.generate_concepts(text, max_concepts=3)
        
        assert len(result["concepts"]) <= 3
    
    def test_get_style_info(self):
        """Test getting style information."""
        style_info = self.generator.get_style_info("realistic")
        
        assert "description" in style_info
        assert "characteristics" in style_info
    
    def test_list_available_styles(self):
        """Test listing available styles."""
        styles = self.generator.list_available_styles()
        
        assert "realistic" in styles
        assert "artistic" in styles
        assert "abstract" in styles
    
    def test_convenience_function(self):
        """Test the convenience function."""
        result = generate_visual_concepts("A forest with trees.")
        
        assert "concepts" in result
        assert "scene_description" in result
