import json
import re
from ast import literal_eval
from uuid import uuid4
from typing import Dict, Iterator, List

import streamlit as st

# ------------------ GLOBAL STYLES ------------------ #
st.markdown(
    """
    <style>
        .box-tag {
            display:inline-block;
            background:var(--secondary-background-color, #444);
            color: var(--text-color, #eee);
            border:1px solid #666;
            border-radius:6px;
            padding:2px 6px;
            margin:2px 4px;
            font-size:0.8rem;
        }
        .faded {
            opacity:0.65;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------ SIDEBAR ------------------ #
with st.sidebar:
    st.title("💬 Questões Propostas")

    if st.button("➕ Nova Questão"):
        cid = str(uuid4())
        
    

# ------------------ HELPERS ------------------ #

def parse_retrieval_list(raw: str) -> List[Dict]:
    """Convert backend string to list of metadata dicts."""
    if not raw:
        return []
    # backend envia string com aspas simples → trocamos por duplas para JSON
    try:
        cleaned = re.sub(r"'", '"', raw)
        docs = json.loads(cleaned)
        if isinstance(docs, list):
            return [d for d in docs if isinstance(d, dict)]
    except Exception:
        pass
    # fallback literal_eval
    try:
        docs = literal_eval(raw)
        return [d for d in docs if isinstance(d, dict)]
    except Exception:
        return []


def boxes_html(docs: List[Dict]) -> str:
    rendered = []
    for d in docs:
        parts = [f"{k}: {v}" for k, v in d.items()]
        rendered.append(f"<span class='box-tag'>{' · '.join(parts)}</span>")
    return " ".join(rendered)


def render_saved(msg: Dict):
    role = "assistant" if msg["origin"] != "user" else "user"
    with st.chat_message(role):
        if msg["origin"] == "user":
            st.markdown(msg["content"])
        else:
            faded_cls = "faded" if msg["type"] in {"thoughts", "retrieval_result"} else ""
            st.markdown(f"<div class='{faded_cls}'><strong>{msg['agent']}</strong>: {msg['content']}</div>", unsafe_allow_html=True)
            if msg.get("docs"):
                st.markdown(boxes_html(msg["docs"]), unsafe_allow_html=True)


def consume_stream(prompt: str, checkpoint: str | None, store: Dict):
    events: Iterator[Dict] = get_chat_stream(prompt, checkpoint)

    final_text = ""
    final_agent = None
    final_placeholder = None

    for ev in events:
        
        if st.session_state.stop_generation:
            break

        etype = ev.get("type")

        if etype == "checkpoint":
            store["checkpoint_id"] = ev.get("checkpoint_id")
            continue

        if etype in ("thoughts", "retrieval_result"):
            
            agent = ev.get("agent", "assistant")
            content = ev.get("content", "")

            docs = parse_retrieval_list(ev.get("retrieval_result", "")) if etype == "retrieval_result" else dict()


            with st.chat_message("assistant"):
                st.markdown(f"<div class='faded'><strong>{agent}</strong>: {content}</div>", unsafe_allow_html=True)
                if docs:
                    st.markdown(boxes_html(docs), unsafe_allow_html=True)

            store["messages"].append({
                "origin": "assistant",
                "type": etype,
                "agent": agent,
                "content": content,
                "docs": docs,
            })

        elif etype == "final_answer":
            if final_agent is None:
                final_agent = ev.get("agent", "assistant")
                container = st.chat_message("assistant")
                with container:
                    final_placeholder = st.empty()
            final_text += ev.get("content", "")
            if final_placeholder:
                final_placeholder.markdown(f"**{final_agent}**: {final_text}▌")

                
        elif etype == "end":
            if final_agent and final_placeholder:
                final_placeholder.markdown(f"**{final_agent}**: {final_text}")
                store["messages"].append({
                    "origin": "assistant",
                    "type": "final_answer",
                    "agent": final_agent,
                    "content": final_text,
                })
            break

# ------------------ MAIN ------------------ #

st.title("🦜 CAGEChat")
chat = st.session_state.chats[st.session_state.current_chat]

for m in chat["messages"]:
    render_saved(m)

user_query = st.chat_input("Digite sua pergunta…")
stop_box = st.empty()

if user_query:
    chat["messages"].append({"origin": "user", "content": user_query})
    render_saved(chat["messages"][-1])

    stop_box.button("⏹️ Parar", key="stop_btn", on_click=lambda: st.session_state.__setitem__("stop_generation", True))

    consume_stream(user_query, chat["checkpoint_id"], chat)

    st.session_state.stop_generation = False
    stop_box.empty()
