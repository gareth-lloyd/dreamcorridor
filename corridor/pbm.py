def pbm_lines(filename):
    """Given the name of a ppm file, open the file and parse it
    into an array. There will be one member of the array for every
    line of pixels in the image, containing the bytes for that line.
    """
    with open(filename, 'rb') as f:
        file_lines = f.readlines()

    pixel_width, height = file_lines[1].split()
    pixel_width, height = int(pixel_width), int(height)

    img_data = file_lines[2]

    img_lines = []
    x = 0
    byte_width = pixel_width / 8
    if pixel_width % 8:
        byte_width += 1

    for row in range(height):
        img_lines.append(img_data[x:x+byte_width])
        x += byte_width

    return img_lines
