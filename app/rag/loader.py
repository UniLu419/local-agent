from pathlib import Path
from typing import Any, Dict, List


def load_documents(path: str) -> List[Dict[str, Any]]:
    """Placeholder document loader for RAG pipelines."""
    p = Path(path)
    if not p.exists():
        return []
    # For now just return file paths as documents; extend as needed.
    return [{"id": str(p), "text": p.read_text(encoding="utf-8")}]

