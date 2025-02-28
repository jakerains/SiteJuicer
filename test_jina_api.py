import requests
import sys

def test_jina_reader():
    """Test the Jina Reader API connection"""
    url = 'https://r.jina.ai/https://example.com'
    api_key = 'jina_2caa021406de46c7837bc05cce50e14d_qcv8AqU_xS_fCtKz3nJ2qS5IcDk'
    
    headers = {'Authorization': f'Bearer {api_key}'}
    
    try:
        print(f"Sending request to {url}")
        response = requests.get(url, headers=headers)
        
        # Print status code and headers for debugging
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            # Print first 500 characters of the response
            print("\nResponse Preview (first 500 chars):")
            print(response.text[:500])
            print("...")
            return True
        else:
            print(f"Error response: {response.text}")
            return False
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_jina_reader()
    sys.exit(0 if success else 1) 