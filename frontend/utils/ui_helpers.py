"""
UI Helpers for robust HTML and UI component rendering in Streamlit.
Guarantees pure HTML rendering without Markdown parser code-fence collisions.
"""
import streamlit as st
import textwrap


def render_html(html_code: str):
    """
    Renders pure HTML into the Streamlit DOM without Markdown parsing.
    Prevents indentation or blank lines from being misinterpreted as Markdown code blocks.
    """
    if not html_code:
        return
    cleaned = textwrap.dedent(html_code).strip()
    if not cleaned:
        return
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        st.markdown(cleaned, unsafe_allow_html=True)

