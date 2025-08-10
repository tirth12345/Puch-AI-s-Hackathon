#!/usr/bin/env python3
"""
Credential Setup and Verification Script for Puch AI Health Buddy
"""

import os
import sys
from pathlib import Path

def check_credentials():
    """Check current credential status"""
    print("🔐 Credential Status Check")
    print("=" * 60)
    
    # MCP Server credentials (not needed for basic functionality)
    print("\n1. 🩺 MCP Server:")
    print("   ✅ No credentials required for MCP server")
    print("   ✅ Server runs locally without API keys")
    print("   ✅ Claude Desktop connects via stdio (no auth)")
    
    # Check for .env file
    env_file = Path.cwd() / ".env"
    env_template = Path.cwd() / ".env.template"
    
    print("\n2. 📄 Environment Configuration:")
    if env_file.exists():
        print(f"   ✅ .env file found: {env_file}")
    else:
        print(f"   ❌ .env file not found: {env_file}")
        if env_template.exists():
            print(f"   📋 Template available: {env_template}")
    
    # Check environment variables
    print("\n3. 🌍 Environment Variables:")
    
    required_for_full_features = {
        'WHATSAPP_ACCESS_TOKEN': 'WhatsApp Business API',
        'WHATSAPP_PHONE_NUMBER_ID': 'WhatsApp Phone Number',
        'GOOGLE_TRANSLATE_API_KEY': 'Google Translate API',
        'GOOGLE_MAPS_API_KEY': 'Google Maps API (for location services)'
    }
    
    optional_vars = {
        'WHATSAPP_VERIFY_TOKEN': 'WhatsApp Webhook Verification',
        'WEBHOOK_SECRET': 'Webhook Security',
        'PORT': 'Application Port',
        'DEBUG': 'Debug Mode'
    }
    
    # Check required credentials for full functionality
    missing_required = []
    for var_name, description in required_for_full_features.items():
        value = os.environ.get(var_name)
        if value and value != f'your_{var_name.lower()}_here':
            print(f"   ✅ {var_name}: Set ({description})")
        else:
            print(f"   ❌ {var_name}: Not set ({description})")
            missing_required.append((var_name, description))
    
    # Check optional credentials
    print("\n4. 🔧 Optional Settings:")
    for var_name, description in optional_vars.items():
        value = os.environ.get(var_name)
        if value and value != f'your_{var_name.lower()}_here':
            print(f"   ✅ {var_name}: {value} ({description})")
        else:
            print(f"   ⚠️  {var_name}: Not set ({description})")
    
    # Determine what works without credentials
    print("\n5. 🚀 What Works Without Credentials:")
    print("   ✅ MCP Server (full functionality)")
    print("   ✅ Basic health analysis (offline)")
    print("   ✅ Emergency guidance (offline)")
    print("   ✅ Health fact-checking (basic)")
    print("   ✅ Server registration and management")
    
    print("\n6. 🔒 What Requires Credentials:")
    if missing_required:
        print("   For FULL functionality, you'll need:")
        for var_name, description in missing_required:
            print(f"   ❌ {var_name} - {description}")
            
        print("\n   💡 These are needed for:")
        print("   • WhatsApp integration")
        print("   • Real-time translation")
        print("   • Location-based healthcare search")
        print("   • External API integrations")
    else:
        print("   ✅ All credentials are configured!")
    
    # MCP specific check
    print("\n7. 🔗 MCP Client Connection:")
    print("   ✅ No credentials needed for Claude Desktop")
    print("   ✅ Connection is via local stdio transport")
    print("   ✅ No API keys required for MCP protocol")
    print("   ✅ Server runs entirely locally")
    
    return len(missing_required) == 0

def create_env_file():
    """Create .env file from template"""
    env_file = Path.cwd() / ".env"
    env_template = Path.cwd() / ".env.template"
    
    if env_file.exists():
        print(f"✅ .env file already exists: {env_file}")
        return True
    
    if not env_template.exists():
        print(f"❌ Template file not found: {env_template}")
        return False
    
    # Copy template to .env
    with open(env_template, 'r') as template:
        content = template.read()
    
    with open(env_file, 'w') as env:
        env.write(content)
    
    print(f"✅ Created .env file from template: {env_file}")
    print("📝 Edit this file to add your actual API keys")
    return True

def setup_minimal_config():
    """Setup minimal configuration for MCP server only"""
    print("\n🔧 Setting up minimal configuration for MCP server...")
    
    env_file = Path.cwd() / ".env"
    
    minimal_config = """# Minimal configuration for MCP server
# MCP Server Settings
MCP_PORT=8000
MCP_SERVER_ID=puch-health-buddy-mcp
PORT=5000
DEBUG=False

# Optional: Add API keys below when available
# WHATSAPP_ACCESS_TOKEN=your_token_here
# GOOGLE_TRANSLATE_API_KEY=your_key_here
# GOOGLE_MAPS_API_KEY=your_key_here
"""
    
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(minimal_config)
        print(f"✅ Created minimal .env file: {env_file}")
    else:
        print(f"⚠️  .env file already exists: {env_file}")
    
    return True

def main():
    """Main function"""
    print("🩺 Puch AI Health Buddy - Credential Setup")
    print("=" * 60)
    
    # Check current status
    has_all_creds = check_credentials()
    
    print("\n" + "=" * 60)
    print("📋 Summary and Recommendations:")
    print("=" * 60)
    
    if has_all_creds:
        print("🎉 All credentials are configured!")
        print("✅ Your MCP server has full functionality")
    else:
        print("⚠️  Some credentials are missing, but that's OK!")
        print("✅ Your MCP server will work with basic functionality")
        print("🔧 You can add credentials later for full features")
    
    print("\n🚀 For MCP Server (Claude Desktop):")
    print("✅ NO credentials needed!")
    print("✅ Server is ready to connect")
    print("✅ Just restart Claude Desktop to connect")
    
    print("\n📝 To add credentials later:")
    print("1. Edit the .env file in your project directory")
    print("2. Add your API keys (WhatsApp, Google, etc.)")
    print("3. Restart the MCP server")
    
    # Offer to create minimal config
    env_file = Path.cwd() / ".env"
    if not env_file.exists():
        response = input("\n🔧 Create minimal .env file for MCP server? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            setup_minimal_config()
    
    print("\n✅ Setup complete! Your MCP server is ready to use.")

if __name__ == "__main__":
    main()
