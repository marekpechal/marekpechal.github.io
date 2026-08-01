import json, os
import yaml

def export_geojson(filename, line_string_list):

    # Structure the data into a valid GeoJSON LineString
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": line_string
                }
            }
        for line_string in line_string_list]
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(geojson_data, f, indent=2)

def import_geojson(filename):
    with open(filename, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    pts = []
    for feature in json_data["features"]:
        print("processing feature")
        if feature["type"] == "Feature" and feature["geometry"]["type"] == "LineString":
            print("matching")
            pts += list(feature["geometry"]["coordinates"])
        print("done")
    return pts

def slugify(s):
    return s.replace(" ", "-").lower()

data_file = os.path.join(os.path.dirname(__file__), '../../_data/hiking.yml')
input_map_dir = os.path.join(os.path.dirname(__file__), '../../assets/maps/')
output_map_dir = os.path.join(os.path.dirname(__file__), '../../assets/maps/combined/')

print([fname for fname in os.listdir(input_map_dir) if fname.endswith(".geojson")])

with open(data_file, 'r') as file:
    hiking_data_yml = yaml.safe_load(file)

for route in hiking_data_yml["routes"]:
    line_string_list = [[]]
    for i in range(len(route["places"])-1):
        map_name = \
            "map_" + \
            slugify(route["places"][i]["name"]) + \
            "_" + \
            slugify(route["places"][i+1]["name"]) + \
            ".geojson"
        full_file_path = os.path.join(input_map_dir, map_name)
        line_string_list[0] += import_geojson(full_file_path)
    os.makedirs(output_map_dir, exist_ok=True)
    full_file_path = os.path.join(output_map_dir, route["map_filename"]+".geojson")
    export_geojson(full_file_path, line_string_list)
