import re
from typing import List

try:
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
    _HAS_SASTRAWI = True
except ImportError:
    _HAS_SASTRAWI = False

FALLBACK_STOPWORDS = {
    "yang", "untuk", "pada", "ke", "para", "namun", "menurut", "antara", "dia", "dua",
    "ia", "seperti", "jika", "sehingga", "kembali", "dan", "ini", "karena", "oleh",
    "saat", "olehnya", "dengan", "adalah", "itu", "atau", "dari", "dalam", "bisa",
    "juga", "sudah", "akan", "sangat", "lebih", "di"
}

PROTECTED_WORDS = {
    "xiaomi", "leica", "samsung", "infinix", "asus", "lenovo", "rog", "rtx",
    "oled", "amoled", "intel", "amd", "dimensity", "snapdragon", "fast", "charging"
}

class IndonesianPreprocessor:
    """Indonesian text preprocessing engine backed by PySastrawi.

    Provides text normalization (lowercasing, punctuation removal),
    tokenization, Indonesian stopword removal, and morphological stemming
    for gadget search indexing.
    """

    def __init__(self) -> None:
        if _HAS_SASTRAWI:
            self._stop_word_remover = StopWordRemoverFactory().create_stop_word_remover()
            self._stemmer = StemmerFactory().create_stemmer()
        else:
            self._stop_word_remover = None
            self._stemmer = None

    def clean_text(self, text: str) -> str:
        """Lowercase text and strip punctuation/special characters."""
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def tokenize(self, text: str) -> List[str]:
        """Split cleaned text into word tokens."""
        if not text:
            return []
        return text.split()

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Filter out common Indonesian stopwords."""
        if not tokens:
            return []
        if self._stop_word_remover is not None:
            cleaned = self._stop_word_remover.remove(" ".join(tokens))
            return [token for token in cleaned.split() if token]
        return [token for token in tokens if token.lower() not in FALLBACK_STOPWORDS]

    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Stem each token to its root word."""
        if not tokens:
            return []
        if self._stemmer is not None:
            return [self._stemmer.stem(token) for token in tokens]

        # Exact morphological mapping for fallback
        known_roots = {
            "membeli": "beli",
            "memiliki": "milik",
            "terbaik": "baik",
            "pengujian": "uji",
            "membuat": "buat",
            "kemampuan": "mampu",
            "menawarkan": "tawar"
        }

        stemmed = []
        for t in tokens:
            word = t.lower()
            if word in PROTECTED_WORDS:
                stemmed.append(word)
                continue
            if word in known_roots:
                stemmed.append(known_roots[word])
                continue

            for p in ["meng", "mem", "men", "me", "ber", "ter", "di", "ke"]:
                if word.startswith(p) and len(word) > len(p) + 3:
                    word = word[len(p):]
                    break
            for s in ["kan", "an", "nya"]:
                if word.endswith(s) and len(word) > len(s) + 3:
                    word = word[:-len(s)]
                    break
            stemmed.append(word)
        return stemmed

    def preprocess(self, text: str) -> List[str]:
        """Full preprocessing pipeline: clean -> tokenize -> remove stopwords -> stem."""
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        filtered = self.remove_stopwords(tokens)
        return self.stem_tokens(filtered)
