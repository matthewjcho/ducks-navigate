"""
File: app.py
Authors: Alison Dutton, Matthew Cho, Sandhya Gottimukkala
Date: 11/14/2026
Description: Streamlit GUI for Ducks Navigate! Shows an interactive map of
the Stevens campus, lets the user pick a start and destination, and draws
the walking route on the map with step-by-step directions.

Run with:  python -m streamlit run app.py

The GUI expects a campus map object with these methods:
    get_locations()            -> {node_id: {"name", "lat", "lon", "kind"}}
    get_destinations()         -> {node_id: display_name}
    find_route(start, end)     -> (list_of_node_ids, total_distance_ft)
"""

import folium
import streamlit as st
from streamlit_folium import st_folium

# Switch to the real class once campus_map.py is ready:
# from campus_map import CampusMap
from mock_campus_map import MockCampusMap

STEVENS_CENTER = (40.7443, -74.0255)  # middle of campus
MAP_ZOOM = 17
FEET_PER_METER = 3.28084


@st.cache_resource
def load_campus():
    """Create the campus map once and reuse it on every rerun."""
    return MockCampusMap()  # later: CampusMap()


def format_distance(distance_ft, unit):
    """Return the distance as text in the unit the user picked."""
    if unit == "Meters":
        return f"{distance_ft / FEET_PER_METER:,.0f} m"
    return f"{distance_ft:,.0f} ft"


def show_header():
    """Display the title and how-to-use instructions."""
    st.title("🦆 Ducks Navigate!")
    st.write("Find a walking route between buildings on the Stevens campus.")
    with st.expander("How to use this app"):
        st.markdown(
            "1. Choose a **start** and **destination** in the sidebar.\n"
            "2. Click **Find Route** to draw the path on the map.\n"
            "3. Switch **units** or toggle **Show all campus points** anytime.\n"
            "4. Click **Clear** to reset and try another route."
        )


def show_sidebar(destinations):
    """Draw the sidebar controls and return the user's choices."""
    st.sidebar.header("Plan your route")
    ids = sorted(destinations, key=lambda node_id: destinations[node_id])

    # Elements 1-2: start and destination dropdowns
    start = st.sidebar.selectbox("Start", ids, format_func=destinations.get)
    end = st.sidebar.selectbox("Destination", ids, index=min(1, len(ids) - 1),
                               format_func=destinations.get)

    # Elements 3-4: display options
    unit = st.sidebar.radio("Distance units", ["Feet", "Meters"], horizontal=True)
    show_all = st.sidebar.toggle("Show all campus points", value=True)

    # Elements 5-6: action buttons
    col1, col2 = st.sidebar.columns(2)
    find = col1.button("Find Route", type="primary", use_container_width=True)
    clear = col2.button("Clear", use_container_width=True)

    return start, end, unit, show_all, find, clear


def build_map(locations, path, show_all):
    """Create the Folium campus map with markers and the route line."""
    campus_map = folium.Map(location=STEVENS_CENTER, zoom_start=MAP_ZOOM)

    # Background markers for every building and waypoint
    if show_all:
        for node_id, info in locations.items():
            if node_id in path:
                continue
            if info["kind"] == "building":
                folium.Marker((info["lat"], info["lon"]), tooltip=info["name"],
                              icon=folium.Icon(color="gray", icon="building", prefix="fa")
                              ).add_to(campus_map)
            else:
                folium.CircleMarker((info["lat"], info["lon"]), radius=4,
                                    tooltip=info["name"], color="gray",
                                    fill=True).add_to(campus_map)

    # Route: green start, red end, blue stops in between, line connecting them
    points = []
    for index, node_id in enumerate(path):
        info = locations[node_id]
        point = (info["lat"], info["lon"])
        points.append(point)
        if index == 0:
            color = "green"
        elif index == len(path) - 1:
            color = "red"
        else:
            color = "blue"
        folium.Marker(point, tooltip=info["name"], popup=info["name"],
                      icon=folium.Icon(color=color)).add_to(campus_map)

    if len(points) >= 2:
        folium.PolyLine(points, weight=6, opacity=0.85).add_to(campus_map)
        campus_map.fit_bounds(points, padding=(40, 40))

    return campus_map


def show_directions(locations, path, distance_ft, unit):
    """Show the route summary and numbered steps."""
    names = [locations[node_id]["name"] for node_id in path]
    st.success(f"**Route:** {' → '.join(names)}  \n"
               f"**Total distance:** {format_distance(distance_ft, unit)}")
    st.markdown("\n".join(f"{step}. {name}" for step, name in enumerate(names, start=1)))


def main():
    """Run the Ducks Navigate! app."""
    st.set_page_config(page_title="Ducks Navigate!", page_icon="🦆", layout="wide")
    show_header()

    campus = load_campus()
    locations = campus.get_locations()
    start, end, unit, show_all, find, clear = show_sidebar(campus.get_destinations())

    if clear:
        st.session_state.pop("route", None)

    if find:
        if start == end:
            st.info("You're already there! Pick a different destination.")
            st.session_state.pop("route", None)
        else:
            path, distance_ft = campus.find_route(start, end)
            st.session_state["route"] = (path, distance_ft)

    path, distance_ft = st.session_state.get("route", ([], 0))
    if find and not path and start != end:
        st.warning("No route found between those two places yet.")

    map_col, info_col = st.columns([3, 2])
    with map_col:
        st_folium(build_map(locations, path, show_all), height=520,
                  use_container_width=True, returned_objects=[])
    with info_col:
        if path:
            show_directions(locations, path, distance_ft, unit)
        else:
            st.info("Pick a start and destination, then click **Find Route**.")


if __name__ == "__main__":
    main()