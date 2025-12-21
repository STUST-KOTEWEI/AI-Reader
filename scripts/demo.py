#!/usr/bin/env python3
"""
Demo script for Project-HOLO modules.

Run this script to see a demonstration of all the core features.
"""

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from holo.ingestion.text_segmenter import TextSegmenter
from holo.nlp.emotion_analyzer import EmotionAnalyzer
from holo.sensory.haptics_emulator import HapticsEmulator
from holo.visual.image_generator import ImageConceptGenerator
from holo.olfactory.scent_mapper import ScentMapper


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_text_segmentation(text: str):
    """Demonstrate text segmentation."""
    print_section("Text Segmentation")
    
    segmenter = TextSegmenter()
    result = segmenter.get_segments_with_metadata(text)
    
    print(f"Strategy: {result['strategy_used']}")
    print(f"Total segments: {result['total_segments']}")
    print(f"Total length: {result['total_length']} characters")
    print("\nSegments:")
    for seg in result['segments'][:3]:
        print(f"  [{seg['index']}] {seg['text'][:50]}...")


def demo_emotion_analysis(text: str):
    """Demonstrate emotion analysis."""
    print_section("Emotion Analysis")
    
    analyzer = EmotionAnalyzer()
    result = analyzer.analyze(text)
    
    print(f"Primary emotion: {result['primary_emotion']} (confidence: {result['confidence']:.2f})")
    print(f"Intensity: {result['intensity']:.2f}")
    print(f"Sentiment: polarity={result['sentiment']['polarity']:.2f}, subjectivity={result['sentiment']['subjectivity']:.2f}")
    print("\nEmotion scores:")
    for emotion, score in result['emotions'].items():
        if score > 0:
            print(f"  {emotion}: {score:.3f}")


def demo_haptics(text: str):
    """Demonstrate haptic pattern generation."""
    print_section("Haptic Feedback Generation")
    
    emulator = HapticsEmulator()
    pattern = emulator.generate_from_text(text)
    
    print(f"Pattern name: {pattern['name']}")
    print(f"Total events: {len(pattern['events'])}")
    print("\nHaptic events (first 5):")
    for event in pattern['events'][:5]:
        print(f"  Time: {event['time']}ms, Intensity: {event['intensity']:.1f}, Duration: {event['duration']}ms")
    
    # Also demo emotion-based haptics
    analyzer = EmotionAnalyzer()
    emotion, intensity = analyzer.get_emotion_for_haptics(text)
    emotion_pattern = emulator.generate_from_emotion(emotion, intensity)
    
    print(f"\nEmotion-based pattern ({emotion}):")
    print(f"  Events: {len(emotion_pattern['events'])}")


def demo_visual_concepts(text: str):
    """Demonstrate visual concept generation."""
    print_section("Visual Concept Generation")
    
    generator = ImageConceptGenerator()
    result = generator.generate_concepts(text)
    
    print(f"Scene: {result['scene_description']}")
    print(f"Mood: {result['mood']}")
    print(f"Lighting: {result['lighting']}")
    print(f"Composition: {result['composition_suggestion']}")
    print(f"\nColor palette: {', '.join(result['color_palette'][:5])}")
    print("\nVisual concepts:")
    for concept in result['concepts'][:3]:
        print(f"  - {concept['element']} ({concept['category']})")


def demo_scent_mapping(text: str):
    """Demonstrate scent mapping."""
    print_section("Scent Profile Generation")
    
    mapper = ScentMapper()
    result = mapper.generate_profile(text)
    
    primary = result['primary_scent']
    print(f"Primary scent: {primary['name']} ({primary['family']})")
    print(f"  Intensity: {primary['intensity']:.2f}")
    print(f"  Notes: {', '.join(primary['notes'])}")
    
    if result['ambient_scents']:
        print("\nAmbient scents:")
        for scent in result['ambient_scents']:
            print(f"  - {scent['name']} ({scent['family']}) @ {scent['intensity']:.2f}")
    
    print(f"\nDetected families: {', '.join(result['detected_families'])}")


def main():
    """Run the demo."""
    print("\n" + "=" * 60)
    print("  Project-HOLO Feature Demonstration")
    print("=" * 60)
    
    # Sample narrative text
    sample_text = """
    The ancient forest stretched endlessly before her, its towering trees 
    reaching toward a sky painted in hues of amber and gold. A gentle breeze 
    carried the scent of pine and wildflowers as she stepped onto the 
    moss-covered path. She felt happy and excited about the adventure ahead!
    
    Somewhere in the distance, a mysterious stream whispered secrets to the 
    stones. Strange shadows danced between the trees. This was the beginning 
    of her greatest adventure. She was ready!
    """
    
    print(f"\nInput text ({len(sample_text)} characters):")
    print("-" * 40)
    print(sample_text[:200] + "...")
    
    # Run all demonstrations
    demo_text_segmentation(sample_text)
    demo_emotion_analysis(sample_text)
    demo_haptics(sample_text)
    demo_visual_concepts(sample_text)
    demo_scent_mapping(sample_text)
    
    print_section("Demo Complete!")
    print("All Project-HOLO modules are working correctly.")
    print("\nFor more information, see the documentation in /docs/")


if __name__ == "__main__":
    main()
