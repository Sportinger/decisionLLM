"""Text similarity utilities."""

from typing import List
import re


def jaccard_similarity(text1: str, text2: str) -> float:
    """Calculate Jaccard similarity between two texts."""
    words1 = set(tokenize(text1))
    words2 = set(tokenize(text2))

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union) if union else 0.0


def tokenize(text: str) -> List[str]:
    """Simple tokenization: lowercase and split by non-alphanumeric."""
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return words


def cosine_similarity_simple(text1: str, text2: str) -> float:
    """Simple cosine similarity using word frequencies."""
    from collections import Counter

    words1 = tokenize(text1)
    words2 = tokenize(text2)

    counter1 = Counter(words1)
    counter2 = Counter(words2)

    # Get all unique words
    all_words = set(counter1.keys()) | set(counter2.keys())

    # Calculate dot product and magnitudes
    dot_product = sum(counter1.get(w, 0) * counter2.get(w, 0) for w in all_words)
    magnitude1 = sum(v ** 2 for v in counter1.values()) ** 0.5
    magnitude2 = sum(v ** 2 for v in counter2.values()) ** 0.5

    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)
