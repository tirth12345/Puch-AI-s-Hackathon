# 🩺 Puch AI + Health Buddy

**An AI-powered WhatsApp health assistant and fact-checker designed for Indian communities, bridging the gap between healthcare information and accessibility.**

> 🏆 **Built for Puch AI Hackathon** - Empowering health literacy through conversational AI

## 🌟 Features

### 🏥 **Intelligent Health Consultation**
- **Symptom Analysis**: Advanced pattern recognition for common health issues
- **Medical Guidance**: Evidence-based advice for fever, cold, stomach issues, and more
- **Urgency Detection**: Identifies emergency situations requiring immediate medical attention
- **Disclaimer-compliant**: Clear medical disclaimers ensuring user safety

### 🔍 **Health Fact-Checking**
- **Misinformation Detection**: Identifies and debunks common health myths
- **Source Verification**: Cross-references with WHO, CDC, and PIB Fact Check
- **COVID-19 Myth Busting**: Specialized detection for pandemic-related misinformation
- **Educational Responses**: Provides accurate information with reliable sources

### 🌐 **Multi-Language Support**
- **12 Indian Languages**: Hindi, Gujarati, Marathi, Tamil, Telugu, Kannada, Malayalam, Bengali, Punjabi, Odia, Assamese
- **Auto Language Detection**: Automatically detects user's preferred language
- **Culturally Aware**: Responses tailored for Indian healthcare context

### 📍 **Location-Based Services**
- **Healthcare Finder**: Locates nearby clinics and hospitals
- **City-Specific Search**: Support for major Indian cities
- **Emergency Services**: Quick access to emergency healthcare facilities

### 🔒 **Security & Privacy**
- **Webhook Verification**: Secure message handling with signature validation
- **Data Protection**: User interactions logged securely
- **Compliance Ready**: Built with healthcare data privacy in mind

### 🤖 **MCP (Model Context Protocol) Integration**
- **Server ID**: `puch-health-buddy-mcp`
- **Standardized AI Interface**: Compatible with MCP-enabled AI assistants
- **Tool Integration**: Exposes health services as MCP tools
- **Multi-Modal Support**: Text and prompt-based interactions
- **Async Operations**: High-performance asynchronous processing

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- WhatsApp Business API access
- Facebook Developer Account
- Optional: MCP-compatible AI assistant for tool integration

### 1. Clone & Setup
```bash
git clone https://github.com/tirth12345/Puch-AI-s-Hackathon.git
cd puch-health-buddy
pip install -r requirements.txt

# For MCP integration (optional)
pip install -e ".[mcp]"
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```env
# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=your_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_verify_token
WEBHOOK_SECRET=your_webhook_secret

# MCP (Model Context Protocol) dependencies
mcp==0.9.0
asyncio-mqtt==0.11.0
pydantic==2.5.0

# Google APIs (Optional)
GOOGLE_TRANSLATE_API_KEY=your_translate_api_key
GOOGLE_MAPS_API_KEY=your_maps_api_key

# MCP Server (Optional)
MCP_PORT=8000

# Application Settings
PORT=5000
DEBUG=False
FLASK_ENV=production
```

### 3. Run the Application
```bash
# Development
python main.py

# Production with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### 4. Set Up WhatsApp Webhook
- Navigate to your Facebook Developer Console
- Configure webhook URL: `https://yourdomain.com/webhook`
- Use your `WHATSAPP_VERIFY_TOKEN` for verification

## 📁 Project Architecture

```
PuchAi Hackathon/
├── 🏠 main.py                          # Application entry point
├── 📋 requirements.txt                 # Python dependencies
├── ⚙️ setup.py                         # Package configuration
├── 📖 README.md                        # This file
├── 
├── 📂 src/puch_health_buddy/           # Main application package
│   ├── 🧠 core/                        # Core application logic
│   │   ├── app.py                      # Flask application factory
│   │   └── bot.py                      # WhatsApp bot intelligence
│   ├── 
│   ├── 🤖 mcp/                         # MCP (Model Context Protocol) integration
│   │   ├── server.py                   # MCP server implementation
│   │   ├── config.py                   # MCP configuration
│   │   ├── client.py                   # MCP test client
│   │   └── utils.py                    # MCP utilities
│   ├── 
│   ├── 🔧 services/                    # Business logic services
│   │   ├── health_service.py           # Health consultation engine
│   │   ├── fact_check_service.py       # Misinformation detection
│   │   ├── translation_service.py      # Multi-language support
│   │   └── location_service.py         # Healthcare facility finder
│   ├── 
│   └── 🛠️ utils/                       # Utility modules
│       ├── analyzers.py                # Health & fact-check analysis
│       ├── formatters.py               # Response formatting
│       └── helpers.py                  # General utilities
├── 
├── ⚙️ config/                          # Configuration management
│   └── settings.py                     # Application settings
├── 
├── 🧪 tests/                           # Test suite
│   └── test_app.py                     # Comprehensive tests
├── 
├── 📊 scripts/                         # Utility scripts
│   ├── monitor.py                      # Application monitoring
│   ├── start_mcp_server.py             # MCP server startup
│   └── show_mcp_id.py                  # Display MCP server info
├── 
├── 🚀 deployment/                      # Deployment configurations
│   ├── Dockerfile                      # Docker containerization
│   ├── docker-compose.yml             # Multi-container setup
│   ├── deploy.sh                       # Deployment automation
│   ├── ci-cd.yml                       # CI/CD pipeline
│   └── Procfile                        # Heroku configuration
└── 
└── 📚 docs/                            # Documentation
    ├── RESTRUCTURING_GUIDE.md         # Architecture guide
    └── MCP_INTEGRATION.md             # MCP integration guide
```

