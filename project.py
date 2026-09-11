from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()


class PipelineState(TypedDict):
    raw_input: str
    content_type: str
    tone: str
    language: str
    length: str
    edited_text: str
    script_text: str
    final_output: str
    hooks: str
    thumbnail: str
    seo: str


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7
)


def editor_node(state: PipelineState):
    print("\n--- Editor ---")

    prompt = (
        "You are an expert copyeditor. "
        "Clean the following content by fixing grammar, spelling "
        "and unclear sentences while preserving the original meaning. "
        "Return only the improved content.\n\n"
        f"{state['raw_input']}"
    )

    response = llm.invoke(prompt)

    return {
        "edited_text": response.content.strip()
    }


def scriptwriter_node(state: PipelineState):
    print("\n--- Scriptwriter ---")

    prompt = (
        "You are an expert content creator.\n\n"
        f"Content type: {state['content_type']}\n"
        f"Tone: {state['tone']}\n"
        f"Length: {state['length']}\n"
        f"Language: {state['language']}\n\n"
        "Transform the edited content into engaging content "
        "appropriate for the selected content type.\n\n"
        "Requirements:\n"
        "- Make it engaging and conversational.\n"
        "- Start with a strong hook.\n"
        "- Keep the explanation easy to follow.\n"
        "- Respect the requested tone and length.\n"
        "- Do not add unrelated information.\n"
        "- Return only the content.\n\n"
        f"Content:\n{state['edited_text']}"
    )

    response = llm.invoke(prompt)

    return {
        "script_text": response.content.strip()
    }


def translator_node(state: PipelineState):
    print("\n--- Language Converter ---")

    prompt = (
        f"Convert the following content into natural {state['language']}.\n\n"
        "Do not translate word-for-word. "
        "Make the result sound natural to a native speaker. "
        "Preserve the original meaning, energy and tone. "
        "Return only the final content.\n\n"
        f"Content:\n{state['script_text']}"
    )

    response = llm.invoke(prompt)

    return {
        "final_output": response.content.strip()
    }


def hook_node(state: PipelineState):
    print("\n--- Hook Generator ---")

    prompt = (
        "Generate 5 highly engaging hooks based on the following content.\n\n"
        "Requirements:\n"
        "- Short and punchy.\n"
        "- Create curiosity.\n"
        "- Suitable for social media.\n"
        "- Match the content tone.\n"
        "- Do not repeat the same idea.\n\n"
        f"Content:\n{state['final_output']}"
    )

    response = llm.invoke(prompt)

    return {
        "hooks": response.content.strip()
    }


def thumbnail_node(state: PipelineState):
    print("\n--- Thumbnail Generator ---")

    prompt = (
        "Create 3 clickable thumbnail concepts for the following content.\n\n"
        "For every concept provide:\n"
        "1. Thumbnail text\n"
        "2. Main visual\n"
        "3. Background/color style\n"
        "4. Emotion or expression\n\n"
        "Keep the concepts simple, bold and visually strong.\n\n"
        f"Content:\n{state['final_output']}"
    )

    response = llm.invoke(prompt)

    return {
        "thumbnail": response.content.strip()
    }


def seo_node(state: PipelineState):
    print("\n--- SEO Optimizer ---")

    prompt = (
        "Create a complete SEO package for the following content.\n\n"
        "Provide:\n"
        "1. 5 SEO-friendly titles\n"
        "2. A compelling description\n"
        "3. 15 relevant keywords\n"
        "4. 10 relevant hashtags\n\n"
        "Make the titles clickable without misleading clickbait. "
        "Return everything in a clean format.\n\n"
        f"Content:\n{state['final_output']}"
    )

    response = llm.invoke(prompt)

    return {
        "seo": response.content.strip()
    }


graph = StateGraph(PipelineState)

graph.add_node("editor", editor_node)
graph.add_node("scriptwriter", scriptwriter_node)
graph.add_node("translator", translator_node)
graph.add_node("hooks", hook_node)
graph.add_node("thumbnail", thumbnail_node)
graph.add_node("seo", seo_node)

graph.add_edge(START, "editor")
graph.add_edge("editor", "scriptwriter")
graph.add_edge("scriptwriter", "translator")

graph.add_edge("translator", "hooks")
graph.add_edge("translator", "thumbnail")
graph.add_edge("translator", "seo")

graph.add_edge("hooks", END)
graph.add_edge("thumbnail", END)
graph.add_edge("seo", END)

app = graph.compile()
