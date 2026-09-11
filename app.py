import streamlit as st
from project import app

st.set_page_config(
    page_title="ScriptFlow AI",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 ScriptFlow AI")
st.caption("Turn your ideas into powerful content.")

st.divider()

# Input
st.subheader("💡 What's your idea?")

text = st.text_area(
    "Enter your content",
    height=200,
    placeholder="Paste your topic, idea or rough content here...",
    label_visibility="collapsed"
)

# Settings
col1, col2, col3, col4 = st.columns(4)

with col1:
    content_type = st.selectbox(
        "🎬 Content Type",
        [
            "YouTube Video",
            "YouTube Short",
            "Instagram Reel",
            "LinkedIn Post",
            "Blog Post"
        ]
    )

with col2:
    tone = st.selectbox(
        "🎭 Tone",
        [
            "Energetic",
            "Professional",
            "Educational",
            "Casual",
            "Funny",
            "Inspirational"
        ]
    )

with col3:
    language = st.selectbox(
        "🌐 Language",
        ["Hinglish", "English", "Hindi"]
    )

with col4:
    length = st.selectbox(
        "⏱️ Length",
        ["Short", "Medium", "Long"]
    )

st.write("")

# Generate
if st.button("🚀 Generate Content", type="primary", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some content first.")

    else:
        with st.spinner("✨ Creating your content..."):

            result = app.invoke({
                "raw_input": text,
                "content_type": content_type,
                "tone": tone,
                "language": language,
                "length": length
            })

        st.success("Your content is ready! 🎉")

        st.divider()

        # Results
        st.subheader("✨ Your Results")

        script_tab, hooks_tab, thumbnail_tab, seo_tab = st.tabs([
            "🎬 Script",
            "🔥 Hooks",
            "🖼️ Thumbnail",
            "🔍 SEO"
        ])

        with script_tab:
            st.write(result["final_output"])

            st.download_button(
                "📥 Download Script",
                result["final_output"],
                "script.txt",
                "text/plain"
            )

        with hooks_tab:
            st.write(result["hooks"])

        with thumbnail_tab:
            st.write(result["thumbnail"])

        with seo_tab:
            st.write(result["seo"])

        # Download everything
        all_content = f"""
SCRIPT

{result["final_output"]}


HOOKS

{result["hooks"]}


THUMBNAIL IDEAS

{result["thumbnail"]}


SEO

{result["seo"]}
"""

        st.download_button(
            "📄 Download Everything",
            all_content,
            "scriptflow_content.txt",
            "text/plain"
        )

st.divider()

st.caption("Built with ❤️ using Streamlit + LangGraph + Groq")

