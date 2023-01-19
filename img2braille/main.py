from argparse import ArgumentParser, Namespace

from PIL.Image import open as img_open


def main() -> int:
    args = parse_args()

    # TODO: simplify and split

    img = img_open(args.input)
    img = img.resize((args.width, round((args.width * img.size[1]) / img.size[0])))
    off_x = img.size[0] % 2
    off_y = img.size[1] % 4
    if off_x + off_y > 0:
        img = img.resize((img.size[0] + off_x, img.size[1] + off_y))
    original_img = img.copy()

    img = apply_algo(img, args.calc)
    img = img.convert("RGB")
    average = calc_average(img, args.calc, args.autocontrast)
    if args.dither:
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
            line += color_average_at_cursor(original_img, (x_pos, y_pos), args.color)
            line += block_from_cursor(img, (x_pos, y_pos), average, args.noempty, args.blank)
            if args.color in {"html", "htmlbg"}:
                line += "</font>"

            x_pos += 2
        if args.color in {"ansi", "ansifg", "ansiall"}:
            line += "\x1b[0m"
        print(line)
        if args.color in {"html", "htmlbg", "htmlall"}:
            print("</br>")
        line = ''
        y_pos += 4

    return 0


def parse_args() -> Namespace:
    parser = ArgumentParser('img2braille')

    parser.add_argument(
        "input",
        type=str,
        help="image file"
    )
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

    return parser.parse_args()
