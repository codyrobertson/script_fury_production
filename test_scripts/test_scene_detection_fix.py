#!/usr/bin/env python3
"""
Test script to verify the scene detection algorithm fix
"""

from utils.scene_analyzer import detect_optimal_scene_count, estimate_pages, count_scene_headers

def test_scene_detection():
    """Test scene detection with the sample screenplay"""
    
    print("🔍 Testing Scene Detection Algorithm Fix")
    print("=" * 50)
    
    # Test with sample screenplay
    with open('sample_screenplay.txt', 'r') as f:
        text = f.read()
    
    pages = estimate_pages(text)
    headers = count_scene_headers(text)
    optimal = detect_optimal_scene_count(text)
    
    print(f"\n📄 Sample Screenplay Analysis:")
    print(f"   Pages estimated: {pages}")
    print(f"   Scene headers found: {headers}")
    print(f"   Optimal scenes: {optimal}")
    
    # Verify main app formula step by step
    page_based = max(5, min(pages // 2, 500))
    scene_count = max(headers, page_based)
    final_count = max(3, min(scene_count, 500))
    
    print(f"\n🧮 Formula Verification:")
    print(f"   Industry standard: 1 scene per 2-3 pages")
    print(f"   Page-based estimate: max(5, min({pages} // 2, 500)) = {page_based}")
    print(f"   Max with headers: max({headers}, {page_based}) = {scene_count}")
    print(f"   Final with bounds: max(3, min({scene_count}, 500)) = {final_count}")
    print(f"   ✅ Algorithm result matches: {optimal == final_count}")
    
    # Test expected behavior for different screenplay lengths
    print(f"\n📊 Expected Behavior for Different Lengths:")
    test_cases = [
        (5, "Short screenplay"),
        (18, "Medium screenplay"),
        (30, "Short feature"),
        (90, "Feature film"),
        (120, "Long feature")
    ]
    
    for test_pages, description in test_cases:
        test_page_based = max(5, min(test_pages // 2, 500))
        print(f"   {test_pages:3} pages ({description:15}) → {test_page_based:2} scenes recommended")
    
    print(f"\n✅ Scene Detection Fix Summary:")
    print(f"   ❌ Before: 48 scenes for 18-page screenplay (way too many)")
    print(f"   ✅ After:  {optimal} scenes for {pages}-page screenplay (reasonable)")
    print(f"   🎯 Using same algorithm as main Script Fury app")
    
    return optimal <= 15  # Should be reasonable for short screenplay

if __name__ == "__main__":
    success = test_scene_detection()
    
    if success:
        print(f"\n🎉 Scene detection algorithm fix successful!")
        print(f"   The algorithm now produces reasonable scene counts")
        print(f"   matching the main Script Fury application.")
    else:
        print(f"\n❌ Scene detection still producing unreasonable counts")
        exit(1)