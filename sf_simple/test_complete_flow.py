#!/usr/bin/env python3
"""
Complete End-to-End Test for SF Simple
Tests the entire upload → generate → frames flow
"""

import os
import sys
import time
import json
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Test configuration
SERVER_URL = "http://localhost:5001"
TEST_SCREENPLAY = """
127 HOURS

FADE IN:

EXT. CANYON - DAY

ARON, 27, athletic and confident, rappels down into the narrow slot canyon. He wears a blue shirt and carries a backpack.

ARON
This is what I live for.

INT. CANYON - CONTINUOUS  

Aron squeezes through tight spaces between the red rock walls. He checks his climbing gear and water supplies.

A massive boulder shifts and traps his arm against the canyon wall.

ARON
(screaming)
Help! Someone help me!

But no one can hear him in the remote canyon.

FADE OUT.
"""

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{SERVER_URL}/api/projects")
        print(f"✅ Server is running: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Server not running: {e}")
        return False

def test_upload_screenplay():
    """Test screenplay upload"""
    try:
        # Save test screenplay to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(TEST_SCREENPLAY)
            temp_file = f.name
        
        # Upload file
        with open(temp_file, 'rb') as f:
            files = {'file': ('test_screenplay.txt', f, 'text/plain')}
            response = requests.post(f"{SERVER_URL}/upload", files=files)
        
        # Cleanup
        os.unlink(temp_file)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Upload successful: {data['project_id']}")
            print(f"   Detected scenes: {data['detected_scenes']}")
            print(f"   Word count: {data['word_count']}")
            return data['project_id']
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def test_generation(project_id):
    """Test storyboard generation"""
    try:
        # Start generation
        payload = {
            'project_id': project_id,
            'style': 'classic'
        }
        response = requests.post(f"{SERVER_URL}/generate", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Generation started: {data['success']}")
            return True
        else:
            print(f"❌ Generation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False

def test_progress_tracking(project_id, timeout=120):
    """Test progress tracking and frame generation"""
    try:
        start_time = time.time()
        last_progress = 0
        
        while time.time() - start_time < timeout:
            response = requests.get(f"{SERVER_URL}/status/{project_id}")
            
            if response.status_code == 200:
                status = response.json()
                progress = status.get('progress', 0)
                current_step = status.get('current_step', 'Unknown')
                
                if progress > last_progress:
                    print(f"📊 Progress: {progress}% - {current_step}")
                    last_progress = progress
                
                # Check if completed
                if status.get('status') == 'completed':
                    frames = status.get('frames', [])
                    print(f"✅ Generation completed: {len(frames)} frames")
                    
                    # Check frame details
                    for i, frame in enumerate(frames[:3]):  # Check first 3 frames
                        print(f"   Frame {i+1}: {frame['frame_id']}")
                        print(f"      Status: {frame['status']}")
                        print(f"      Image URL: {frame['image_url'][:50]}...")
                        print(f"      Cost: ${frame['cost']}")
                    
                    return True
                
                # Check if error
                if status.get('status') == 'error':
                    print(f"❌ Generation error: {status.get('error', 'Unknown error')}")
                    return False
            
            time.sleep(2)
        
        print(f"❌ Generation timed out after {timeout} seconds")
        return False
        
    except Exception as e:
        print(f"❌ Progress tracking error: {e}")
        return False

def main():
    """Run complete test suite"""
    print("🧪 SF Simple Complete Flow Test")
    print("=" * 50)
    
    # Check environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        return False
    else:
        print(f"✅ API Key loaded: {api_key[:20]}...")
    
    # Test server health
    if not test_server_health():
        print("❌ Server health check failed")
        return False
    
    # Test upload
    project_id = test_upload_screenplay()
    if not project_id:
        print("❌ Upload test failed")
        return False
    
    # Test generation
    if not test_generation(project_id):
        print("❌ Generation test failed")
        return False
    
    # Test progress tracking and frame generation
    if not test_progress_tracking(project_id):
        print("❌ Progress tracking test failed")
        return False
    
    print("\n🎉 All tests passed!")
    print("=" * 50)
    print(f"✅ Upload: Working")
    print(f"✅ Generation: Working") 
    print(f"✅ Frame Images: Working")
    print(f"✅ Progress Tracking: Working")
    print(f"\n🌐 View results: {SERVER_URL}/storyboard/{project_id}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)