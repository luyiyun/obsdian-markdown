def preprocess(s: str, end: str = "\n") -> str:
    s = s.replace("\r\n", "\n")
    s = s.replace("\r", "\n")
    if end and not s.endswith(end):
        s += end
    return s
