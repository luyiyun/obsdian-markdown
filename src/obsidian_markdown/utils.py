def preprocess(s: str) -> str:
    s = s.replace("\r\n", "\n")
    s = s.replace("\r", "\n")
    if not s.endswith("\n"):
        s += "\n"
    return s.lstrip(" \t\n\r")
