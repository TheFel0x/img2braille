

# Adjustment To Color Calculation
# Takes an image and returns a new image with the same size
# The new image only uses either the R, G or B values of the original image
def adjust_to_color(img, pos):
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            val = img.getpixel((x, y))[pos]
            img.putpixel((x, y), (val, val, val))
    return img

# Average Calculation
# Takes an image and returns the averade color value
def calc_average(img, algorythm, autocontrast):
    if autocontrast:
        average = 0
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if algorythm == "RGBsum":
                    average += img.getpixel((x, y))[0] + img.getpixel((x, y))[1] + img.getpixel((x, y))[2]
                elif algorythm == "R":
                    average = img.getpixel((x, y))[0]
                elif algorythm == "G":
                    average = img.getpixel((x, y))[1]
                elif algorythm == "B":
                    average = img.getpixel((x, y))[2]
                elif algorythm == "BW":
                    average = img.getpixel((x, y))
                else:
                    average += img.getpixel((x, y))[0] + img.getpixel((x, y))[1] + img.getpixel((x, y))[2]
        return average / (img.size[0] * img.size[1])
    else:
        return 382.5

# Returns boolean representing the color of a pixel
# Uses the average color value for this
# Average color value is
def get_dot_value(img, pos, average):
    px = img.getpixel(pos)
    if px[0] + px[1] + px[2] < average:
        return not args.invert
    return args.invert

# Returns block (braille symbol) at the current position
# Uses average to calculate the block
# noempty replaces empty blocks with 1-dot blocks
def block_from_cursor(img, pos, average, noempty, blank):
    if blank:
        return chr(0x28FF)
    block_val = 0x2800
    if get_dot_value(img, pos, average):
        block_val += 0x0001
    if get_dot_value(img, (pos[0] + 1, pos[1]), average):
        block_val += 0x0008
    if get_dot_value(img, (pos[0], pos[1] + 1), average):
        block_val += 0x0002
    if get_dot_value(img, (pos[0] + 1, pos[1] + 1), average):
        block_val += 0x0010
    if get_dot_value(img, (pos[0], pos[1] + 2), average):
        block_val += 0x0004
    if get_dot_value(img, (pos[0] + 1, pos[1] + 2), average):
        block_val += 0x0020
    if get_dot_value(img, (pos[0], pos[1] + 3), average):
        block_val += 0x0040
    if get_dot_value(img, (pos[0] + 1, pos[1] + 3), average):
        block_val += 0x0080
    if noempty and block_val == 0x2800:
        block_val = 0x2801
    return chr(block_val)

# Gets the average original color value at the current position
# output depends on the color style
def color_average_at_cursor(original_img, pos, colorstyle):
    px = original_img.getpixel(pos)
    if colorstyle == "ansi":
        return "\x1b[48;2;{};{};{}m".format(px[0], px[1], px[2])
    elif colorstyle == "ansifg":
        return "\x1b[38;2;{};{};{}m".format(px[0], px[1], px[2])
    elif colorstyle == "ansiall":
        return "\x1b[38;2;{};{};{};48;2;{};{};{}m".format(px[0], px[1], px[2], px[0], px[1], px[2])
    elif colorstyle == "html":
        return "<font color=\"#{:02x}{:02x}{:02x}\">".format(px[0], px[1], px[2])
    elif colorstyle == "htmlbg":
        return "<font style=\"background-color:#{:02x}{:02x}{:02x}\">".format(px[0], px[1], px[2])
    elif colorstyle == "htmlall":
        return "<font style=\"color:#{:02x}{:02x}{:02x};background-color:#{:02x}{:02x}{:02x}\">".format(px[0], px[1], px[2], px[0], px[1], px[2])
    else:
        return ""
