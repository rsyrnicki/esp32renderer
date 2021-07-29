import sys

def main():
    if len(sys.argv) > 0:
        fileName = sys.argv[0]
    else:
        print("Specify a filename (without .obj)")
        return
    with open(f"{fileName}.obj") as file_in:
        vertices = []
        faces = []
        normals = []
        normalsToFaces = []
        for line in file_in:
            if line[0] == '#':
                continue
            elif line[0] == 'f':
                v1 = line.split()[1]
                v2 = line.split()[2]
                v3 = line.split()[3]
                face = [v1.split("/")[0], v2.split("/")[0], v3.split("/")[0]]
                faces.append(face)
                normalsToFaces.append(v1.split("/")[2])
            elif line[0] == 'v':
                if line[1] == 't':
                    continue
                elif line[1] == 'n':
                    l = line.split()
                    normals.append([l[1], l[2], l[3]])
                else:
                    l = line.split()
                    vertices.append([l[1], l[2], l[3]])

        # Write to a .ino file
        file = open("esp32renderer.ino","w")
        file.write(f"const int numberVertices = {len(vertices)}; \n")
        file.write(f"const int numberFaces = {len(faces)}; \n")
        file.write(f"const int numberNormals = {len(normals)}; \n")

        file.write(f"float vertices[{len(vertices)}][3] = {{ \n")
        for i in range(len(vertices)):
            file.write(f"  {{ {vertices[i][0]}, {vertices[i][1]}, {vertices[i][2]} }}, \n")
        file.write("}; \n")

        file.write(f"float rawNormals[{len(normals)}][3] = {{ \n")
        for i in range(len(normals)):
            file.write(f"  {{ {normals[i][0]}, {normals[i][1]}, {normals[i][2]} }}, \n")
        file.write("}; \n")
        file.write(f"float normals[{len(normals)}][3]; \n")

        file.write(f"int normalsToFaces[{len(faces)}] = {{ ")
        for i in range(len(normalsToFaces)):
            file.write(f"  {normalsToFaces[i]}, ")
        file.write("}; \n")

        file.write(f"int faces[{len(faces)}][3] = {{ \n")
        for i in range(len(faces)):
            file.write(f"  {{ {faces[i][0]}, {faces[i][1]}, {faces[i][2]} }}, \n")
        file.write("}; \n")
        file.write(f"int vertices2D[{len(vertices)}][2]; \n")


if __name__ == '__main__':
    main()
