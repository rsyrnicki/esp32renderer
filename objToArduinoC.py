import sys

def maxValueOnAxis(array2D, axis):
    output = 0.0
    for i in range(len(array2D)):
        i = max(i, float(array2D[i][axis]))
    return output

def minValueOnAxis(array2D, axis):
    output = 0.0
    for i in range(len(array2D)):
        i = min(i, float(array2D[i][axis]))
    return output

def maxIn2DArray(array2D):
    output = 0.0
    for i in range(len(array2D)):
        for j in range(len(array2D[0])):
            output = max(output, abs(float(array2D[i][j])))
    return output
    
def main():
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
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
        maxValue = maxIn2DArray(vertices)
        maxY = maxValueOnAxis(vertices, 1)
        minY = minValueOnAxis(vertices, 2)
        for i in range(len(vertices)):
            x = float(vertices[i][0]) / maxValue
            y = (float(vertices[i][1]) / maxValue) - minY
            z = float(vertices[i][2]) / maxValue
            file.write(f"   {{  {x}, {y}, {z} }}, \n")
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

