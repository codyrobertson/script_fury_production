#!/usr/bin/env python3
"""
Quick test to verify core functionality is working
"""

import requests
import json
import time
import os

def test_core_functionality():
    """Test the core functionality of the app"""
    
    base_url = "http://localhost:5001"
    
    # Test 1: Upload a screenplay
    print("🔄 Testing file upload...")
    
    # Create a simple screenplay
    screenplay = """
FADE IN:

EXT. PARK - DAY

A beautiful park on a sunny day. ALICE (25), a young woman, sits on a bench reading a book.

ALICE
(to herself)
Such a lovely day.

A DOG runs up to her and starts barking.

ALICE (CONT'D)
Hello there, little fellow.

FADE OUT.
"""
    
    # Save to temp file
    with open('/tmp/test_screenplay.txt', 'w') as f:
        f.write(screenplay)
    
    # Upload file
    with open('/tmp/test_screenplay.txt', 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{base_url}/upload", files=files)
    
    if response.status_code == 200:
        data = response.json()
        project_id = data['project_id']
        print(f"   ✅ Upload successful: {project_id}")
        print(f"   📊 Word count: {data['word_count']}")
        print(f"   📊 Character count: {data['char_count']}")
    else:
        print(f"   ❌ Upload failed: {response.status_code}")
        return False
    
    # Test 2: Generate storyboard
    print("\n🎨 Testing storyboard generation...")
    
    generation_data = {
        'project_id': project_id,
        'style': 'classic',
        'frame_density': 'medium'
    }
    
    response = requests.post(f"{base_url}/generate", json=generation_data)
    
    if response.status_code == 200:
        print("   ✅ Generation started successfully")
    else:
        print(f"   ❌ Generation failed: {response.status_code}")
        return False
    
    # Test 3: Check status
    print("\n📊 Checking generation status...")
    
    # Wait a bit and check status
    time.sleep(2)
    
    response = requests.get(f"{base_url}/status/{project_id}")
    
    if response.status_code == 200:
        status = response.json()
        print(f"   Status: {status['status']}")
        print(f"   Progress: {status['progress']}%")
        print(f"   Current step: {status['current_step']}")
        
        # If completed, show frame count
        if status['status'] == 'completed':
            print(f"   🎉 Frames generated: {len(status['frames'])}")
        
    else:
        print(f"   ❌ Status check failed: {response.status_code}")
        return False
    
    # Test 4: Check processing page
    print("\n📄 Testing processing page...")
    
    response = requests.get(f"{base_url}/processing/{project_id}")
    
    if response.status_code == 200:
        print("   ✅ Processing page accessible")
    else:
        print(f"   ❌ Processing page failed: {response.status_code}")
        return False
    
    # Cleanup
    os.remove('/tmp/test_screenplay.txt')
    
    print("\n🎉 All core functionality tests passed!")
    return True

if __name__ == "__main__":
    try:
        success = test_core_functionality()
        if success:
            print("\n✅ Core functionality is working correctly!")
        else:
            print("\n❌ Some tests failed")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Make sure the Flask app is running on port 5001")