import pytest

from utils.utils import get_lat_long_from_city


class TestGetLatLong:
    def test_get_lat_long_from_real_city(self):
        test_city = "Tokyo"
        expected_lat_long = (35.6870, 139.7495)
        lat_long = get_lat_long_from_city(test_city)
        assert lat_long == expected_lat_long

    def test_get_lat_long_from_non_existent_city(self):
        test_city = "NonExistentCity"
        with pytest.raises(ValueError) as e:
            get_lat_long_from_city(test_city)
        assert str(e.value) == "'NonExistentCity' not found in the dataset."

    def test_get_lat_long_from_city_with_extra_spaces(self):
        test_city = "  London  "
        expected_lat_long = (51.5072, -0.1275)
        lat_long = get_lat_long_from_city(test_city)
        assert lat_long == expected_lat_long

    def test_get_lat_long_from_non_ascii_city_(self):
        test_city = "São Paulo"
        expected_lat_long = (-23.5504, -46.6339)
        lat_long = get_lat_long_from_city(test_city)
        assert lat_long == expected_lat_long
