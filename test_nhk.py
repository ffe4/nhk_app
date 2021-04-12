import pytest

from nhkdict import NHKDict, NHKAudio


class TestNHKDict:
    @classmethod
    def setup_class(cls):
        cls.nhk = NHKDict("data/nhk_dict.xml")

    @pytest.mark.parametrize(
        "query,expected_ids", [("間", {"160", "1010", "109670", "500750"})]
    )
    def test_find_items(self, query, expected_ids):
        actual_ids = {item.get("id") for item in self.nhk.find_items(query)}
        assert actual_ids == expected_ids

    def test_lookup(self):
        query = "間"
        expected_titles = {
            "愛，相〔接〕，あい《間》（間隔），藍，合い（～の洋服）",
            "間",
            "官，巻，感，缶，観，間，棺，款，管，環，漢，冠（～たる），かん《緘，鐶》，歓，閑，艦，かん《奸》（君側の～）",
            "間（室，拍子），真（～に受ける）",
        }
        results = self.nhk.lookup(query)
        actual_titles = {result.title for result in results}
        assert len(results) == 4
        assert actual_titles == expected_titles


class TestNHKAudio:
    @classmethod
    def setup_class(cls):
        cls.snd = NHKAudio('file:data/Accent-snd.db?mode=ro')

    @pytest.mark.parametrize('name,size', [
        ('J00003', 4401),
        ('K90542', 11107),
    ])
    def test_get(self, name, size):
        file = self.snd.get(name)
        assert len(file) == size, file
