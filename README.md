[![CodeFactor](https://www.codefactor.io/repository/github/thefel0x/img2braille/badge/main)](https://www.codefactor.io/repository/github/thefel0x/img2braille/overview/main)
# img2braille
Turns an Image into Braille Art with [Pillow](https://python-pillow.org/). (...or Unicode Art ...or "ASCII Art" (its not rly ascii))

Supports color now!

## Installation
First make sure that you have [Python 3](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed.
In the terminal:
```bash
git clone https://github.com/TheFel0x/img2braille
cd img2braille
python -m pip install -r requirements.txt
```
Then to run the script:
```bash
python script.py --help
```

## Arguments
|flag|value|description|
|--|--|--|
| `input` | string (path) | path to image file |
| `-w` `--width` | integer | output width (characters) |
| `-i` `--noinvert` | - | deactivates inverted dots. for light backgrounds with dark text |
| `-d` `--dither` | - | activates dithering |
| `--calc` | `RGBsum` `R` `G` `B` `BW` | determines the way in which is checked wether a dot is black or white |
| `-n` `--noempty` | - | don\'t use U+2800 "Braille pattern dots-0" (some applications remove these symbols because they treat them as spaces) |
| `-c` `--color` | `none` `ansi` `ansifg` `ansiall` `html` `htmlbg` `htmlall` | color support for either HTML style with font tags or ANSI escaped for cli use (html also puts br tags at the end of each line) htmlbg colors the background instead of the characters and all colors both |
| `-a` `--autocontrast` | - | enables autocontrast, to automatically adjust black and white values for calculations to the images max/min (recommended for black/white use) |
| `-b` `--blank` | - | all braille blocks are "full" blocks, in case you only care about the color output and not about the braille pattern | 

## Examples
`python script.py 'lain.png' --color ansi --dither --noempty`
![image](https://user-images.githubusercontent.com/43345523/143688036-d10ab9b1-4b15-46ac-8796-b80644034d43.png)

`python script.py 'lain.png' --dither`
![dither-braille](https://user-images.githubusercontent.com/43345523/124508661-af5d5e80-ddd0-11eb-82cc-256bace864df.png)

`python script.py 'lain.png'`
![default-braille](https://user-images.githubusercontent.com/43345523/124508597-8fc63600-ddd0-11eb-93d9-3ede4d521f3b.png)

`python script.py 'lain.png' --noinvert`
![noinvert-braille](https://user-images.githubusercontent.com/43345523/124508619-9b196180-ddd0-11eb-9def-b906a5e534c4.png)

## How it works:
- divide image into 2x4 pixel blocks
- calculate the blocks value by adding the [dot values](#Dot-values) to `0x2800`
- create braille character by outputting the final block value as a char (UTF-16 encoded)

### Dot-values:
<table>
  <tr>
    <td> +1 </td>
    <td> +8 </td>
  </tr>
  <tr>
    <td> +2 </td>
    <td> +16 </td>
  </tr>
  <tr>
    <td> +4 </td>
    <td> +32 </td>
  </tr>
  <tr>
    <td> +64 </td>
    <td> +128 </td>
  </tr>
</table> 

For calculating which braille symbol represents a 2x4 pixel block. The braille symbol works similar to an 8-bit binary number.

## How do I save output?
Using the `>` operator, like this:
`python script.py 'lain.png' > output.txt`

## TODO:
- support for different dithering algorithms
- fix any bugs
- support 3,4 and 8 bit ANSI color mode
- check if support for `U+1FB00` to `U+1FB3B` (Block Sextant) might be possible
- maybe edge detection filter?
- maybe IRC color option?
- color palette support? maybe using https://github.com/hbldh/hitherdither ?
- adjust-aspect-ratio option (for non-monospace fonts that mess up the aspect ration of the output)
