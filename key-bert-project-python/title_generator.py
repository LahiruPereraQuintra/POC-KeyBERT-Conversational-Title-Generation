import time
from typing import Any, Dict, List, Optional, Tuple

from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from sentence_transformers import SentenceTransformer
from transformers import pipeline

from config import (
    CLASSIFIER_MODEL,
    INTENT_LABELS,
    INTENT_THRESHOLD,
    KEYBERT_MODEL,
    TOP_N_KEYWORDS,
)


class TitleGenerator:
    """
    Loads the embedding model + intent classifier once, then serves requests.
    """

    def __init__(self) -> None:
        # Force CPU usage explicitly (your POC requirement).
        embedding_model = SentenceTransformer(KEYBERT_MODEL, device="cpu")
        self.keybert = KeyBERT(model=embedding_model)

        # Extract grammatical keyphrases using spaCy POS patterns.
        self.keyphrase_vectorizer = KeyphraseCountVectorizer(
            spacy_pipeline="en_core_web_sm"
        )

        # Zero-shot multi-label intent classification via NLI pipeline.
        self.intent_classifier = pipeline(
            "zero-shot-classification",
            model=CLASSIFIER_MODEL,
            device=-1,  # CPU
        )

    def _extract_keyphrases(self, query: str) -> List[Tuple[str, float]]:
        # `extract_keywords` returns a list of (keyphrase, score).
        return self.keybert.extract_keywords(
            query,
            vectorizer=self.keyphrase_vectorizer,
            top_n=TOP_N_KEYWORDS,
        )

    def _detect_intents(self, query: str) -> List[str]:
        result = self.intent_classifier(
            query,
            candidate_labels=INTENT_LABELS,
            multi_label=True,
        )

        labels: List[str] = result.get("labels", [])
        scores: List[float] = result.get("scores", [])

        selected: List[str] = []
        for label, score in zip(labels, scores):
            if score > INTENT_THRESHOLD:
                selected.append(label)

        return selected

    @staticmethod
    def _derive_company(top_keyphrase: str) -> str:
        words = top_keyphrase.split()
        first_two = words[:2]
        return " ".join(first_two).title() if first_two else top_keyphrase.title()

    @staticmethod
    def _build_title(top_keyphrase: str, intents: List[str]) -> str:
        # Title case the keyphrase, as it represents the core topic.
        # e.g., "dividend yield" -> "Dividend Yield"
        topic = top_keyphrase.title()

        intent_set = set(intents)

        # 1. Error / Bug Fix (Highest priority if something is broken)
        if "error / bug fix" in intent_set:
            return f"{topic} Issue"

        # 2. How To / Tutorial
        if "how to / tutorial" in intent_set:
            if "explanation / definition" in intent_set:
                return f"Understanding {topic}"
            return f"{topic} Guide"

        # 3. Explanation / Definition
        if "explanation / definition" in intent_set:
            return f"{topic} Explained"

        # 4. Time Specific + Financial (Report/Trends)
        if "time specific" in intent_set and "financial query" in intent_set:
            # If the user asks about Apple stock price in 2024
            return f"{topic} Report"

        # 5. Generic Financial Query
        if "financial query" in intent_set:
            # Drop the hardcoded "Revenue". The `topic` is already a financial concept
            # (e.g., "Current Stock Price" or "Dividend Yield")
            return topic

        # Fallback for any other query
        return topic

    def generate(self, query: str) -> Dict[str, Any]:
        start = time.perf_counter()

        keywords = self._extract_keyphrases(query)
        top_keyphrase: str
        if keywords:
            top_keyphrase = keywords[0][0]
        else:
            top_keyphrase = query

        intents = self._detect_intents(query)
        title = self._build_title(top_keyphrase=top_keyphrase, intents=intents)

        duration_ms = int((time.perf_counter() - start) * 1000)
        return {
            "title": title,
            "keyphrase": top_keyphrase,
            "intents": intents,
            "duration_ms": duration_ms,
        }


_generator: Optional[TitleGenerator] = None


def get_title_generator() -> TitleGenerator:
    """
    Create/load models once. Intended to be called during FastAPI startup.
    """

    global _generator
    if _generator is None:
        _generator = TitleGenerator()
    return _generator

