from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage

def convert_message(m):
    if m["role"] == "user":
        return HumanMessage(content=m["content"])
    elif m["role"] == "assistant":
        return AIMessage(content=m["content"])
    elif m["role"] == "system":
        return SystemMessage(content=m["content"])
    else:
        raise ValueError(f"Unknown role {m['role']}")

