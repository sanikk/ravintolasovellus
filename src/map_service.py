import folium
from db_module import get_restaurants_all


def get_map():
    map_location = (60.165, 24.94)
    m = folium.Map(location=map_location, zoom_start=14, tiles="cartodbpositron")
    for (
        restaurant_id,
        name,
        admin_id,
        lat,
        lng,
        place_id,
        address,
    ) in get_restaurants_all():
        if not lat or lng:
            continue
        folium.Marker(
            location=[lat, lng],
            tooltip=name,
            popup=f"<a href='/restaurants/{ restaurant_id }'>{name}</a>",
            icon=folium.Icon(icon="cutlery", color="cadetblue"),
        ).add_to(m)
    m.get_root().height = "600px"
    return m.get_root()._repr_html_()
