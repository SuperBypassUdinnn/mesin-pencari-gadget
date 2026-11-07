import re
from typing import List

from Sastrawi.StopWordRemover.StopWordRemoverFactory import (
    StopWordRemoverFactory,
)
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class IndonesianPreprocessor:
    """Indonesian text preprocessing engine backed by PySastrawi.

    Provides text normalization (lowercasing, punctuation removal),
    tokenization, Indonesian stopword removal, and morphological stemming
    for gadget search indexing.
    """

    def __init__(self) -> None:
        self._stop_word_remover = StopWordRemoverFactory().create_stop_word_remover()
        self._stemmer = StemmerFactory().create_stemmer()

    def clean_text(self, text: str) -> str:
        """Lowercase text and strip punctuation/special characters.

        Alphanumeric technical specifications (e.g. ``13t``, ``8gen2``,
        ``120hz``, ``4k``) are preserved since they consist solely of
        letters and digits.
        """
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
        """Filter out common Indonesian stopwords using PySastrawi.

        Tech modifiers that are not stopwords (e.g. ``13t``, ``8gen2``)
        are preserved.
        """
        if not tokens:
            return []
        cleaned = self._stop_word_remover.remove(" ".join(tokens))
        return [token for token in cleaned.split() if token]

    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Stem each token using PySastrawi's morphological stemmer."""
        return [self._stemmer.stem(token) for token in tokens]

    def preprocess(self, text: str) -> List[str]:
        """Run the full preprocessing pipeline.

        ``clean_text`` -> ``tokenize`` -> ``remove_stopwords`` ->
        ``stem_tokens``.
        """
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        filtered = self.remove_stopwords(tokens)
        return self.stem_tokens(filtered)