### 🤖 MCP Integration

The project includes a full **Model Context Protocol (MCP)** server implementation:

- **Server ID**: `puch-health-buddy-mcp`
- **Available Tools**: Health analysis, fact-checking, location search, translation, emergency guidance
- **Supported Languages**: 12 Indian languages
- **Transport**: stdio (standard MCP protocol)

```bash
# Start MCP server
python scripts/start_mcp_server.py

# View MCP server information
python scripts/show_mcp_id.py
```

## 🛠️ Development

### Local Development Setup
```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v

# Run with auto-reload
export FLASK_ENV=development
python main.py
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src/puch_health_buddy

# Run specific test
python -m pytest tests/test_app.py::TestWhatsAppBot::test_health_query
```

### Code Quality
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## 🐳 Deployment

### Docker Deployment
```bash
# Build image
docker build -t puch-health-buddy .

# Run container
docker run -p 5000:5000 --env-file .env puch-health-buddy

# Docker Compose
docker-compose up -d
```

### Cloud Deployment

#### Heroku
```bash
# Login and create app
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set WHATSAPP_ACCESS_TOKEN=your_token

# Deploy
git push heroku main
```

#### AWS/GCP/Azure
Refer to `deployment/` directory for platform-specific configurations.

## 🔧 API Endpoints

### REST API (WhatsApp Integration)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check and service info |
| `/webhook` | GET | WhatsApp webhook verification |
| `/webhook` | POST | WhatsApp message processing |
| `/health` | GET | Application health status |

### MCP Tools (AI Assistant Integration)
| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `analyze_health_symptoms` | Analyze health symptoms and provide guidance | `symptoms`, `language` |
| `fact_check_health_claim` | Verify health information and detect misinformation | `claim`, `language` |
| `find_nearby_healthcare` | Find nearby healthcare facilities | `location`, `language` |
| `translate_health_info` | Translate health information between languages | `text`, `target_language` |
| `get_health_emergency_guidance` | Emergency health assessment and guidance | `symptoms`, `language` |

## 💬 Usage Examples

### Health Consultation
```
User: "I have fever and headache since 2 days"

Bot: "🩺 Health Information - Fever

Symptoms: high temperature, sweating, chills, headache

General Advice: Rest, drink fluids, take paracetamol if needed. See doctor if fever >101°F or persists >3 days.

⚠️ Seek immediate medical help if: difficulty breathing, severe headache, chest pain

Disclaimer: This is general information only. Please consult a healthcare professional for proper diagnosis."
```

### Fact-Checking
```
User: "Is it true that garlic prevents COVID-19?"

Bot: "🔍 Fact Check Result

Claim: Eating Garlic Prevents Covid
Verdict: FALSE ❌
Explanation: No scientific evidence supports garlic as COVID-19 prevention
Sources: WHO, PIB Fact Check

ℹ️ Always verify health information from official sources like WHO, CDC, or government health departments."
```

### Multi-Language Support
```
User: "मुझे बुखार है" (Hindi: I have fever)

Bot: "🩺 स्वास्थ्य जानकारी - बुखार

लक्षण: तेज़ बुखार, पसीना, कंपकंपी, सिरदर्द

सामान्य सलाह: आराम करें, तरल पदार्थ पिएं, ज़रूरत हो तो पैरासिटामोल लें..."
```

### MCP Tool Usage (AI Assistant Integration)
```json
{
  "tool": "analyze_health_symptoms",
  "arguments": {
    "symptoms": "I have fever and headache since 2 days",
    "language": "en"
  }
}
```

**Response:**
```json
{
  "analysis": "Health analysis indicates fever and headache symptoms...",
  "urgency_level": "medium",
  "recommendations": ["Rest and stay hydrated", "Monitor symptoms", "Consult healthcare provider if symptoms worsen"],
  "disclaimer": "This is not medical advice. Consult healthcare professionals."
}
```

### MCP Fact-Checking
```json
{
  "tool": "fact_check_health_claim",
  "arguments": {
    "claim": "Garlic prevents COVID-19",
    "language": "en"
  }
}
```

## 🏥 Supported Health Categories

