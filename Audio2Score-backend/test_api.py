#!/usr/bin/env python3
"""
API Testing Script for Audio2Score Backend
Usage: python test_api.py [base_url]
Example: python test_api.py https://audio2score-backend.onrender.com
"""
import requests
import sys
import time
from typing import Optional

# Get base URL from command line or use default
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"

print("\n" + "=" * 60)
print("   Audio2Score Backend API Tests (FastAPI)")
print("=" * 60)
print(f"\n🎯 Testing API at: {BASE_URL}\n")


def test_health_check():
    """Test health check endpoint"""
    print("1️⃣  Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            data = response.json()
            print(f"   📊 API: {data.get('message')}")
            print(f"   📊 Framework: {data.get('framework')}")
            print(f"   📊 Version: {data.get('version')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()


def test_register() -> Optional[dict]:
    """Test user registration"""
    print("2️⃣  Testing User Registration...")
    
    test_user = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=test_user
        )
        
        if response.status_code == 201:
            data = response.json()
            print("   ✅ Registration successful")
            print(f"   👤 Username: {test_user['username']}")
            print(f"   📧 Email: {test_user['email']}")
            print(f"   🔑 Token: {'✓' if data.get('token') else '✗'}")
            return {
                "user": test_user,
                "token": data.get("token")
            }
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   📄 {response.json()}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return None
    finally:
        print()


def test_login(user_data: dict) -> Optional[str]:
    """Test user login"""
    print("3️⃣  Testing User Login...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "username": user_data["username"],
                "password": user_data["password"]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Login successful")
            print(f"   🔑 Token: {'✓' if data.get('token') else '✗'}")
            return data.get("token")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   📄 {response.json()}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return None
    finally:
        print()


def test_get_me(token: str):
    """Test getting current user info"""
    print("4️⃣  Testing Get Current User...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Get user info successful")
            print(f"   📊 User: {data.get('username')}")
            print(f"   📧 Email: {data.get('email')}")
            print(f"   🆔 ID: {data.get('id')}")
        else:
            print(f"   ❌ Get user info failed: {response.status_code}")
            print(f"   📄 {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()


def test_get_library(token: str):
    """Test getting MIDI library"""
    print("5️⃣  Testing Get MIDI Library...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/midi/library",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Get library successful")
            print(f"   📚 MIDI files count: {data.get('count', 0)}")
            
            if data.get('count', 0) > 0:
                for midi in data.get('midis', [])[:3]:
                    print(f"      - {midi.get('original_filename')} ({midi.get('note_count', 'N/A')} notes)")
        else:
            print(f"   ❌ Get library failed: {response.status_code}")
            print(f"   📄 {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()


def test_unauthorized_access():
    """Test unauthorized access"""
    print("6️⃣  Testing Unauthorized Access...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/midi/library")
        
        if response.status_code == 401:
            print("   ✅ Unauthorized access properly blocked")
        elif response.status_code == 403:
            print("   ✅ Forbidden access properly blocked")
        else:
            print(f"   ⚠️  Expected 401/403, got: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()


def test_api_docs():
    """Test API documentation endpoints"""
    print("7️⃣  Testing API Documentation...")
    
    try:
        # Test Swagger UI
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("   ✅ Swagger UI available at /docs")
        else:
            print(f"   ⚠️  Swagger UI status: {response.status_code}")
        
        # Test ReDoc
        response = requests.get(f"{BASE_URL}/redoc")
        if response.status_code == 200:
            print("   ✅ ReDoc available at /redoc")
        else:
            print(f"   ⚠️  ReDoc status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    print()


def main():
    """Run all tests"""
    # 1. Health check
    test_health_check()
    
    # 2. Test unauthorized access
    test_unauthorized_access()
    
    # 3. Test registration
    registration_result = test_register()
    if not registration_result:
        print("❌ Cannot continue tests without registration")
        return
    
    # 4. Test login
    token = test_login(registration_result["user"])
    if not token:
        print("❌ Cannot continue tests without login")
        return
    
    # 5. Test get current user
    test_get_me(token)
    
    # 6. Test get library
    test_get_library(token)
    
    # 7. Test API documentation
    test_api_docs()
    
    # Summary
    print("=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n💡 Tips:")
    print(f"   - API Documentation: {BASE_URL}/docs")
    print(f"   - Alternative Docs: {BASE_URL}/redoc")
    print(f"\n   - Use this token to test file upload:")
    print(f"   {token[:50]}...")
    print(f"\n   - Test file upload with curl:")
    print(f"   curl -X POST {BASE_URL}/api/midi/upload \\")
    print(f"     -H \"Authorization: Bearer {token}\" \\")
    print(f"     -F \"audio=@path/to/your/audio.mp3\"\n")


if __name__ == "__main__":
    main()
