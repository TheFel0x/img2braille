from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input",type=str,help="image file")
parser.add_argument("-w","--width",type=int,help="output width in chars")
parser.add_argument("--noinvert",action='store_true',help="don't invert colors (for bright backrounds with dark text)")
parser.add_argument("-d","--dither",action='store_true',help="use dithering")
# TODO: add more calculation options
parser.add_argument("-c","--calculation",type=str,choices=["RGBsum","R","G","B","BW"],help="determines the way in which dot values are calculated")

args = parser.parse_args()

imgpath = args.input
new_width = args.width if not args.width == None else 200
inverted = not args.noinvert if not args.noinvert == None else True 
dither = args.dither if not args.dither == None else False
algorythm = args.calculation if not args.calculation == None else "RGBsum"

img = Image.open(imgpath)
img = img.resize((new_width,round((new_width*img.size[1])/img.size[0])))

off_x = (img.size[0]%2)
off_y = (img.size[1]%4)

if off_x + off_y > 0:
    img = img.resize((img.size[0]+off_x,img.size[1]+off_y))

if dither:
    if not algorythm == "RGBsum" or algorythm == "BW":
        if algorythm == "R":
            # adjust image to red values
            pass
        elif algorythm == "G":
            # adjust image to green values
            pass
        elif algorythm == "B":
            # adjust image to blue values
            pass
    img = img.convert("1")
    algorythm = "BW"

def get_dot_value(pos):
    if algorythm == "RGBsum":
        px = img.getpixel(pos)
        if px[0]+px[1]+px[2] < 382.5:
            return not inverted
        else:
            return inverted
    elif algorythm == "R":
        px = img.getpixel(pos)
        if px[0] < 127.5:
            return not inverted
        else:
            return inverted    
    elif algorythm == "G":
        px = img.getpixel(pos)
        if px[1] < 127.5:
            return not inverted
        else:
            return inverted
    elif algorythm == "B":
        px = img.getpixel(pos)
        if px[2] < 127.5:
            return not inverted
        else:
            return inverted
    elif algorythm == "BW":
        px = img.getpixel(pos)
        if px < 127.5:
            return not inverted
        else:
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
    return chr(block_val)

def iterate_image():
    y_size = img.size[1]
    x_size = img.size[0]
    y_pos = 0
    x_pos = 0
    line = ''
    while y_pos < y_size-3:
        x_pos = 0
        while x_pos < x_size:
            line = line + block_from_cursor((x_pos,y_pos))
            x_pos = x_pos + 2
        print(line)
        line = ''
        y_pos = y_pos + 4

iterate_image()
