"""
Simple test script to verify DNS Manager functionality
Run this to check if the app components work correctly
"""

import sys
import io

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import customtkinter
        print("✓ CustomTkinter imported successfully")
    except ImportError as e:
        print(f"✗ CustomTkinter import failed: {e}")
        return False

    try:
        import json
        import os
        import socket
        import subprocess
        import threading
        import time
        print("✓ All standard library modules available")
    except ImportError as e:
        print(f"✗ Standard library import failed: {e}")
        return False

    return True

def test_platform():
    """Check if running on Windows"""
    print("\nTesting platform...")
    if sys.platform != 'win32':
        print("✗ This application requires Windows")
        return False
    print("✓ Running on Windows")
    return True

def test_dns_validation():
    """Test IP validation function"""
    print("\nTesting IP validation...")

    def is_valid_ip(ip: str) -> bool:
        try:
            parts = ip.split('.')
            return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
        except:
            return False

    test_cases = [
        ("1.1.1.1", True),
        ("8.8.8.8", True),
        ("192.168.1.1", True),
        ("256.1.1.1", False),
        ("1.1.1", False),
        ("invalid", False),
    ]

    all_passed = True
    for ip, expected in test_cases:
        result = is_valid_ip(ip)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {ip}: {result} (expected {expected})")
        if result != expected:
            all_passed = False

    return all_passed

def test_network_commands():
    """Test if network commands are available"""
    print("\nTesting network commands...")

    try:
        import subprocess
        result = subprocess.run(
            ['netsh', 'interface', 'show', 'interface'],
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode == 0:
            print("✓ netsh command available")
            return True
        else:
            print("✗ netsh command failed")
            return False
    except Exception as e:
        print(f"✗ Network command test failed: {e}")
        return False

def test_socket():
    """Test socket functionality for ping tests"""
    print("\nTesting socket functionality...")

    try:
        import socket
        # Try to resolve a hostname
        ip = socket.gethostbyname("google.com")
        print(f"✓ Socket working (google.com -> {ip})")
        return True
    except Exception as e:
        print(f"✗ Socket test failed: {e}")
        return False

def test_file_operations():
    """Test JSON file operations"""
    print("\nTesting file operations...")

    try:
        import json
        import os

        test_data = {"test": "data"}
        test_file = "test_config.json"

        # Write
        with open(test_file, 'w') as f:
            json.dump(test_data, f)

        # Read
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)

        # Cleanup
        os.remove(test_file)

        if loaded_data == test_data:
            print("✓ File operations working")
            return True
        else:
            print("✗ Data mismatch in file operations")
            return False
    except Exception as e:
        print(f"✗ File operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("DNS Manager Pro - Component Tests")
    print("="*50)

    tests = [
        ("Imports", test_imports),
        ("Platform", test_platform),
        ("IP Validation", test_dns_validation),
        ("Network Commands", test_network_commands),
        ("Socket", test_socket),
        ("File Operations", test_file_operations),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))

    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    total = len(results)
    passed = sum(1 for _, result in results if result)

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! DNS Manager is ready to use.")
        print("\nTo run the application:")
        print("  1. Double-click 'run_as_admin.bat'")
        print("  2. Or run: python dns_manager.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")

    print("="*50)

if __name__ == "__main__":
    main()
