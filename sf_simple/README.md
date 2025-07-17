# Script Fury Simple - Standalone Storyboard Generator

A streamlined, **completely self-contained** storyboard generator that converts screenplays into professional storyboard frames using AI. This is a simplified version that demonstrates core functionality without complex infrastructure.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation & Setup

1. **Clone or copy this directory**
   ```bash
   # This directory is completely self-contained
   cd sf_simple
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy and edit the .env file
   cp .env.example .env
   # Add your OpenAI API key to .env
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open http://localhost:5001 in your browser
   - Upload a screenplay (PDF, TXT, or Fountain format)
   - Select a visual style and generate storyboard frames

## 🏗️ Architecture

### Complete Self-Containment
- **No external dependencies** on main Script Fury codebase
- **Portable** - can be moved anywhere and run independently
- **All utilities included** - text extraction, AI analysis, frame generation
- **Self-contained static assets** - CSS, JS, images all included

### Core Components

```
sf_simple/
├── app.py                    # Main Flask application
├── requirements.txt          # All dependencies listed
├── .env                     # Configuration (API keys, settings)
├── utils/                   # Self-contained utilities
│   ├── text_extractor.py    # PDF/text extraction
│   ├── scene_analyzer.py    # AI screenplay analysis
│   ├── storyboard_generator.py # Frame generation
│   └── print_generator.py   # Printable layouts
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── uploads/                 # Temporary file storage
└── tests/                   # Complete test suite
```

### Technology Stack
- **Backend**: Flask + Python
- **AI/ML**: OpenAI GPT-4o-mini + gpt-image-1
- **Frontend**: Vanilla HTML/CSS/JS with Japanese-inspired design
- **Text Processing**: PyPDF2 + pdfplumber for PDF extraction

## 🎨 Features

### AI-Powered Analysis
- Automatic scene detection using industry standards
- Character extraction and visual descriptions
- Intelligent frame count optimization
- Story structure analysis

### Professional Storyboard Generation
- 4 visual styles: Classic, Cinematic, Sketch, Comic
- Consistent black & white line art
- Real-time generation progress
- Professional animation studio standards

### Modern UI/UX
- Japanese-inspired design system matching main Script Fury app
- Responsive design for all devices
- localStorage session recovery
- Real-time progress tracking
- Project-specific cache isolation

### File Format Support
- **PDF**: Automatic text extraction from screenplay PDFs
- **TXT**: Plain text screenplays
- **Fountain**: Fountain markup format support

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python run_tests.py

# Run specific test suites
python -m unittest tests.unit.test_scene_analyzer
python -m unittest tests.integration.test_app
python -m unittest tests.e2e.test_end_to_end
```

### Test Coverage
- **Unit tests**: Individual component testing
- **Integration tests**: API and service integration
- **E2E tests**: Complete workflow testing
- **Performance tests**: Large screenplay handling

## 🔧 Configuration

### Environment Variables (.env)
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
DEFAULT_MODEL=gpt-4o-mini
IMAGE_MODEL=gpt-image-1

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
MAX_SCENES_DEFAULT=5
QUALITY_DEFAULT=medium

# Cost Limits
MAX_COST_PER_PROJECT=10.00
```

### Customization
- **Styles**: Modify `STYLES` dict in `app.py`
- **Scene Detection**: Adjust algorithms in `utils/scene_analyzer.py`
- **Visual Style**: Update `STORYBOARD_STYLE_DNA` in `utils/storyboard_generator.py`

## 💰 Cost Management

### Pricing
- **Analysis**: ~$0.10-0.30 per screenplay (GPT-4o-mini)
- **Frame Generation**: ~$0.04-0.08 per frame (gpt-image-1)
- **Total Project**: Usually $0.50-2.00 for 5-15 frames

### Cost Controls
- Per-project cost limits enforced
- Real-time cost tracking
- Configurable quality settings

## 🚀 Deployment

### Local Development
```bash
python app.py
# Access at http://localhost:5001
```

### Production Deployment
1. Set `FLASK_ENV=production` in .env
2. Use a production WSGI server (gunicorn, uwsgi)
3. Configure reverse proxy (nginx, Apache)
4. Set up SSL certificates
5. Configure error logging and monitoring

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
```

## 📁 Portability

### Moving the Application
This entire directory is **completely portable**:

1. **Copy the entire sf_simple directory** to any location
2. **Install Python dependencies**: `pip install -r requirements.txt`
3. **Set up .env file** with your API keys
4. **Run**: `python app.py`

### No External Dependencies
- ✅ No dependencies on parent directories
- ✅ No imports from main Script Fury codebase
- ✅ All utilities and models self-contained
- ✅ Self-contained static assets and templates
- ✅ Independent configuration and environment

## 🔍 Troubleshooting

### Common Issues

**"Module not found" errors**
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're in the sf_simple directory when running

**"OpenAI API error"**
- Verify your API key is set in .env
- Check your OpenAI account has sufficient credits
- Ensure you have access to gpt-4o-mini and gpt-image-1 models

**Upload failures**
- Check file size (max 16MB)
- Ensure PDF is text-based (not scanned images)
- Try converting to plain text format

**Generation hanging**
- Check OpenAI API status
- Verify network connectivity
- Check Flask debug output for error details

### Debug Mode
```bash
# Enable detailed logging
FLASK_DEBUG=True python app.py
```

## 📄 License

This is a simplified demonstration version of Script Fury. See the main project for full licensing information.

## 🤝 Contributing

Since this is a self-contained demonstration project:
1. This directory can be modified independently
2. No need to sync with main Script Fury codebase
3. All changes stay within this directory
4. Perfect for experimentation and customization

---

**Script Fury Simple** - Professional storyboard generation made simple and portable.