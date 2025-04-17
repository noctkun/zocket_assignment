import streamlit as st
import requests.exceptions
from summarizer import fetch_and_clean
from agent import summarize_with_agent
import os

GEMINI_API_KEY = "AIzaSyBzqw9HkLnecFTzruh27wgkSucFngS0HUU"

st.set_page_config(page_title="Web Page Summarizer Agent", layout="wide")
st.title("AI Web Page Summarizer")

st.markdown("Enter a URL below. The system will fetch the web page's main text content and use a Google Gemini-powered AI agent to generate a concise summary.")

if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    st.warning("API Key not set. Please replace 'YOUR_GEMINI_API_KEY_HERE' in the app.py file with your actual Google Gemini API key.")

with st.form("summarize_form"):
    url = st.text_input("Web Page URL", placeholder="https://example.com/news/article")
    submitted = st.form_submit_button("Generate Summary")

    if submitted:
        if not url:
            st.error("Please enter a valid URL.")
        elif not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            st.error("API Key is missing or not configured correctly in app.py.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original Content")
                content = None
                try:
                    with st.spinner(f"Fetching content from {url}..."):
                        content = fetch_and_clean(url)
                        if not content:
                            st.error("Could not extract readable content from the URL.")
                        else:
                            st.info(f"Successfully extracted approx. {len(content)} characters.")
                            st.text_area("Extracted Text", content, height=400)
                except requests.exceptions.RequestException as e:
                    st.error(f"Network Error: Could not fetch URL. Details: {e}")
                except ValueError as e:
                    st.error(f"Content Error: {e}")
                except Exception as e:
                    st.error(f"Unexpected error during fetching: {e}")
                    st.exception(e)

            with col2:
                st.subheader("Generated Summary")
                if content:
                    try:
                        with st.spinner("Summarizing... Please wait."):
                            summary = summarize_with_agent(
                                context=content,
                                gemini_api_key=GEMINI_API_KEY
                            )
                        if isinstance(summary, str) and summary.startswith("Error:"):
                            st.error(f"Agent Error: {summary}")
                        elif not summary:
                            st.warning("Agent returned an empty summary.")
                        else:
                            st.success("Summary generated successfully.")
                            st.markdown(summary)
                    except Exception as e:
                        st.error(f"Unexpected error during summarization: {e}")
                        st.exception(e)
                elif url:
                    st.warning("Cannot generate summary because content could not be retrieved.")

st.markdown("---")
st.caption("Powered by AutoGen and Google Gemini | Fetches text using Requests and BeautifulSoup")
