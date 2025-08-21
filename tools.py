def lietuvos_darbo_kodeksas_tool(question: str) -> str:
    """Tool to answer questions about Lithuanian Labor Code"""
    return f"Mock answer for Lithuanian Labor Code question: '{question}' - This would contain relevant information from the labor code."

TOOLS = {
    "lietuvos_darbo_kodeksas": {
        "function": lietuvos_darbo_kodeksas_tool,
        "description": "Answers questions about Lithuanian Labor Code (Lietuvos darbo kodeksas)"
    }
}