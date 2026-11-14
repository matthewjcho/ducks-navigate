# 🦆 Ducks Navigate!

An accessible campus route planner for Stevens Institute of Technology. Pick a starting building and a destination, and Ducks Navigate! shows you the walking route on an interactive campus map with step-by-step directions.

**Team:** Alison Dutton, Matthew Cho, Sandhya Gottimukkala
**Course:** AAI 551

---

## Requirements

- Python **3.12 or later**
- The packages listed in `requirements.txt`:
  - `streamlit` (GUI)
  - `pandas` (loading and cleaning the CSV data)
  - `networkx` (building the campus graph and finding routes)
  - `folium` and `streamlit-folium` (interactive campus map)
  - `pytest` (tests)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/matthewjcho/ducks-navigate.git
   cd ducks-navigate
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install the packages**
   ```bash
   python -m pip install -r requirements.txt
   ```

## Running the App

From the project folder, run:

```bash
python -m streamlit run app.py
```

The app opens in your browser at **http://localhost:8501**. If it doesn't open automatically, copy that link into your browser.

To stop the app, go back to the terminal and press **Ctrl + C**.

## How to Use

1. **Choose your start** from the **Start** dropdown in the left sidebar.
2. **Choose your destination** from the **Destination** dropdown.
3. Click **Find Route**.
4. The route appears on the campus map:
   - 🟢 **Green marker:** your starting point
   - 🔵 **Blue markers:** stops along the way
   - 🔴 **Red marker:** your destination
   - The blue line shows the walking path.
5. The panel next to the map lists each step and the **total walking distance**.
6. Use the extra controls anytime:
   - **Distance units:** switch between feet and meters.
   - **Show all campus points:** show or hide the other buildings and waypoints on the map.
   - **Clear:** reset the route and start over.

If no route exists between two places, the app shows a message instead of a path. Try a different start or destination.

## Running the Tests

```bash
python -m pytest
```

## Project Structure

```
ducks-navigate/
├── app.py               # Streamlit GUI (map, controls, directions)
├── campus_map.py        # CampusMap class: loads data, builds graph, finds routes
├── building.py          # Building class
├── route.py             # Route class (one path segment)
├── data/
│   ├── buildings.csv          # Stevens buildings and reference coordinates
│   ├── intersections.csv      # Walkway waypoints used to connect buildings
│   ├── routes.csv             # Path segments between buildings/waypoints (distances in feet)
│   ├── entrances.csv          # Building entrances
│   ├── building_entrances.csv # Links buildings to their entrances
│   └── points_of_interest.csv # Places inside buildings (e.g., cafes)
├── tests/
│   └── test_campus_map.py     # pytest tests
├── docs/                # Diagrams
├── archive/             # Early research notebooks
├── requirements.txt
└── README.md
```

## Data Sources

- Building names and map numbers: official Stevens campus map
- Coordinates: OpenStreetMap and Google Maps, checked by the team
- Distances: measured between campus points (in feet)

Some coordinates and routes are still being verified, so the campus coverage will grow as more data is added.
