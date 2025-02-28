#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UI module for SiteJuicer

This module provides a web-based user interface for SiteJuicer using Streamlit.
"""

import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime

try:
    import streamlit as st
    from streamlit_ace import st_ace
except ImportError:
    print("Streamlit UI requires additional dependencies. Install with: pip install streamlit streamlit-ace")
    sys.exit(1)

# Add the parent directory to sys.path if running from this file directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))

from core import (
    fetch_content, filter_content, strip_jina_metadata, format_markdown,
    save_markdown, save_html, save_json, extract_images
)

# Set page config
st.set_page_config(
    page_title="SiteJuicer",
    page_icon="🧃",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    """Main function for the Streamlit UI"""
    
    # Sidebar content
    with st.sidebar:
        st.title("SiteJuicer 🧃")
        st.markdown("Convert web pages to readable Markdown, HTML, or JSON")
        
        url = st.text_input("Enter a URL:", placeholder="https://example.com")
        
        # Output format selection
        output_format = st.selectbox(
            "Output format:",
            options=["markdown", "html", "json"],
            index=0,
        )
        
        # Advanced options in an expander
        with st.expander("Advanced Options"):
            col1, col2 = st.columns(2)
            
            with col1:
                include_metadata = st.checkbox("Include metadata", value=True)
                generate_toc = st.checkbox("Generate table of contents", value=False)
                extract_links = st.checkbox("Extract links", value=False)
            
            with col2:
                main_content_only = st.checkbox("Main content only", value=False)
                download_images = st.checkbox("Download images", value=False)
                cache_enabled = st.checkbox("Enable caching", value=True)
            
            timeout = st.number_input("Timeout (seconds)", min_value=5, max_value=120, value=30, step=5)
            user_agent = st.text_input(
                "User Agent:", 
                value="",
                placeholder="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        
        # Process button
        process_button = st.button("Process URL", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.markdown(
            "Made with ❤️ using [SiteJuicer](https://github.com/jakerains/sitejuicer)"
        )
    
    # Main content area
    if not url and not process_button:
        # Show welcome content when no URL provided
        st.title("Welcome to SiteJuicer 🧃")
        st.markdown("""
        SiteJuicer helps you convert web content to clean, readable formats:
        
        - ✨ **Extract clean content** from any web page
        - 📝 **Convert to Markdown**, HTML, or JSON
        - 🖼️ **Download images** (optional)
        - 🔗 **Extract links** (optional)
        - 📚 **Generate table of contents** (optional)
        
        Enter a URL in the sidebar to get started.
        """)
        
        # Example URLs in columns
        st.subheader("Try these examples:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### News")
            st.markdown("- [BBC News](https://www.bbc.com)")
            st.markdown("- [The Guardian](https://www.theguardian.com)")
        
        with col2:
            st.markdown("#### Technical")
            st.markdown("- [Python Docs](https://docs.python.org/3/)")
            st.markdown("- [MDN Web Docs](https://developer.mozilla.org)")
        
        with col3:
            st.markdown("#### Blogs")
            st.markdown("- [Medium](https://medium.com)")
            st.markdown("- [DEV Community](https://dev.to)")
            
    elif url or process_button:
        if process_button and not url:
            st.error("Please enter a URL to process")
            return

        # Process the URL
        try:
            with st.spinner(f"Processing {url} ..."):
                # Fetch content
                result = fetch_content(
                    url, 
                    options={
                        "api_key": st.session_state.get("api_key", ""),
                        "main_content_only": main_content_only,
                        "include_images": download_images,
                        "image_dir": tempfile.mkdtemp(prefix="sitejuicer_") if download_images else None,
                        "content_format": output_format
                    }
                )
                
                content = result.get("content", "")
                title = result.get("title", "")
                
                if "error" in result:
                    st.error(f"Error processing URL: {result['error']}")
                    return
                
                # Format based on requested output
                if output_format == "html":
                    output_content = content  # HTML is already in the right format
                    language = "html"
                elif output_format == "json":
                    import json
                    data = {
                        "url": url,
                        "title": title or "",
                        "date_extracted": datetime.now().isoformat(),
                        "content": content
                    }
                    output_content = json.dumps(data, indent=2)
                    language = "json"
                else:  # markdown (default)
                    output_content = format_markdown(
                        content, url, title, 
                        include_metadata=include_metadata,
                        generate_toc=generate_toc,
                        extract_links=extract_links
                    )
                    language = "markdown"
            
            # Display the title and processed content
            st.title(title or "Processed Content")
            st.markdown(f"Source: [{url}]({url})")
            
            # Display the content in an ace editor
            edited_content = st_ace(
                value=output_content,
                language=language,
                theme="github",
                height=600,
                readonly=False,
                key="editor",
            )
            
            # Download button for the content
            extension = ".md" if output_format == "markdown" else ".html" if output_format == "html" else ".json"
            filename = f"{title or 'content'}{extension}".replace(" ", "_")
            
            st.download_button(
                label=f"Download as {output_format.upper()}",
                data=edited_content,
                file_name=filename,
                mime=f"text/{output_format}",
                use_container_width=True,
            )
            
        except Exception as e:
            st.error(f"Error processing URL: {str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main() 