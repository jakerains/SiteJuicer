#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for validating changes to the fetch_content function.
This script tests the updated return structure of the fetch_content function.
"""

import os
import sys
import json
from core import fetch_content

def test_fetch_content_return_structure():
    """
    Test the updated return structure of the fetch_content function.
    
    This function tests that the fetch_content function returns a dictionary
    with the expected keys: content, title, and url.
    
    Returns:
        bool: True if all tests pass, False otherwise.
    """
    # Get API key from environment
    api_key = os.environ.get("JINA_API_KEY")
    if not api_key:
        print("Error: JINA_API_KEY environment variable not set.", file=sys.stderr)
        print("Please set the JINA_API_KEY environment variable to your Jina Reader API key.", file=sys.stderr)
        print("Example: export JINA_API_KEY=jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX", file=sys.stderr)
        return False
    
    # Validate API key format
    if not api_key.startswith("jina_"):
        print("Warning: API key does not have the expected format (should start with 'jina_').", file=sys.stderr)
        print("Expected format: jina_XXXXXXXXXXXXXXXXXXXXXXXX_XXXXXXXXXXXXXXXX", file=sys.stderr)
        print("Current value: " + api_key, file=sys.stderr)
        print("Authentication may fail with incorrect format.", file=sys.stderr)
    
    # Test URL
    test_url = "https://example.com"
    
    # Options for fetch_content
    options = {
        "api_key": api_key,
        "main_content_only": True,
        "content_format": "markdown"
    }
    
    print(f"Testing fetch_content with URL: {test_url}")
    print(f"Using API key: {api_key[:8]}...{api_key[-4:]}")
    
    try:
        # Call fetch_content
        result = fetch_content(test_url, options)
        
        # Validate result is a dictionary
        if not isinstance(result, dict):
            print(f"Error: Expected result to be a dictionary, got {type(result)}", file=sys.stderr)
            return False
        
        # Check for required keys
        required_keys = ["content", "title", "url"]
        missing_keys = [key for key in required_keys if key not in result]
        
        if missing_keys:
            print(f"Error: Missing required keys in result: {', '.join(missing_keys)}", file=sys.stderr)
            return False
        
        # Print summary of result
        print("\nFetch Content Result Summary:")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"URL: {result.get('url', 'N/A')}")
        print(f"Content length: {len(result.get('content', ''))}")
        
        # Print preview of content
        content_preview = result.get('content', '')[:200] + "..." if len(result.get('content', '')) > 200 else result.get('content', '')
        print(f"\nContent preview:\n{content_preview}")
        
        print("\nAll tests passed!")
        return True
        
    except Exception as e:
        print(f"Error testing fetch_content: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fetch_content_return_structure()
    sys.exit(0 if success else 1) 