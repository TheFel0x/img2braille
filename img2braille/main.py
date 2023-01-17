from argparse import ArgumentParser, Namespace


def main() -> int:
    args = parse_args()
    # TODO


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
    # note: default should be threshold? maybe something nicer looking instead.

    return parser.parse_args()
