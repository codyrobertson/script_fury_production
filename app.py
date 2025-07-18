#!/usr/bin/env python3
"""
Script Fury Simple - A streamlined storyboard generator
Demonstrates core functionality without complex infrastructure
"""

import os
import json
import asyncio
import threading
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create logger for this module
logger = logging.getLogger('sf_simple')
if os.getenv('SF_SIMPLE_ENABLE_DETAILED_LOGGING', 'false').lower() == 'true':
    logger.setLevel(logging.DEBUG)

# Suppress Flask's default logging for cleaner output
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Import our simple utilities
from utils.text_extractor import extract_text_from_file
from utils.scene_analyzer import analyze_screenplay
from utils.storyboard_generator import generate_storyboard_frames
from utils.print_generator import generate_printable_storyboard

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simple in-memory storage
projects = {}
generation_status = {}

# Styles available
STYLES = {
    'classic': {
        'name': 'Classic Storyboard',
        'description': 'Traditional black and white line art',
        'prompt_style': 'Professional storyboard, black and white line art, clean vector-like lines'
    },
    'cinematic': {
        'name': 'Cinematic',
        'description': 'Film-style composition and framing',
        'prompt_style': 'Cinematic storyboard, dramatic composition, film-style framing'
    },
    'sketch': {
        'name': 'Sketch Style',
        'description': 'Hand-drawn sketch appearance',
        'prompt_style': 'Hand-drawn sketch storyboard, loose artistic lines, sketchy style'
    },
    'comic': {
        'name': 'Comic Book',
        'description': 'Comic book panel style',
        'prompt_style': 'Comic book storyboard, dynamic panels, graphic novel style'
    }
}

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/')
def upload_page():
    """Upload page - start of the flow"""
    return render_template('upload_main.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and text extraction"""
    try:
        logger.info("📁 File upload started")
        
        if 'file' not in request.files:
            logger.warning("❌ No file provided in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.warning("❌ No file selected")
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"📄 File saved: {filename} ({os.path.getsize(filepath)} bytes)")
        
        # Extract text
        logger.info("🔍 Extracting text from file...")
        text = extract_text_from_file(filepath)
        
        # Clean up file
        os.remove(filepath)
        
        if not text:
            logger.error("❌ Could not extract text from file")
            return jsonify({'error': 'Could not extract text from file'}), 400
        
        logger.info(f"✅ Text extracted: {len(text)} characters, {len(text.split())} words")
        
        # Quick analysis to get scene count
        logger.info("🎬 Detecting optimal scene count...")
        from utils.scene_analyzer import detect_optimal_scene_count
        detected_scenes = detect_optimal_scene_count(text)
        logger.info(f"📊 Scene detection complete: {detected_scenes} scenes detected")
        
        # Create project
        project_id = str(uuid.uuid4())
        projects[project_id] = {
            'id': project_id,
            'filename': filename,
            'text': text,
            'created_at': datetime.now().isoformat(),
            'word_count': len(text.split()),
            'char_count': len(text),
            'detected_scenes': detected_scenes
        }
        
        logger.info(f"🆔 Project created: {project_id}")
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'filename': filename,
            'word_count': len(text.split()),
            'char_count': len(text),
            'text_length': len(text),
            'detected_scenes': detected_scenes
        })
    
    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate/<project_id>')
def generate_page(project_id):
    """Generate page - style selection and generation"""
    if project_id not in projects:
        return "Project not found", 404
    
    project = projects[project_id]
    return render_template('generate_main.html', project=project, styles=STYLES)

