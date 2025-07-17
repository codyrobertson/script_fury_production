#!/usr/bin/env python3
"""
Test the enhanced style characteristics for each variation
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.storyboard_generator import get_style_dna

def test_enhanced_styles():
    """Test each style has the correct enhanced characteristics"""
    print("🎨 ENHANCED STYLE CHARACTERISTICS TEST")
    print("=" * 80)
    
    # Test each style for specific requirements
    style_tests = {
        'classic': {
            'name': 'CLASSIC',
            'requirements': [
                'black and white line art only',
                'Clean vector-like lines',
                'no shading, no gradients'
            ],
            'description': 'Pure professional storyboard style'
        },
        'cinematic': {
            'name': 'CINEMATIC', 
            'requirements': [
                'dramatic composition',
                'film-style framing',
                'CINEMATIC EXCEPTION: allow monochrome grays and gradients for depth'
            ],
            'description': 'Film-style with monochrome depth allowed'
        },
        'sketch': {
            'name': 'SKETCH',
            'requirements': [
                'hand-drawn ink pen sketch appearance',
                'organic ink pen strokes', 
                'loose artistic ink lines',
                'pen and ink illustration style'
            ],
            'description': 'Ink pen sketch style with organic strokes'
        },
        'comic': {
            'name': 'COMIC',
            'requirements': [
                'inky dramatic comic book panel style',
                'bold inky lines',
                'high contrast ink work',
                'dynamic dramatic panels',
                'graphic novel ink illustration'
            ],
            'description': 'Bold dramatic comic book ink style'
        }
    }
    
    all_passed = True
    
    for style_key, test_data in style_tests.items():
        print(f"\n🎭 {test_data['name']} STYLE TEST")
        print("-" * 60)
        
        dna = get_style_dna(style_key)
        print(f"📏 Length: {len(dna)} characters")
        print(f"📝 Description: {test_data['description']}")
        
        # Check style-specific requirements
        missing_requirements = []
        for requirement in test_data['requirements']:
            if requirement not in dna:
                missing_requirements.append(requirement)
                
        if missing_requirements:
            print(f"❌ Missing requirements: {len(missing_requirements)}")
            for req in missing_requirements:
                print(f"   - {req}")
            all_passed = False
        else:
            print(f"✅ All style requirements present ({len(test_data['requirements'])})")
            
        # Check universal consistency controls
        universal_controls = [
            'maintain identical character features',
            'same facial proportions',
            'consistent line art style throughout all frames'
        ]
        
        missing_controls = []
        for control in universal_controls:
            if control not in dna:
                missing_controls.append(control)
                
        if missing_controls:
            print(f"❌ Missing consistency controls: {len(missing_controls)}")
            for control in missing_controls:
                print(f"   - {control}")
            all_passed = False
        else:
            print(f"✅ All consistency controls present")
            
        # Show key style elements
        print(f"🎨 Key style elements found:")
        for requirement in test_data['requirements']:
            if requirement in dna:
                print(f"   ✅ {requirement}")
                
    # Special validation for cinematic grays/gradients exception
    print(f"\n🎬 CINEMATIC SPECIAL VALIDATION")
    print("-" * 60)
    
    cinematic_dna = get_style_dna('cinematic')
    
    if 'allow monochrome grays and gradients for depth' in cinematic_dna:
        print(f"✅ Cinematic gray/gradient exception properly specified")
    else:
        print(f"❌ Missing cinematic gray/gradient exception")
        all_passed = False
        
    # Check that other styles don't have the exception
    for style in ['classic', 'sketch', 'comic']:
        style_dna = get_style_dna(style)
        if 'allow monochrome grays and gradients' in style_dna:
            print(f"❌ {style.upper()} incorrectly has gray/gradient exception")
            all_passed = False
        else:
            print(f"✅ {style.upper()} correctly restricts grays/gradients")
            
    # Ink characteristics validation
    print(f"\n🖋️  INK CHARACTERISTICS VALIDATION")
    print("-" * 60)
    
    sketch_dna = get_style_dna('sketch')
    comic_dna = get_style_dna('comic')
    
    sketch_ink_terms = ['ink pen', 'organic ink pen strokes', 'pen and ink illustration']
    comic_ink_terms = ['inky dramatic', 'bold inky lines', 'high contrast ink work']
    
    sketch_ink_count = sum(1 for term in sketch_ink_terms if term in sketch_dna)
    comic_ink_count = sum(1 for term in comic_ink_terms if term in comic_dna)
    
    print(f"SKETCH ink characteristics: {sketch_ink_count}/{len(sketch_ink_terms)} ({'✅' if sketch_ink_count == len(sketch_ink_terms) else '❌'})")
    print(f"COMIC ink characteristics: {comic_ink_count}/{len(comic_ink_terms)} ({'✅' if comic_ink_count == len(comic_ink_terms) else '❌'})")
    
    if sketch_ink_count < len(sketch_ink_terms) or comic_ink_count < len(comic_ink_terms):
        all_passed = False
        
    # Final result
    print(f"\n🎯 FINAL RESULT")
    print("=" * 80)
    
    if all_passed:
        print(f"🎉 ALL STYLE ENHANCEMENTS SUCCESSFUL!")
        print(f"   ✅ CLASSIC: Pure professional storyboard")
        print(f"   ✅ CINEMATIC: Film-style with monochrome depth")
        print(f"   ✅ SKETCH: Organic ink pen illustration") 
        print(f"   ✅ COMIC: Bold dramatic ink work")
        print(f"   ✅ All styles maintain character consistency")
        return True
    else:
        print(f"❌ Some style enhancements failed validation")
        return False

if __name__ == "__main__":
    success = test_enhanced_styles()
    exit(0 if success else 1)