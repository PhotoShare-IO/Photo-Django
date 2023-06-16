def truncate_long_text(text: str) -> str:
    return (text[:30] + "...") if len(text) > 30 else text
