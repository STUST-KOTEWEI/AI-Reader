"""
Tests for Scent Mapper Module
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from holo.olfactory.scent_mapper import ScentMapper, generate_scent_profile


class TestScentMapper:
    """Test cases for ScentMapper."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.mapper = ScentMapper()
    
    def test_initialization(self):
        """Test mapper initialization."""
        assert self.mapper is not None
        assert self.mapper.SCENT_FAMILIES is not None
    
    def test_generate_forest_profile(self):
        """Test profile generation for forest text."""
        text = "The ancient forest was full of pine trees and cedar wood."
        result = self.mapper.generate_profile(text)
        
        assert "primary_scent" in result
        assert "ambient_scents" in result
        assert "blend_recipe" in result
        assert result["primary_scent"]["family"] == "woody"
    
    def test_generate_floral_profile(self):
        """Test profile generation for floral text."""
        text = "The garden was full of roses, jasmine, and lavender flowers."
        result = self.mapper.generate_profile(text)
        
        assert result["primary_scent"]["family"] == "floral"
    
    def test_generate_oceanic_profile(self):
        """Test profile generation for ocean text."""
        text = "The beach waves crashed on the shore, bringing salt and seaweed."
        result = self.mapper.generate_profile(text)
        
        assert result["primary_scent"]["family"] == "oceanic"
    
    def test_generate_citrus_profile(self):
        """Test profile generation for citrus text."""
        text = "Fresh lemon and orange zest filled the sunny kitchen."
        result = self.mapper.generate_profile(text)
        
        assert result["primary_scent"]["family"] == "citrus"
    
    def test_generate_smoky_profile(self):
        """Test profile generation for smoky text."""
        text = "The campfire burned brightly, smoke and ash rising into the night."
        result = self.mapper.generate_profile(text)
        
        assert result["primary_scent"]["family"] == "smoky"
    
    def test_empty_text(self):
        """Test handling of empty text."""
        result = self.mapper.generate_profile("")
        
        assert result["primary_scent"]["intensity"] == 0.0
        assert result["ambient_scents"] == []
    
    def test_intensity_parameter(self):
        """Test intensity parameter."""
        text = "The forest was full of pine trees."
        low_intensity = self.mapper.generate_profile(text, intensity=0.2)
        high_intensity = self.mapper.generate_profile(text, intensity=0.9)
        
        assert low_intensity["primary_scent"]["intensity"] < high_intensity["primary_scent"]["intensity"]
    
    def test_emotion_bias_happy(self):
        """Test emotion bias for happy."""
        text = "A nice day."  # Neutral text
        result = self.mapper.generate_profile(text, emotion="joy")
        
        assert "citrus" in result["detected_families"] or "floral" in result["detected_families"]
    
    def test_emotion_bias_sad(self):
        """Test emotion bias for sad."""
        text = "A quiet place."
        result = self.mapper.generate_profile(text, emotion="sadness")
        
        assert any(f in result["detected_families"] for f in ["woody", "earthy", "oceanic"])
    
    def test_blend_recipe_structure(self):
        """Test blend recipe structure."""
        text = "Forest with flowers and herbs."
        result = self.mapper.generate_profile(text)
        
        assert "channels" in result["blend_recipe"]
        assert "total_intensity" in result["blend_recipe"]
        
        if result["blend_recipe"]["channels"]:
            channel = result["blend_recipe"]["channels"][0]
            assert "family" in channel
            assert "percentage" in channel
            assert "intensity" in channel
            assert "channel_id" in channel
    
    def test_scent_notes(self):
        """Test scent notes inclusion."""
        text = "The rose garden was beautiful."
        result = self.mapper.generate_profile(text)
        
        assert "notes" in result["primary_scent"]
        assert len(result["primary_scent"]["notes"]) > 0
    
    def test_get_family_info(self):
        """Test getting family information."""
        family_info = self.mapper.get_family_info("floral")
        
        assert family_info is not None
        assert "name" in family_info
        assert "keywords" in family_info
        assert "available_scents" in family_info
    
    def test_get_family_info_invalid(self):
        """Test getting info for invalid family."""
        family_info = self.mapper.get_family_info("nonexistent")
        
        assert family_info is None
    
    def test_list_families(self):
        """Test listing all families."""
        families = self.mapper.list_families()
        
        assert "floral" in families
        assert "woody" in families
        assert "citrus" in families
        # Use >= to be resilient to future additions
        assert len(families) >= 10
    
    def test_get_emotion_suggestions(self):
        """Test emotion suggestions."""
        suggestions = self.mapper.get_emotion_suggestions("joy")
        
        assert len(suggestions) > 0
        assert "citrus" in suggestions
    
    def test_multiple_families_detected(self):
        """Test detection of multiple families."""
        text = "The forest had pine trees and roses, with a hint of smoke from the campfire."
        result = self.mapper.generate_profile(text)
        
        assert len(result["detected_families"]) >= 2
    
    def test_convenience_function(self):
        """Test the convenience function."""
        result = generate_scent_profile("A forest with trees.")
        
        assert "primary_scent" in result
        assert "ambient_scents" in result
