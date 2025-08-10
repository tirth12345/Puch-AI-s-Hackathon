# MCP Integration for Puch AI Health Buddy

## 🆔 Server Information

**MCP Server ID:** `puch-health-buddy-mcp`

**Server Name:** Puch AI Health Buddy MCP Server

**Version:** 1.0.0

## 🚀 Quick Start

### 1. Install MCP Dependencies

```bash
pip install mcp asyncio-mqtt pydantic
```

### 2. Start MCP Server

```bash
# Run the MCP server startup script
python scripts/start_mcp_server.py

# Or run the server directly (after installing mcp package)
python -m src.puch_health_buddy.mcp.server
```

### 3. View Server Information

```bash
# Display MCP server ID and capabilities
python scripts/show_mcp_id.py
```

## 🛠️ Available MCP Tools

Your MCP server provides these tools:

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `analyze_health_symptoms` | Analyze health symptoms and provide guidance | `symptoms`, `language` |
| `fact_check_health_claim` | Verify health information and detect misinformation | `claim`, `language` |
| `find_nearby_healthcare` | Find nearby healthcare facilities | `location`, `language` |
| `translate_health_info` | Translate health information between languages | `text`, `target_language`, `source_language` |
| `get_health_emergency_guidance` | Emergency health assessment and guidance | `symptoms`, `language` |

## 🌐 Supported Languages

- **English** (en)
- **Hindi** (hi) - हिंदी
- **Gujarati** (gu) - ગુજરાતી
- **Marathi** (mr) - मराठी
- **Tamil** (ta) - தமிழ்
- **Telugu** (te) - తెలుగు
- **Kannada** (kn) - ಕನ್ನಡ
- **Malayalam** (ml) - മലയാളം
- **Bengali** (bn) - বাংলা
- **Punjabi** (pa) - ਪੰਜਾਬੀ
- **Odia** (or) - ଓଡ଼ିଆ
- **Assamese** (as) - অসমীয়া

## 📋 MCP Prompts

The server also provides these interactive prompts:

1. **`health_consultation`** - Interactive health consultation
2. **`medical_fact_check`** - Medical fact-checking
3. **`emergency_assessment`** - Emergency health assessment

## 🔧 Configuration Files

- **`mcp_manifest.json`** - MCP server manifest
- **`config/settings.py`** - Server configuration with MCP settings
- **`src/puch_health_buddy/mcp/config.py`** - MCP-specific configuration

## 📊 Usage Examples

### Health Symptom Analysis
```json
{
  "tool": "analyze_health_symptoms",
  "arguments": {
    "symptoms": "I have fever and headache",
    "language": "en"
  }
}
```

### Fact Checking
```json
{
  "tool": "fact_check_health_claim", 
  "arguments": {
    "claim": "Garlic prevents COVID-19",
    "language": "en"
  }
}
```

### Finding Healthcare Facilities
```json
{
  "tool": "find_nearby_healthcare",
  "arguments": {
    "location": "Mumbai",
    "language": "en"
  }
}
```

## 🔒 Security & Compliance

- **Rate Limiting**: Each tool has configurable rate limits
- **Input Validation**: All inputs are sanitized and validated
- **Medical Disclaimers**: All health advice includes appropriate disclaimers
- **Privacy**: No personal health data is stored

## 🏥 Integration with Health Services

The MCP server integrates with your existing health services:

- **Health Service**: Symptom analysis and medical guidance
- **Fact Check Service**: Misinformation detection and verification
- **Translation Service**: Multi-language support
- **Location Service**: Healthcare facility search

## 📱 Client Integration

To integrate with your MCP client:

1. Use server ID: `puch-health-buddy-mcp`
2. Connect via stdio transport
3. Call available tools with proper parameters
4. Handle responses with medical disclaimers

## 🚨 Emergency Features

The server includes special emergency detection:

- Identifies critical symptoms requiring immediate attention
- Provides emergency contact information for India (102, 108)
- Escalates urgent cases with clear warnings
- Supports emergency guidance in multiple languages

## 📞 Support

For issues with MCP integration:

1. Check server logs for errors
2. Validate configuration with `python scripts/show_mcp_id.py`
3. Test basic functionality with `python src/puch_health_buddy/mcp/client.py`
4. Ensure all dependencies are installed

---

**Remember**: This MCP server provides health information for educational purposes only. Always consult healthcare professionals for medical advice.
