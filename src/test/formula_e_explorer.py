import unittest
from src.formula_e_explorer import (
    load_data,
    get_entity_name,
    get_entity_profile,
    find_entity_id_by_name,
    get_season_data,
    get_standings,
    get_races,
    get_race,
    search_races,
    calculate_total_points
)

class TestFormulaEExplorer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = load_data()

    def test_load_data(self):
        self.assertIsInstance(self.data, dict)

    def test_get_entity_name(self):
        self.assertEqual(get_entity_name(self.data, 'drivers', 'd1'), 'Sam Bird')

    def test_get_entity_profile(self):
        profile = get_entity_profile(self.data, 'drivers', 'd3')
        self.assertEqual(profile['name'], 'Sebastien Buemi')
        self.assertEqual(profile['nationality'], 'Swiss')

    def test_find_entity_id_by_name(self):
        self.assertEqual(find_entity_id_by_name(self.data, 'drivers', 'Jean-Eric Vergne'), 'd4')
        self.assertIsNone(find_entity_id_by_name(self.data, 'drivers', 'Unknown Driver'))

    def test_get_season_data(self):
        season_data = get_season_data(self.data, '2019-2020')
        self.assertIsNotNone(season_data)
        self.assertEqual(season_data['season_name'], '2019-2020')

    def test_get_standings(self):
        standings = get_standings(self.data, '2019-2020', 'drivers')
        self.assertEqual(len(standings), 4)
        self.assertEqual(standings[0]['driver_id'], 'd1')

    def test_get_races(self):
        races = get_races(self.data, '2019-2020')
        self.assertIn('Diriyah E-Prix', races)

    def test_get_race(self):
        race = get_race(self.data, '2019-2020', 'Mexico City E-Prix')
        self.assertIsNotNone(race)
        self.assertEqual(race['location'], 'Mexico City, Mexico')

    def test_search_races(self):
        races = search_races(self.data, 'Mexico')
        self.assertEqual(len(races), 1)
        self.assertEqual(races[0]['race_name'], 'Mexico City E-Prix')

    def test_calculate_total_points(self):
        points = calculate_total_points(self.data, 'd1')
        self.assertEqual(points, 120)

if __name__ == '__main__':
    unittest.main()