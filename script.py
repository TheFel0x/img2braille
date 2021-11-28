from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,help="image file")
parser.add_argument("-w","--width",type=int,help="determines output width in number of chars")
parser.add_argument("--noinvert",action='store_true',help="don't invert colors (for bright backrounds with dark text)")
parser.add_argument("-d","--dither",action='store_true',help="use dithering (recommended)")
# TODO: add more calculation options
parser.add_argument("-c","--calculation",type=str,choices=["RGBsum","R","G","B","BW"],help="determines the way in which dot values (on/off) are calculated")
parser.add_argument("--noempty",action='store_true',help='don\'t use U+2800 "Braille pattern dots-0" (can fix spacing problems))')
parser.add_argument("--color",type=str,choices=["none","ansi","ansifg","ansiall","html", "htmlbg", "htmlall"],help="adds color for html or ansi ascaped output")

args = parser.parse_args()
imgpath = args.input
new_width = args.width if args.width is not None else 200
inverted = not args.noinvert if args.noinvert is not None else True 
dither = args.dither if args.dither is not None else False
algorythm = args.calculation if args.calculation is not None else "RGBsum"
noempty = args.noempty if args.noempty is not None else False
colorstyle = args.color if args.color is not None else "none"

img = Image.open(imgpath)
img = img.resize((new_width,round((new_width*img.size[1])/img.size[0])))

off_x = (img.size[0]%2)
off_y = (img.size[1]%4)

if off_x + off_y > 0:
    img = img.resize((img.size[0]+off_x,img.size[1]+off_y))

original_img = img.copy()

def adjust_to_color(img, pos):
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            val = img.getpixel((x,y))[pos]
            img.putpixel((x,y),(val,val,val))
    return img

if dither:
    if algorythm != "RGBsum" or algorythm == "BW":
        if algorythm == "R":
            img = adjust_to_color(img,0)
        elif algorythm == "G":
            img = adjust_to_color(img,1)
        elif algorythm == "B":
            img = adjust_to_color(img,2)
    img = img.convert("1")
    algorythm = "BW"

def get_dot_value(pos):
    if algorythm == "RGBsum":
        px = img.getpixel(pos)
        if px[0]+px[1]+px[2] < 382.5:
            return not inverted
        return inverted
    elif algorythm == "R":
        px = img.getpixel(pos)
        if px[0] < 127.5:
            return not inverted  
        return inverted    
    elif algorythm == "G":
        px = img.getpixel(pos)
        if px[1] < 127.5:
            return not inverted
        return inverted
    elif algorythm == "B":
        px = img.getpixel(pos)
        if px[2] < 127.5:
            return not inverted
        return inverted
    elif algorythm == "BW":
        px = img.getpixel(pos)
        if px < 127.5:
            return not inverted
        return inverted   
    else:
        # TODO: add more ways of getting dot value
        pass

def block_from_cursor(pos):
    block_val = 0x2800
    if get_dot_value(pos):
        block_val = block_val + 0x0001
    if get_dot_value((pos[0]+1,pos[1])):
        block_val = block_val + 0x0008
    if get_dot_value((pos[0],pos[1]+1)):
        block_val = block_val + 0x0002
    if get_dot_value((pos[0]+1,pos[1]+1)):
        block_val = block_val + 0x0010
    if get_dot_value((pos[0],pos[1]+2)):
        block_val = block_val + 0x0004
    if get_dot_value((pos[0]+1,pos[1]+2)):
        block_val = block_val + 0x0020
    if get_dot_value((pos[0],pos[1]+3)):
        block_val = block_val + 0x0040
    if get_dot_value((pos[0]+1,pos[1]+3)):
        block_val = block_val + 0x0080
    if noempty and block_val == 0x2800:
        block_val = 0x2801
    return chr(block_val)

def color_average_at_cursor(pos):
    px = original_img.getpixel(pos)
    if colorstyle == "ansi":
        return "\x1b[48;2;{};{};{}m".format(px[0],px[1],px[2])
    elif colorstyle == "ansifg":
        return "\x1b[38;2;{};{};{}m".format(px[0],px[1],px[2])
    elif colorstyle == "ansiall":
        return "\x1b[38;2;{};{};{};48;2;{};{};{}m".format(px[0],px[1],px[2],px[0],px[1],px[2])
    elif colorstyle == "html":
        return "<font color=\"#{:02x}{:02x}{:02x}\">".format(px[0],px[1],px[2])
    elif colorstyle == "htmlbg":
        return "<font style=\"background-color:#{:02x}{:02x}{:02x}\">".format(px[0],px[1],px[2])
    elif colorstyle == "htmlall":
        return "<font style=\"color:#{:02x}{:02x}{:02x};background-color:#{:02x}{:02x}{:02x}\">".format(px[0],px[1],px[2],px[0],px[1],px[2])
    else:
        return ""

def iterate_image():
    y_size = img.size[1]
    x_size = img.size[0]
    y_pos = 0
    x_pos = 0
    line = ''
    while y_pos < y_size-3:
        x_pos = 0
        while x_pos < x_size:
            

            line = line + color_average_at_cursor((x_pos,y_pos))
            line = line + block_from_cursor((x_pos,y_pos))
            if colorstyle == "html" or colorstyle == "htmlbg":
                line = line + "</font>"

            x_pos = x_pos + 2
        if colorstyle == "ansi" or colorstyle == "ansifg" or colorstyle == "ansiall":
            line = line + "\x1b[0m"
        print(line)
        if colorstyle == "html" or colorstyle == "htmlbg" or colorstyle == "htmlall":
            print("</br>")
        line = ''
        y_pos = y_pos + 4

iterate_image()
