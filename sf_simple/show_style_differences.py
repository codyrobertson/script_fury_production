#!/usr/bin/env python3
"""
Show the actual DNA differences between styles
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.storyboard_generator import get_style_dna

def show_style_differences():
    """Show what makes each style unique while maintaining consistency"""
    print("🎨 STYLE DNA DIFFERENCES")
    print("=" * 80)
    
    styles = ["classic", "cinematic", "sketch", "comic"]
    
    for style in styles:
        print(f"\n🎭 {style.upper()} STYLE DNA")
        print("-" * 60)
        
        dna = get_style_dna(style)
        
        # Break into readable chunks
        chunks = dna.split(", ")
        
        print(f"📏 Length: {len(dna)} characters")
        print(f"🧬 DNA Components:")
        
        for i, chunk in enumerate(chunks, 1):
            if i <= 6:
                print(f"   {i:2d}. {chunk}")
            elif "dramatic composition" in chunk or "hand-drawn" in chunk or "comic book" in chunk:
                print(f"   🎨 STYLE: {chunk}")
            elif "CRITICAL" in chunk:
                print(f"   🔒 CONSISTENCY: {chunk}")
            elif i == len(chunks):
                print(f"   🔒 FINAL: {chunk}")
                
        print()

def compare_styles():
    """Compare what's unique to each style"""
    print("\n🔍 STYLE COMPARISON")
    print("=" * 80)
    
    classic_dna = get_style_dna("classic")
    
    styles = {
        "cinematic": get_style_dna("cinematic"),
        "sketch": get_style_dna("sketch"), 
        "comic": get_style_dna("comic")
    }
    
    for style_name, style_dna in styles.items():
        print(f"\n🆚 {style_name.upper()} vs CLASSIC")
        print("-" * 40)
        
        # Find what's added
        classic_parts = set(classic_dna.split(", "))
        style_parts = set(style_dna.split(", "))
        
        additions = style_parts - classic_parts
        
        print(f"✨ Unique additions ({len(additions)}):")
        for addition in sorted(additions):
            if len(addition) > 5:  # Skip tiny fragments
                print(f"   + {addition}")
                
    print(f"\n💡 KEY INSIGHT:")
    print(f"   🎯 ALL styles share the same enhanced consistency base")
    print(f"   🎨 Each style adds unique visual elements")
    print(f"   🔒 All styles enforce identical character/color/lighting rules")

if __name__ == "__main__":
    show_style_differences()
    compare_styles()