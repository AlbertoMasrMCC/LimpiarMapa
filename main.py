import xml.etree.ElementTree as ET
import csv

# Validamos si la esquina se encuentra en una calle distinta a la que se esta analizando
def validateCorner(root, name, corner_id):
    for element in root:
        if element.tag == "way":
            for tag in reversed(element):
                if tag.tag == "tag" and tag.attrib['k'] == "name":
                    if tag.attrib["v"] == name:
                        break
                if tag.tag == "tag" and tag.attrib['k'] == "service":
                    break
                if tag.tag == "tag" and tag.attrib['k'] == "highway":
                    # Recorrer todos los nodos del elemento "way"
                    for nd in element:
                        if nd.tag == "nd" and nd.attrib["ref"] == corner_id:
                            return True
    return False

if __name__ == '__main__':

    # Convertir el archivo OSM a XML
    tree = ET.parse("Sector Centro.osm")
    root = tree.getroot()

    # Diccionario para almacenar las esquinas de cada calle
    corners = {}

    # Lista para almacenar las calles con las coordenadas de sus esquinas
    street_corners = []

    # Recorre todos los elementos del árbol XML
    for element in root:
        if element.tag == "way":
            # Recorre todos los elementos "tag" del elemento "way"
            for tag in element:
                if tag.tag == "tag" and tag.attrib['k'] == "highway":
                    # Obtiene el nombre de la calle (si está presente)
                    name = None
                    for name_tag in element:
                        if name_tag.tag == "tag" and name_tag.attrib['k'] == "name":
                            name = name_tag.attrib["v"]
                            break
                    # Si la calle no está en el diccionario, la añade con una lista vacía
                    if name not in corners:
                        corners[name] = []
                    # Recorre todos los elementos "nd" (nodos) del elemento "way"
                    for nd in element:
                        if nd.tag == "nd":
                            # Si el nodo no está en la lista de esquinas de la calle, lo añade
                            if validateCorner(root, name, nd.attrib["ref"]):
                                corners[name].append(nd.attrib["ref"])

    # Iterar e imprimir cada nombre de la esquina y sus esquinas
    for name, corner_ids in corners.items():
        # Iterar sobre las esquinas de la calle
        for corner_id in corner_ids:
            # Recorrer todos los nodos del árbol XML
            for element in root:
                if element.tag == "node" and element.attrib["id"] == corner_id:
                    street_corners.append([element.attrib["lat"], element.attrib["lon"], "", "", name])

    for i, record in enumerate(street_corners):
        # Si el índice del elemento actual es mayor que 0 (es decir, si no es el primer elemento de la lista)
        if i > 0:
            # Si el nombre de la calle del elemento actual es igual al nombre de la calle del elemento anterior
            if record[4] == street_corners[i - 1][4]:
                # Asigna las coordenadas del elemento actual a la latitud y longitud final del elemento anterior
                street_corners[i - 1][2] = record[0]
                street_corners[i - 1][3] = record[1]
            # Si el nombre de la calle del elemento actual es diferente al nombre de la calle del elemento anterior
            else:
                # Deja las coordenadas del elemento anterior sin cambiar
                pass

    # Imprimir la lista en un archivo CSV
    with open("calles_culiacan.csv", "w", newline="", encoding="utf-8") as csv_file:
        # Creamos el objeto writer
        writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_ALL)
        # Escribimos los encabezados
        writer.writerow(["lat1", "lon1", "lat2", "lon2", "name"])
        # Escribimos los registros
        writer.writerows(street_corners)