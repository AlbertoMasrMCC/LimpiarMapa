import xml.etree.ElementTree as ET
import csv

if __name__ == '__main__':
    # Parse the .osm file
    tree = ET.parse("Sector Centro.osm")
    root = tree.getroot()

    # Dictionary to store the node IDs and names
    node_data = {}

    # Create the node_id variable and initialize it to None
    node_ids = []

    # Iterate through the elements in the root node
    for element in root:
        # Check if the element is a node
        if element.tag == "node":
            # Iterate through the node's tag elements
            for tag in element:
                # Check if the tag is a "highway" tag
                if tag.attrib["k"] == "highway":
                    # Store the node ID, name and coordinates in the dictionary
                    node_id = element.attrib["id"]
                    node_data[node_id] = {
                        "name": None,
                        "lat": element.attrib["lat"],
                        "lon": element.attrib["lon"]
                    }
                    # Store the node ID in the list
                    node_ids.append(node_id)

    # Iterate through the elements in the root node again
    for element in root:
        # Check if the element is a way
        if element.tag == "way":
            # Iterate through the way's nd elements
            for nd in element:
                # Check if the nd has the node ID we are looking for
                if "ref" in nd.attrib and nd.attrib["ref"] in node_ids:
                    # Find the name of the street
                    street_name = None
                    for name_tag in element:
                        if "k" in name_tag.attrib and name_tag.attrib["k"] == "name":
                            street_name = name_tag.attrib["v"]
                        # Store the street name in the dictionary
                        node_data[nd.attrib["ref"]]["name"] = street_name

    # Print the node id, name and coordinates
    for node_id, data in node_data.items():
        print(f"{node_id}: {data['name']} ({data['lat']}, {data['lon']})")
        # Open the file in write mode with utf-8 encoding
        with open("node_data.csv", "w", newline="", encoding="utf-8") as csv_file:
            # Create a CSV writer object
            writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_ALL)
            # Write the header row
            writer.writerow(["lat", "lon", "name"])
            # Iterate through the node data
            for node_id, data in node_data.items():
                # Write a row for each node
                writer.writerow([data["lat"], data["lon"], data["name"]])