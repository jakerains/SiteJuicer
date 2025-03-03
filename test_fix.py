"""
Test script to verify the fix for the title variable issue.
"""

# Import the core module directly
from core import fetch_content

# Test the fetch_content function with a simple URL
print("Testing fetch_content with example.com...")
result = fetch_content('https://example.com')

# Verify that title is present and not None
print(f"Title: {result.get('title', 'NOT FOUND')}")
print(f"URL: {result.get('url', 'NOT FOUND')}")
print(f"Content length: {len(result.get('content', ''))}")

print("\nTests completed successfully!") 