- **General Health**: Basic health queries and wellness advice
- **Fever & Symptoms**: Temperature-related concerns and management
- **Respiratory Issues**: Cold, cough, breathing problems
- **Digestive Problems**: Stomach pain, nausea, digestive disorders
- **Pain Management**: Headaches, joint pain, general pain relief
- **Mental Health**: Basic mental wellness and stress management
- **Emergency Care**: Critical condition identification and guidance

## 🔍 Fact-Check Categories

- **COVID-19 Myths**: Vaccine misinformation, prevention myths
- **Home Remedies**: Unverified traditional treatments
- **General Health**: Common medical misconceptions
- **Nutrition**: Diet and supplement misinformation

## 🌍 Supported Languages

| Language | Code | Native Name |
|----------|------|-------------|
| English | en | English |
| Hindi | hi | हिंदी |
| Gujarati | gu | ગુજરાતી |
| Marathi | mr | मराठी |
| Tamil | ta | தமிழ் |
| Telugu | te | తెలుగు |
| Kannada | kn | ಕನ್ನಡ |
| Malayalam | ml | മലയാളം |
| Bengali | bn | বাংলা |
| Punjabi | pa | ਪੰਜਾਬੀ |
| Odia | or | ଓଡ଼ିଆ |
| Assamese | as | অসমীয়া |

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include steps to reproduce and expected behavior
- Provide system information and error logs

### 💡 Feature Requests
- Suggest new health categories or fact-check topics
- Propose language support additions
- Share ideas for improved user experience

### 🔧 Development Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📝 Documentation
- Improve README and documentation
- Add code comments and docstrings
- Create usage examples and tutorials

## 📊 Analytics & Monitoring

The application includes built-in monitoring capabilities:

- **Usage Analytics**: Track user interactions and popular queries
- **Health Metrics**: Monitor application performance and uptime
- **Error Tracking**: Log and analyze system errors
- **Language Statistics**: Understand multilingual usage patterns

## 🔐 Security Considerations

- **Webhook Security**: Implements signature verification for WhatsApp webhooks
- **Data Privacy**: Minimal data collection with secure logging
- **Rate Limiting**: Protection against API abuse
- **Input Validation**: Sanitized user inputs to prevent injection attacks
- **HTTPS Required**: All communications encrypted in transit

## 📚 Resources & References

### Official Documentation
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Cloud Translation API](https://cloud.google.com/translate/docs)
- [Model Context Protocol (MCP)](https://spec.modelcontextprotocol.io/)

### MCP Integration
- [MCP Integration Guide](docs/MCP_INTEGRATION.md)
- Server ID: `puch-health-buddy-mcp`
- Available Tools: 5 health-focused MCP tools
- Supported Languages: 12 Indian languages

### Health Information Sources
- [World Health Organization (WHO)](https://who.int)
- [Centers for Disease Control and Prevention (CDC)](https://cdc.gov)
- [Press Information Bureau Fact Check](https://pib.gov.in/PressReleasePage.aspx?PRID=1627564)
- [Ministry of Health and Family Welfare, India](https://mohfw.gov.in)

### Research Papers
- AI in Healthcare: Applications and Challenges
- Misinformation Detection in Social Media
- Natural Language Processing for Medical Text



## 🏆 Hackathon Submission

**Event**: Puch AI Hackathon  
**Theme**: AI for Social Good  
**Category**: Healthcare Technology  
**Submission Date**: 10 August 2025

### Problem Statement
Healthcare misinformation and limited access to reliable medical information in rural and semi-urban India.

### Solution
A WhatsApp-based AI health assistant that provides:
- Instant health consultations in local languages
- Real-time fact-checking of health information
- Access to nearby healthcare facilities
- Emergency situation identification

### Impact
- **Accessibility**: WhatsApp's 400M+ users in India
- **Language Barrier**: Support for 12 Indian languages
- **Misinformation Combat**: Real-time fact-checking capabilities
- **Healthcare Access**: Bridge between communities and healthcare information

## 👥 Team

- **Developer**: Tirth Chokshi , Dhruvil Malvania
- **Email**: tirthchokshi20@gmail.com , dhruvilmalvania@gmail.com
- **GitHub**: https://github.com/tirth12345 , https://github.com/Dhruvilllll
- **LinkedIn**: https://www.linkedin.com/in/tirth-chokshi-44b355295/ , https://www.linkedin.com/in/dhruvil-malvania/

## 🙏 Acknowledgments

- **Puch AI** for organizing the hackathon and inspiring innovation
- **WhatsApp Business API** for enabling conversational healthcare
- **Open Source Community** for the amazing tools and libraries
- **Healthcare Workers** for their invaluable feedback and insights
- **Indian Language Computing** initiatives for multilingual support

---

<div align="center">

**Made with ❤️ for healthier communities**

[🌟 Star this repo](https://github.com/yourusername/puch-health-buddy) • [🐛 Report Bug](https://github.com/yourusername/puch-health-buddy/issues) • [💡 Request Feature](https://github.com/yourusername/puch-health-buddy/issues)

</div>
