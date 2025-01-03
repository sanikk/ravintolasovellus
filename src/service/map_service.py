import folium

from db_module import get_restaurants_all


def get_map_data():
    restaurants = get_restaurants_all()
    return [(r.id, r.name, r.latitude, r.longitude) for r in restaurants]


def get_map():
    map_location = (60.165, 24.94)
    m = folium.Map(location=map_location, zoom_start=14, tiles="cartodbpositron")
    for id, name, lat, long in get_map_data():
        if not lat or not long:
            continue
        folium.Marker(
            location=[lat, long],
            tooltip=name,
            popup=f"<a href='/restaurants/{ id }'>{name}</a>",
            icon=folium.Icon(icon="cutlery", color="cadetblue"),
        ).add_to(m)

    m.get_root().height = "600px"
    return m.get_root()._repr_html_()
