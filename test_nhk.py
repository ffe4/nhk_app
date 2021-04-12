import pytest

from nhk import NHK

nhk = NHK('data/nhk_dict.xml')


@pytest.mark.parametrize('query,expected_ids', [
    ('間', {'160', '1010', '109670', '500750'})
])
def test_find_items(query, expected_ids):
    actual_ids = {item.get('id') for item in nhk.find_items(query)}
    assert actual_ids == expected_ids
