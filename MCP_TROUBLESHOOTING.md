# MCP Server Troubleshooting Guide

## Server ID: `puch-health-buddy-mcp`

### ✅ Current Status
Your MCP server is properly configured and working. The server files are in place and the server can be started successfully.

### 🔧 If You're Still Getting "Server Not Found" Errors

#### 1. **Restart Your MCP Client**
If you're using Claude Desktop or another MCP client:
- Close the application completely
- Wait a few seconds
- Restart the application

#### 2. **Verify Client Configuration**
The MCP client configuration file should be located at:
```
C:\Users\Admin\AppData\Roaming\Claude\claude_desktop_config.json
```

It should contain:
```json
{
  "mcpServers": {
    "puch-health-buddy-mcp": {
      "command": "C:/Users/Admin/AppData/Local/Microsoft/WindowsApps/python3.12.exe",
      "args": ["-m", "src.puch_health_buddy.mcp.simple_server"],
      "cwd": "C:\\Users\\Admin\\Desktop\\PuchAi Hackathon"
    }
  }
}
```

#### 3. **Manual Server Testing**
Test the server manually by running:
```powershell
cd "C:\Users\Admin\Desktop\PuchAi Hackathon"
python scripts\mcp_server_manager.py test
```

#### 4. **Start Server in Background**
You can start the server manually:
```powershell
cd "C:\Users\Admin\Desktop\PuchAi Hackathon"
python scripts\mcp_server_manager.py start
```

Or use the batch file:
```
start_mcp_server.bat
```

### 🛠️ Available Commands

| Command | Description |
|---------|-------------|
| `python scripts\mcp_server_manager.py status` | Check server status |
| `python scripts\mcp_server_manager.py test` | Test server functionality |
| `python scripts\mcp_server_manager.py start` | Start the server |
| `python scripts\verify_mcp_setup.py` | Verify complete setup |

### 🩺 Server Tools Available

1. **analyze_health_symptoms** - Analyze health symptoms and provide medical guidance
2. **fact_check_health_claim** - Verify health information and detect misinformation
3. **find_nearby_healthcare** - Find nearby healthcare facilities
4. **translate_health_info** - Translate health information between languages
5. **get_health_emergency_guidance** - Get emergency health guidance

### 🌐 Supported Languages
English, Hindi, Gujarati, Marathi, Tamil, Telugu, Kannada, Malayalam, Bengali, Punjabi, Odia, Assamese

### ⚠️ Common Issues and Solutions

#### Issue: "Server not found"
**Solution**: Ensure the MCP client is looking in the correct directory and using the exact server ID: `puch-health-buddy-mcp`

#### Issue: "Python not found" 
**Solution**: Make sure Python 3.12+ is installed and available at the configured path

#### Issue: "Module not found"
**Solution**: Install dependencies:
```powershell
pip install flask requests python-dotenv
```

#### Issue: "Permission denied"
**Solution**: Run as administrator or check file permissions

### 📞 Emergency Recovery

If nothing works, you can re-register the server:
```powershell
cd "C:\Users\Admin\Desktop\PuchAi Hackathon"
python scripts\mcp_server_manager.py unregister
python scripts\mcp_server_manager.py register
```

### 🔍 Debug Information

- **Project Path**: `C:\Users\Admin\Desktop\PuchAi Hackathon`
- **Server Module**: `src.puch_health_buddy.mcp.simple_server`
- **Python Path**: `C:/Users/Admin/AppData/Local/Microsoft/WindowsApps/python3.12.exe`
- **Transport**: stdio (standard input/output)
- **Protocol**: Model Context Protocol (MCP)

---

*Last Updated: August 10, 2025*
