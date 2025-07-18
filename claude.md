# Script Fury Simple - AI Assistant Project Guide

## 🎯 Project Overview
**Script Fury Simple** is a production-ready AI-powered storyboard generator that converts screenplays into professional black & white storyboard frames using OpenAI's GPT models.

### Core System Architecture
```
sf_simple/
├── app.py                          # Main Flask application
├── utils/                          # Core utilities
│   ├── scene_analyzer.py           # AI-powered screenplay analysis
│   ├── storyboard_generator.py     # Enhanced Style DNA system
│   ├── model_config.py             # Optimized model configuration
│   ├── prompt_sanitizer.py         # AI-based prompt cleaning
│   └── text_extractor.py           # PDF/text extraction
├── templates/                      # HTML templates
├── static/                         # CSS, JS, images
├── railway.toml                    # Railway deployment config
├── nixpacks.toml                   # Build configuration
└── Dockerfile                      # Docker deployment
```

## 🛠️ Development Standards

### Code Quality Requirements
- **Professional Quality**: Animation studio broadcast-standard output
- **Character Consistency**: Same facial features across all frames
- **Performance**: Sub-6 second analysis times (current: 5.78s)
- **Zero Garbage**: Clean AI-based character extraction only
- **Style Control**: 4 distinct enhanced styles with consistency controls

### Model Configuration (BALANCED - Optimal)
```python
# Current optimized configuration
CHARACTER_MODEL=gpt-4o          # Best character detection
SCENE_MODEL=gpt-4o             # Superior scene understanding  
INFO_MODEL=gpt-4o-mini         # Fast basic info
SANITIZATION_MODEL=o3-mini     # Fastest sanitization
IMAGE_MODEL=gpt-image-1        # Specialized for images
```

### Testing Requirements
Before making any changes, run validation tests:
- `test_enhanced_styles.py` - Style DNA validation
- `test_21_jump_street.py` - Character extraction testing
- `test_scene_frame_accuracy.py` - Scene/frame counting validation

## 🎨 Style DNA System

### Enhanced Style DNA Base (1031 characters)
All styles include these universal consistency controls:
- Professional black & white line art only
- Clean vector-like lines, no shading/gradients
- Character consistency across all frames
- Simple line-based lighting (no complex shadows)
- Minimal background details
- Same facial features and proportions throughout

### 4 Style Variations
1. **Classic**: Pure professional storyboard (base DNA)
2. **Cinematic**: Dramatic composition + monochrome grays allowed
3. **Sketch**: Hand-drawn ink pen appearance with organic strokes
4. **Comic**: Bold dramatic ink work with high contrast

## 🔧 Critical Implementation Details

### Character Extraction (utils/scene_analyzer.py:658-690)
Uses AI with strict filtering to eliminate garbage:
- ❌ Sound effects: "AAAAAH!", "AAAAARGH!"
- ❌ Locations: "AUDITORIUM", "SCHOOL"
- ❌ Organizations: "LAPD", "SWAT", "FBI"
- ✅ Only actual human character names

### AsyncIO Client Cleanup
All async functions include proper OpenAI client cleanup:
```python
finally:
    if client:
        loop.run_until_complete(client.close())
    loop.close()
```

### Scene/Frame Counting Logic
- Action sequences: 2 frames (setup + action)
- Dialogue scenes: 1 frame
- Establishing shots: 1 frame
- Maximum per scene: 3 frames

## 🚀 Deployment

### Railway Configuration
Production-ready with `railway.toml`:
- Builder: NIXPACKS
- Health check: `/health`
- Auto-restart on failure
- Environment variables configured

### Environment Variables Required
```bash
OPENAI_API_KEY=your_api_key_here
MODEL_MODE=balanced
CHARACTER_MODEL=gpt-4o
SCENE_MODEL=gpt-4o
SANITIZATION_MODEL=o3-mini
INFO_MODEL=gpt-4o-mini
IMAGE_MODEL=gpt-image-1
```

## 📊 Current Performance Metrics
- **Analysis Speed**: 5.78s average (BALANCED config)
- **Character Quality**: 10/10 (zero garbage extraction)
- **Frame Accuracy**: 100% (manual verification matches)
- **Success Rate**: 100% (all tests passing)

## 🔗 Key Files to Understand
1. **`utils/scene_analyzer.py`** - Core AI analysis with character extraction
2. **`utils/storyboard_generator.py`** - Style DNA system implementation
3. **`utils/model_config.py`** - Model selection and configuration
4. **`app.py`** - Flask routes and main application logic

## 🚨 Critical Guidelines
- **NEVER** modify the enhanced Style DNA without testing all 4 styles
- **ALWAYS** validate character extraction results for garbage content
- **MUST** include proper AsyncIO client cleanup in any new async functions
- **REQUIRED** to run performance tests after model configuration changes
- **ESSENTIAL** to maintain frame counting accuracy for budget calculations

## 🎯 Common Tasks
1. **Style adjustments**: Modify Style DNA in `utils/storyboard_generator.py:114-156`
2. **Model tuning**: Adjust config in `utils/model_config.py`
3. **Character extraction improvements**: Enhance prompts in `utils/scene_analyzer.py:658-690`
4. **Performance optimization**: Profile async operations and model calls

---

*This system is production-ready and optimized for Railway deployment. Focus on maintaining the high-quality standards already established.*