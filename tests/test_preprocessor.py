import pytest

from backend.app.engine.preprocessor import IndonesianPreprocessor


@pytest.fixture
def preprocessor() -> IndonesianPreprocessor:
    return IndonesianPreprocessor()


class TestCleanText:
    def test_lowercases_text(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.clean_text("HALO DUNIA") == "halo dunia"

    def test_removes_punctuation_and_special_characters(
        self, preprocessor: IndonesianPreprocessor
    ) -> None:
        assert preprocessor.clean_text("Halo, dunia! Apa kabar?") == "halo dunia apa kabar"

    def test_preserves_alphanumeric_tech_specs(
        self, preprocessor: IndonesianPreprocessor
    ) -> None:
        assert preprocessor.clean_text("Xiaomi 13T 8Gen2 120Hz 4K") == "xiaomi 13t 8gen2 120hz 4k"

    def test_collapses_whitespace(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.clean_text("halo    dunia") == "halo dunia"

    def test_empty_string(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.clean_text("") == ""


class TestTokenize:
    def test_splits_cleaned_text_into_tokens(
        self, preprocessor: IndonesianPreprocessor
    ) -> None:
        assert preprocessor.tokenize("halo dunia ini gadget") == [
            "halo",
            "dunia",
            "ini",
            "gadget",
        ]

    def test_empty_string(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.tokenize("") == []


class TestRemoveStopwords:
    def test_filters_common_indonesian_stopwords(
        self, preprocessor: IndonesianPreprocessor
    ) -> None:
        result = preprocessor.remove_stopwords(["ini", "adalah", "ulasan", "laptop", "bagus"])
        assert "ini" not in result
        assert "adalah" not in result
        assert "ulasan" in result
        assert "laptop" in result
        assert "bagus" in result

    def test_preserves_tech_modifiers(self, preprocessor: IndonesianPreprocessor) -> None:
        result = preprocessor.remove_stopwords(["xiaomi", "13t", "adalah", "bagus"])
        assert "xiaomi" in result
        assert "13t" in result
        assert "bagus" in result
        assert "adalah" not in result

    def test_empty_list(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.remove_stopwords([]) == []


class TestStemTokens:
    def test_stems_each_token(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.stem_tokens(["membeli", "memiliki", "terbaik"]) == [
            "beli",
            "milik",
            "baik",
        ]

    def test_preserves_tech_specs_after_stemming(
        self, preprocessor: IndonesianPreprocessor
    ) -> None:
        assert preprocessor.stem_tokens(["13t", "8gen2", "120hz", "4k"]) == [
            "13t",
            "8gen2",
            "120hz",
            "4k",
        ]

    def test_empty_list(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.stem_tokens([]) == []


class TestPreprocess:
    def test_executes_full_pipeline(self, preprocessor: IndonesianPreprocessor) -> None:
        result = preprocessor.preprocess("Xiaomi 13T adalah ponsel bagus dengan kamera 4K!")
        assert "13t" in result
        assert "4k" in result
        assert "ponsel" in result
        assert "kamera" in result
        assert "bagus" in result
        assert "adalah" not in result
        assert "dengan" not in result

    def test_empty_string(self, preprocessor: IndonesianPreprocessor) -> None:
        assert preprocessor.preprocess("") == []
