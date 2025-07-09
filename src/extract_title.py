def extract_title(markdown: str):
    markdown = markdown.lstrip()
    if markdown[:2] != "# ":
        raise Exception("Invalid starting header in markdown file")
    return markdown[2:].split("\n")[0].strip()
