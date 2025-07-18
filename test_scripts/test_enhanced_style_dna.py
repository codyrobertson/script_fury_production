#!/usr/bin/env python3
"""
Test Enhanced STYLE DNA for consistency issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.storyboard_generator import get_style_dna

def test_enhanced_style_dna():
    """Test the enhanced STYLE DNA includes all new elements"""
    print("🎨 ENHANCED STYLE DNA TEST")
    print("=" * 60)
    
    # Test different style prompts
    test_styles = ["classic", "cinematic", "sketch", "comic"]
    
    for style in test_styles:
        print(f"\n🎭 Testing {style.upper()} style...")
        
        style_dna = get_style_dna(style)
        print(f"Style DNA length: {len(style_dna)} characters")
        
        # Check for key elements
        required_elements = [
            "black and white line art only",
            "Clean vector-like lines",
            "no shading, no gradients",
            "STRICTLY black and white",
            "Simple line-based lighting",
            "identical line art style",
            "STRICTLY monochrome black and white only",
            "Same facial features",
            "Minimal background details",
            "NO photographic elements"
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in style_dna:
                missing_elements.append(element)
                
        if missing_elements:
            print(f"   ❌ Missing elements: {len(missing_elements)}")
            for missing in missing_elements:
                print(f"      - {missing}")
        else:
            print(f"   ✅ All elements present")
            
        # Check specific improvements
        improvements = {
            "Lighting control": "Simple line-based lighting" in style_dna,
            "Skin tone consistency": "identical line art style" in style_dna,
            "Color accuracy": "STRICTLY monochrome" in style_dna,
            "Character consistency": "Same facial features" in style_dna,
            "Background simplicity": "Minimal background details" in style_dna,
            "Anti-photorealism": "NO photographic elements" in style_dna
        }
        
        print(f"   📊 Improvements included:")
        for improvement, present in improvements.items():
            status = "✅" if present else "❌"
            print(f"      {status} {improvement}")
            
    print(f"\n💡 SAMPLE STYLE DNA (Classic):")
    sample_dna = get_style_dna("classic")
    print(f"   {sample_dna[:200]}...")
    print(f"   Total length: {len(sample_dna)} characters")
    
    # Validate no color leakage terms
    print(f"\n🚫 COLOR LEAKAGE PREVENTION:")
    color_terms = ["color", "colored", "shade", "shading", "gradient", "photorealistic", "realistic rendering"]
    prevention_terms = ["black and white", "monochrome", "line art", "NO photographic", "pure line art"]
    
    for term in color_terms:
        if term in sample_dna.lower():
            print(f"   ⚠️  Found color term: {term}")
    
    prevention_count = sum(1 for term in prevention_terms if term in sample_dna.lower())
    print(f"   ✅ Prevention terms: {prevention_count}/{len(prevention_terms)}")
    
    print(f"\n🎉 ENHANCED STYLE DNA TEST COMPLETE!")
    return True

if __name__ == "__main__":
    success = test_enhanced_style_dna()
    exit(0 if success else 1)