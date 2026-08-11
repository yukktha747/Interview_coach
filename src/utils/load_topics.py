from pathlib import Path
import re


def load_topics(data_dir):
    data_path = Path(data_dir)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Data directory does not exist: {data_path}"
        )

    topics = []

    for file_path in data_path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        match = re.search(
            r"^#\s+(.+)$",
            content,
            re.MULTILINE
        )

        if match:
            topics.append(match.group(1).strip())

    return sorted(set(topics))