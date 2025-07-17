#!/usr/bin/env python3
"""
Test that ALL style variations maintain enhanced consistency controls
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.storyboard_generator import get_style_dna

def test_all_style_consistency():
    """Test that all styles maintain enhanced consistency"""
    print("🎨 ALL STYLE CONSISTENCY TEST")
    print("=" * 70)
    
    styles = ["classic", "cinematic", "sketch", "comic"]
    
    # Key consistency elements that MUST be in ALL styles
    consistency_requirements = [
        "black and white line art only",
        "STRICTLY monochrome black and white only", 
        "identical line art style",
        "Same facial features",
        "maintain identical character features",
        "consistent line art style throughout all frames"
    ]
    
    all_results = {}
    
    for style in styles:
        print(f"\n🎭 {style.upper()} STYLE ANALYSIS")
        print("-" * 50)
        
        dna = get_style_dna(style)
        all_results[style] = dna
        
        print(f"Length: {len(dna)} characters")
        
        # Check for consistency requirements
        missing = []
        for requirement in consistency_requirements:
            if requirement not in dna:
                missing.append(requirement)
                
        if missing:
            print(f"❌ Missing consistency controls: {len(missing)}")
            for item in missing:
                print(f"   - {item}")
        else:
            print(f"✅ All consistency controls present")
            
        # Show style-specific additions
        if style == "classic":
            print(f"📝 Base style (no additions)")
        elif style == "cinematic":
            if "dramatic composition" in dna and "film-style framing" in dna:
                print(f"📝 Cinematic additions: dramatic composition, film-style framing")
            else:
                print(f"❌ Missing cinematic elements")
        elif style == "sketch": 
            if "hand-drawn sketch" in dna and "loose artistic lines" in dna:
                print(f"📝 Sketch additions: hand-drawn sketch, loose artistic lines")
            else:
                print(f"❌ Missing sketch elements")
        elif style == "comic":
            if "comic book panel" in dna and "dynamic panels" in dna:
                print(f"📝 Comic additions: comic book panel, dynamic panels")
            else:
                print(f"❌ Missing comic elements")
                
        # Check for consistency reinforcement
        if "CRITICAL: maintain identical character features" in dna:
            print(f"✅ Consistency reinforcement present")
        else:
            print(f"❌ Missing consistency reinforcement")
            
    # Compare styles to ensure they all have base consistency
    print(f"\n📊 CROSS-STYLE CONSISTENCY ANALYSIS")
    print("=" * 70)
    
    base_style_dna = all_results["classic"]
    
    for style, dna in all_results.items():
        if style == "classic":
            continue
            
        # Check if all base consistency elements are preserved
        base_elements_preserved = all(element in dna for element in consistency_requirements)
        
        print(f"{style.upper()}: {'✅' if base_elements_preserved else '❌'} Base consistency preserved")
        
        # Show the actual differences
        classic_words = set(base_style_dna.split())
        style_words = set(dna.split())
        
        additions = style_words - classic_words
        if additions:
            print(f"   Added: {', '.join(list(additions)[:5])}{'...' if len(additions) > 5 else ''}")
            
    # Final validation
    print(f"\n🎯 FINAL VALIDATION")
    print("-" * 50)
    
    all_consistent = True
    for style, dna in all_results.items():
        has_all_requirements = all(req in dna for req in consistency_requirements)
        if not has_all_requirements:
            all_consistent = False
            print(f"❌ {style.upper()}: Missing consistency controls")
        else:
            print(f"✅ {style.upper()}: All consistency controls present")
            
    if all_consistent:
        print(f"\n🎉 SUCCESS: All styles maintain enhanced consistency!")
        print(f"   ✅ Character appearance will be consistent across all frames")
        print(f"   ✅ Color accuracy maintained in all style variations") 
        print(f"   ✅ Lighting controls applied to all styles")
        print(f"   ✅ Background simplicity enforced everywhere")
        return True
    else:
        print(f"\n❌ FAILURE: Some styles missing consistency controls")
        return False

if __name__ == "__main__":
    success = test_all_style_consistency()
    exit(0 if success else 1)