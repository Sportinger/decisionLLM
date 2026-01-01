from typing import List, Tuple
import re
from collections import Counter


class ConsensusCalculator:
    """Calculate consensus between multiple LLM responses."""

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        # Tokenize
        words1 = set(ConsensusCalculator._tokenize(text1))
        words2 = set(ConsensusCalculator._tokenize(text2))

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union) if union else 0.0

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple tokenization: lowercase and split by non-alphanumeric."""
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        return words

    @classmethod
    def calculate_pairwise_consensus(cls, responses: List[str]) -> float:
        """Calculate average pairwise similarity across all responses."""
        if len(responses) < 2:
            return 1.0

        similarities = []
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                sim = cls.calculate_similarity(responses[i], responses[j])
                similarities.append(sim)

        return sum(similarities) / len(similarities) if similarities else 0.0

    @classmethod
    def find_most_central_response(cls, responses: List[str]) -> Tuple[int, str]:
        """Find the response that is most similar to all others."""
        if not responses:
            return -1, ""

        if len(responses) == 1:
            return 0, responses[0]

        # Calculate total similarity for each response
        total_similarities = []
        for i, response in enumerate(responses):
            total_sim = sum(
                cls.calculate_similarity(response, other)
                for j, other in enumerate(responses)
                if i != j
            )
            total_similarities.append(total_sim)

        best_idx = max(range(len(responses)), key=lambda i: total_similarities[i])
        return best_idx, responses[best_idx]

    @classmethod
    def extract_common_themes(cls, responses: List[str], min_freq: int = 2) -> List[str]:
        """Extract common themes/words across responses."""
        all_words = []
        for response in responses:
            words = cls._tokenize(response)
            all_words.extend(words)

        # Count word frequencies
        word_counts = Counter(all_words)

        # Filter by minimum frequency and remove common stop words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                      'would', 'could', 'should', 'may', 'might', 'must', 'can',
                      'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
                      'as', 'into', 'through', 'during', 'before', 'after',
                      'above', 'below', 'between', 'under', 'again', 'further',
                      'then', 'once', 'here', 'there', 'when', 'where', 'why',
                      'how', 'all', 'each', 'few', 'more', 'most', 'other',
                      'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                      'so', 'than', 'too', 'very', 'just', 'and', 'but', 'if',
                      'or', 'because', 'until', 'while', 'although', 'i', 'you',
                      'he', 'she', 'it', 'we', 'they', 'this', 'that', 'these',
                      'those', 'am'}

        common_themes = [
            word for word, count in word_counts.most_common(20)
            if count >= min_freq and word not in stop_words and len(word) > 2
        ]

        return common_themes[:10]
