from PIL import Image

# TODO:
#   - take these as input from user
#
# v v v v v v v v v v v v v v v v v v
imgpath = 'test.png'
new_width = 200
inverted = True
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

img = Image.open(imgpath)
img = img.resize((new_width,round((new_width*img.size[1])/img.size[0])))

off_x = (img.size[0]%2)
off_y = (img.size[1]%4)

if off_x + off_y > 0:
    img = img.resize((img.size[0]+off_x,img.size[1]+off_y))

# TODO:
#   - add dithering?

def get_dot_value(pos):
    # TODO:
    #   - add more ways of getting dot value
    px = img.getpixel(pos)
    if px[0]+px[1]+px[2] < 382.5:
        return not inverted
    else:
        return inverted

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