@app.route('/generate', methods=['POST'])
def generate_storyboard():
    """Start storyboard generation with automatic scene detection"""
    try:
        data = request.json
        project_id = data.get('project_id')
        style = data.get('style', 'classic')
        
        logger.info(f"🎬 Generation started for project {project_id} with style '{style}'")
        
        if project_id not in projects:
            logger.error(f"❌ Project not found: {project_id}")
            return jsonify({'error': 'Project not found'}), 404
        
        project = projects[project_id]
        logger.info(f"📄 Project loaded: {project['filename']} ({project['word_count']} words)")
        
        # Initialize generation status
        generation_status[project_id] = {
            'status': 'analyzing',
            'progress': 0,
            'current_step': 'Analyzing screenplay and detecting optimal scenes...',
            'total_steps': 3,
            'current_step_num': 1,
            'scenes': [],
            'frames': [],
            'analysis': None,
            'style': style,
            'started_at': datetime.now().isoformat()
        }
        
        logger.info(f"📊 Generation status initialized for {project_id}")
        
        # Start generation in background thread
        def generate_async():
            try:
                # OPTIMIZATION: Skip redundant AI analysis since we already detected scenes during upload
                # Old flow: Upload (detect scenes) → Generate (re-analyze same text?!) → Frames
                # New flow: Upload (detect scenes) → Generate (use cached count) → Frames IMMEDIATELY
                
                # Step 1: Create fast basic analysis (skip redundant AI analysis)
                if project_id in generation_status:
                    word_count = project['word_count']
                    if word_count > 20000:
                        generation_status[project_id]['current_step'] = 'Analyzing large script (optimized for speed)...'
                    elif word_count > 8000:
                        generation_status[project_id]['current_step'] = 'Analyzing medium script...'
                    else:
                        generation_status[project_id]['current_step'] = 'Analyzing script...'
                    generation_status[project_id]['progress'] = 10
                
                logger.info(f"🚀 Skipping redundant AI analysis - using basic scene extraction for {project['detected_scenes']} scenes")
                
                # FIXED: Use fast targeted AI analysis instead of garbage pattern matching
                from utils.scene_analyzer import fast_ai_analyze_screenplay
                
                # Update progress for AI analysis
                if project_id in generation_status:
                    generation_status[project_id]['current_step'] = 'Extracting characters and story beats with AI...'
                    generation_status[project_id]['progress'] = 20
                
                analysis = fast_ai_analyze_screenplay(project['text'], project['detected_scenes'])
                
                if project_id in generation_status:
                    generation_status[project_id]['current_step'] = f'Analysis complete! Ready to generate {analysis["total_scenes"]} scenes!'
                    generation_status[project_id]['progress'] = 30
                    generation_status[project_id]['analysis'] = analysis
                
                logger.info(f"⚡ Fast analysis complete: {analysis['total_scenes']} scenes, {len(analysis['characters'])} characters")
                
                print(f"📊 Analysis complete: {analysis['total_scenes']} scenes, {len(analysis['characters'])} characters")
                
                # Step 2: Generate frames with live updates  
                if project_id in generation_status:
                    generation_status[project_id]['current_step'] = f'Starting frame generation for {analysis["total_scenes"]} scenes...'
                    generation_status[project_id]['current_step_num'] = 2
                    generation_status[project_id]['progress'] = 40
                
                # FRAME GENERATION: Start immediately with real AI images
                
                # FIXED: Robust frame generation with proper error handling
                frames = []
                total_scenes = len(analysis['scenes'])
                
                print(f"🎬 Starting generation for {total_scenes} scenes...")
                
                try:
                    # Calculate total frames needed based on intelligent analysis
                    total_frames_needed = sum(scene.get('frames_needed', 1) for scene in analysis['scenes'])
                    current_frame_index = 0
                    
                    print(f"🎬 Intelligent generation: {total_frames_needed} total frames for {total_scenes} scenes")
                    
                    for scene_index, scene in enumerate(analysis['scenes']):
                        if project_id not in generation_status:
                            print("❌ Generation cancelled - project removed")
                            break
                        
                        # Variable frames per scene based on AI analysis
                        frames_for_scene = scene.get('frames_needed', 1)
                        scene_type = scene.get('scene_type', 'dialogue')
                        visual_complexity = scene.get('visual_complexity', 'simple')
                        
                        print(f"🎬 Scene {scene['scene_number']} ({scene_type}, {visual_complexity}): {frames_for_scene} frames")
                        
                        # Generate frames for this scene
                        for frame_num in range(frames_for_scene):
                            if project_id not in generation_status:
                                break
                            
                            current_frame_index += 1
                            progress = 45 + (current_frame_index / total_frames_needed * 50)  # 45% to 95%
                            
                            generation_status[project_id].update({
                                'current_step': f'Generating frame {current_frame_index} of {total_frames_needed} - Scene {scene["scene_number"]}.{frame_num + 1}: {scene["location"]}',
                                'progress': progress,
                                'current_frame': current_frame_index,
                                'total_frames': total_frames_needed
                            })
                            
                            # Generate individual frame with REAL AI images and character consistency
                            try:
                                from utils.storyboard_generator import generate_ai_frame_sync
                                frame = generate_ai_frame_sync(scene, frame_num + 1, STYLES[style]['prompt_style'], analysis)
                                frames.append(frame)
                                
                                # Update frames in real-time
                                generation_status[project_id]['frames'] = frames.copy()
                                
                                print(f"   ✅ Generated frame {current_frame_index}: {frame['frame_id']} ({scene_type})")
                                
                            except Exception as frame_error:
                                print(f"   ❌ Frame {current_frame_index} failed: {frame_error}")
                                # Continue with other frames
                                continue
                            
                            time.sleep(0.1)  # Minimal delay for UI updates
                
                except Exception as gen_error:
                    print(f"❌ Generation loop failed: {gen_error}")
                    if project_id in generation_status:
                        generation_status[project_id]['status'] = 'error'
                        generation_status[project_id]['error'] = str(gen_error)
                    return
                
                print(f"🎉 Generation complete: {len(frames)} frames")
                
                # Step 3: Complete
                if project_id in generation_status:
                    generation_status[project_id]['current_step'] = f'Generation complete! Created {len(frames)} frames.'
                    generation_status[project_id]['current_step_num'] = 3
                    generation_status[project_id]['status'] = 'completed'
                    generation_status[project_id]['progress'] = 100
                    generation_status[project_id]['frames'] = frames
                    generation_status[project_id]['completed_at'] = datetime.now().isoformat()
                
            except Exception as e:
                if project_id in generation_status:
                    generation_status[project_id]['status'] = 'error'
                    generation_status[project_id]['error'] = str(e)
                    generation_status[project_id]['current_step'] = f'Error: {str(e)}'
        
        # Start generation thread
        thread = threading.Thread(target=generate_async)
        thread.start()
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'message': 'Generation started'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/processing/<project_id>')
def processing_page(project_id):
    """Processing page - track progress and view results"""
    if project_id not in projects:
        return "Project not found", 404
    
    project = projects[project_id]
    status = generation_status.get(project_id, {})
    
    return render_template('processing_main.html', 
                         project=project, 
                         status=status,
                         styles=STYLES)

