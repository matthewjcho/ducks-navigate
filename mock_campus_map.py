"""
File: mock_campus_map.py
Authors: Alison Dutton, Matthew Cho, Sandhya Gottimukkala
Date: 11/14/2026
Description: TEMPORARY stand-in for the real CampusMap class, used only to
build and preview the GUI before campus_map.py is finished. It returns
hardcoded sample locations and one precomputed path. It contains no real
data loading or routing logic. Delete this file once campus_map.py works.
"""


class MockCampusMap:
    """Fake campus map with the same method names the GUI expects."""

    def __init__(self):
        # Sample points copied from data/buildings.csv and data/intersections.csv
        self.locations = {
            "BABBIO": {"name": "Babbio Center", "lat": 40.7429031, "lon": -74.02669028, "kind": "building"},
            "GATEWAY": {"name": "Gateway Academic Center", "lat": 40.74332986, "lon": -74.02761749, "kind": "building"},
            "LIBRARY": {"name": "Samuel C. Williams Library", "lat": 40.74485912, "lon": -74.02532771, "kind": "building"},
            "HOWE": {"name": "Wesley J. Howe Center", "lat": 40.74509264, "lon": -74.02413783, "kind": "building"},
            "UCC": {"name": "University Center Complex", "lat": 40.74385221, "lon": -74.02509302, "kind": "building"},
            "WP_RIVER_6TH": {"name": "River + 6th", "lat": 40.74309495, "lon": -74.0270064, "kind": "waypoint"},
            "WP_PEIRCE_MORTON": {"name": "Peirce + Morton", "lat": 40.7433343, "lon": -74.02683023, "kind": "waypoint"},
        }
        # One hardcoded sample result: Babbio -> Peirce + Morton
        self.sample_path = ["BABBIO", "WP_RIVER_6TH", "WP_PEIRCE_MORTON"]
        self.sample_distance_ft = 111.5 + 91.35

    def get_locations(self):
        """Return every point to draw on the map (id -> info dict)."""
        return self.locations

    def get_destinations(self):
        """Return the choices for the dropdowns (id -> display name)."""
        return {node_id: info["name"] for node_id, info in self.locations.items()}

    def find_route(self, start_id, end_id):
        """Return (path, total_distance_ft); ([], 0) when no route exists."""
        if [start_id, end_id] == [self.sample_path[0], self.sample_path[-1]]:
            return self.sample_path, self.sample_distance_ft
        if [end_id, start_id] == [self.sample_path[0], self.sample_path[-1]]:
            return list(reversed(self.sample_path)), self.sample_distance_ft
        return [], 0