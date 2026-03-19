"""
Central configuration for the KeyBERT + zero-shot title generator service.

Kept as plain Python constants so they can be easily edited or imported elsewhere.
"""

# Intent labels used by the zero-shot classifier.
INTENT_LABELS = [
    "financial query",
    "time specific",
    "how to / tutorial",
    "error / bug fix",
    "explanation / definition",
]

# Model names to load from Hugging Face.
KEYBERT_MODEL = "all-MiniLM-L6-v2"
CLASSIFIER_MODEL = "cross-encoder/nli-MiniLM2-L6-H768"

# Intent selection threshold. An intent is selected when score > this value.
INTENT_THRESHOLD = 0.5

# Number of top keyphrases to extract.
TOP_N_KEYWORDS = 2

# FastAPI host/port.
HOST = "0.0.0.0"
PORT = 8000

