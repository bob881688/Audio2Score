#!/usr/bin/env python3
"""
Quick health check script for Audio2Score Backend
Usage: python check.py [url]
"""
import sys
import requests

def check_health(base_url):
    """Check if the API is running"""
    try:
        print(f"🔍 Checking {base_url}...")
        response = requests.get(f"{base_url}/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is running!")
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Framework: {data.get('framework')}")
            
            # Check docs
            docs_response = requests.get(f"{base_url}/docs", timeout=5)
            if docs_response.status_code == 200:
                print(f"✅ API Documentation available at {base_url}/docs")
            
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {base_url}")
        print("   Make sure the server is running!")
        return False
    except requests.exceptions.Timeout:
        print(f"⏱️  Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print("=" * 50)
    print("  Audio2Score Backend Health Check")
    print("=" * 50)
    print()
    
    success = check_health(url)
    
    print()
    if success:
        print("🎉 All checks passed!")
    else:
        print("⚠️  Health check failed")
        sys.exit(1)
