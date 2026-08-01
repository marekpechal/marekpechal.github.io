import json, os
import yaml
import matplotlib.pyplot as plt
import matplotlib

colors = [
    c if isinstance(c, str) else matplotlib.colors.rgb2hex(c)
    for c in plt.rcParams['axes.prop_cycle'].by_key()['color']]


def export_geojson(filename, line_string_list):

    # Structure the data into a valid GeoJSON LineString
    geojson_data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"stroke": line_string["stroke"]}
                    if "stroke" in line_string else {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": line_string["coordinates"]
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
os.makedirs(output_map_dir, exist_ok=True)

print([fname for fname in os.listdir(input_map_dir) if fname.endswith(".geojson")])

with open(data_file, 'r') as file:
    hiking_data_yml = yaml.safe_load(file)

line_string_list = []
for route in hiking_data_yml["routes"]:
    line_string = []
    for i in range(len(route["places"])-1):
        map_name = \
            "map_" + \
            slugify(route["places"][i]["name"]) + \
            "_" + \
            slugify(route["places"][i+1]["name"]) + \
            ".geojson"
        full_file_path = os.path.join(input_map_dir, map_name)
        line_string += import_geojson(full_file_path)
    line_string_list.append(line_string)
    full_file_path = os.path.join(output_map_dir, route["map_filename"]+".geojson")
    export_geojson(full_file_path, [{"coordinates": line_string}])

full_file_path = os.path.join(output_map_dir, "map_all.geojson")
export_geojson(full_file_path, [{"coordinates": line_string, "stroke": color}
    for line_string, color in zip(line_string_list, colors)])
