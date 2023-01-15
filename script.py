from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="image file")
parser.add_argument(
    "-w", "--width",
    type=int,
    default=200,
    help="determines output width in number of chars",
)
parser.add_argument(
    "-i", "--noinvert",
    dest='invert',
    action='store_false',
    help="don't invert colors (for bright backrounds with dark text)",
)
parser.add_argument(
    "-d", "--dither",
    action='store_true',
    help="use dithering (recommended)",
)
# TODO: rename "--calc" to "--filter"; choices: R, G, B, <none> ; description: "uses the specified channel. combines R, G and B channel if not specified. doesn't apply to images with 1 channel"
#   note: unsure how images should be handled that have 2 or more than 3 channels, unsure what to do with alpha channel
#   adjust related functions
parser.add_argument(
    "--calc",
    type=str,
    choices=["RGBsum", "R", "G", "B", "BW"],
    default='RGBsum',
    help="determines color values used for calculating dot values (on/off) are calculated",
)
parser.add_argument(
    "-n", "--noempty",
    action='store_true',
    help='don\'t use U+2800 "Braille pattern dots-0" (can fix spacing problems))',
)
parser.add_argument(
    "-c", "--color",
    type=str,
    choices=["none", "ansi", "ansifg", "ansiall", "html", "htmlbg", "htmlall"],
    default='none',
    help="adds color for html or ansi ascaped output",
)
parser.add_argument(
    "-a", "--autocontrast",
    action='store_true',
    help="automatically adjusts contrast for the image",
)
parser.add_argument(
    "-b", "--blank",
    action='store_true',
    help="U+28FF everywhere. If all you want is the color output",
)

# TODO: add "--algorithm" flag; support dithering algorithms: bayer matrix, floyd-steinberg, threshold, etc.
#   note: default should be threshold? maybe something nicer looking instead.


# Arg Parsing
args = parser.parse_args()

# Adjustment To Color Calculation
# Takes an image and returns a new image with the same size
# The new image only uses either the R, G or B values of the original image
def adjust_to_color(img, pos):
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            val = img.getpixel((x, y))[pos]
            img.putpixel((x, y), (val, val, val))
    return img

# Applies chosen color mode to the image
def apply_algo(img, algo):
    if algo == "RGBsum":
        img = img.convert("RGB")
    elif algo == "R":
        img = adjust_to_color(img, 0)
    elif algo == "G":
        img = adjust_to_color(img, 1)
    elif algo == "B":
        img = adjust_to_color(img, 2)
    elif algo == "BW":
        # TODO: check if this actually works with black/white images
        img = img.convert("RGB")
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

# Iterates over the image and does all the stuff
def iterate_image(img, original_img, dither, autocontrast, noempty, colorstyle, blank):
    img = apply_algo(img, args.calc)
    img = img.convert("RGB")
    average = calc_average(img, args.calc, autocontrast)
    if dither:
        img = img.convert("1")
    img = img.convert("RGB")

    y_size = img.size[1]
    x_size = img.size[0]
    y_pos = 0
    x_pos = 0
    line = ''
    while y_pos < y_size - 3:
        x_pos = 0
        while x_pos < x_size:
            line += color_average_at_cursor(original_img, (x_pos, y_pos), colorstyle)
            line += block_from_cursor(img, (x_pos, y_pos), average, noempty, blank)
            if colorstyle in {"html", "htmlbg"}:
                line += "</font>"

            x_pos += 2
        if colorstyle in {"ansi", "ansifg", "ansiall"}:
            line += "\x1b[0m"
        print(line)
        if colorstyle in {"html", "htmlbg", "htmlall"}:
            print("</br>")
        line = ''
        y_pos += 4

# Image Initialization
img = Image.open(args.input)
img = img.resize((args.width, round((args.width * img.size[1]) / img.size[0])))
off_x = img.size[0] % 2
off_y = img.size[1] % 4
if off_x + off_y > 0:
    img = img.resize((img.size[0] + off_x, img.size[1] + off_y))
original_img = img.copy()

# Get your output!
iterate_image(img, original_img, args.dither, args.autocontrast, args.noempty, args.color, args.blank)
