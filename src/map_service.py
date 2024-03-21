import folium
from db_module import get_all_restaurants


def get_map():
    map_location = (60.165, 24.94)
    m = folium.Map(location=map_location, zoom_start=14, tiles='cartodbpositron')
    for restaurant_id, name, lat, lng in get_all_restaurants():
        folium.Marker(
            location=[lat, lng],
            tooltip=name,
            popup=f"<a href='/restaurants/{ restaurant_id }'>{name}</a>",
            icon=folium.Icon(icon='cutlery', color='cadetblue'),
            ).add_to(m)
    m.get_root().height = '600px'
    return m.get_root()._repr_html_()