@app.route('/storyboard/<project_id>')
def storyboard_gallery(project_id):
    """Storyboard gallery page - view all frames in a proper gallery"""
    if project_id not in projects:
        return "Project not found", 404
    
    project = projects[project_id]
    status = generation_status.get(project_id, {})
    
    # Allow access if there are any frames, even if not fully completed
    if not status or not status.get('frames'):
        return render_template('storyboard_waiting.html', project=project)
    
    return render_template('storyboard.html', 
                         project=project, 
                         status=status,
                         frames=status.get('frames', []),
                         analysis=status.get('analysis', {}))

@app.route('/status/<project_id>')
def get_status(project_id):
    """Get generation status for polling"""
    if project_id not in generation_status:
        return jsonify({'error': 'Status not found'}), 404
    
    return jsonify(generation_status[project_id])

@app.route('/print/<project_id>')
def print_storyboard(project_id):
    """Generate printable version of storyboard"""
    if project_id not in projects:
        return "Project not found", 404
    
    if project_id not in generation_status or generation_status[project_id]['status'] != 'completed':
        return "Generation not completed", 400
    
    project = projects[project_id]
    status = generation_status[project_id]
    
    # Generate printable HTML
    printable_html = generate_printable_storyboard(project, status)
    
    # Import the print styles function
    from utils.print_generator import get_print_styles
    
    return render_template('print.html', 
                         project=project, 
                         status=status,
                         printable_html=printable_html,
                         get_print_styles=get_print_styles)

@app.route('/api/projects')
def list_projects():
    """List all projects (for debugging)"""
    return jsonify({
        'projects': list(projects.values()),
        'generation_status': generation_status
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Script Fury Simple starting...")
    print("📁 Upload folder:", app.config['UPLOAD_FOLDER'])
    print(f"🌐 Visit: http://localhost:{port}")
    print("📖 Flow: Upload → Generate → Processing → Print")
    
    app.run(debug=debug, host='0.0.0.0', port=port)