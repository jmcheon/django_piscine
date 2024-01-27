import sys


def ex07(filename):
    elements = []
    with open(filename, "r") as f:
        for line in f:
            name, properties = line.strip().split(" = ")
            properties = dict(prop.strip().split(":") for prop in properties.split(","))
            properties['name'] = name
            elements.append(properties)
    elements.sort(key=lambda e: int(e['position']))

    with open("./periodic_table.html", "w") as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<body>\n')
        f.write('<table>\n')

        row_elements = []
        for element in elements:
            if int(element['position']) == 0 and row_elements:
                f.write('<tr>\n')
                for e in row_elements:
                    f.write('<td style="border: 1px solid black; padding:10px">\n')
                    f.write(f'<h4>{e["name"]}</h4>\n')
                    f.write('<ul>\n')
                    f.write(f'<li>No {e["number"]}</li>\n')
                    f.write(f'<li>{e["small"]}</li>\n')
                    f.write(f'<li>{e["molar"]}</li>\n')
                    f.write(f'<li>{e["electron"]} electron(s)</li>\n')
                    f.write('</ul>\n')
                    f.write('</td>\n')
                f.write('</tr>\n')
                row_elements = []
            row_elements.append(element)


        f.write('</table>\n')
        f.write('</body>\n')
        f.write('</html>\n')


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ex07(sys.argv[1])
    else:
        print(f"Usage: python {sys.argv[0]} periodic_table.txt")
