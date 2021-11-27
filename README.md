[![CodeFactor](https://www.codefactor.io/repository/github/thefel0x/img2braille/badge/master)](https://www.codefactor.io/repository/github/thefel0x/img2braille/overview/master)
# img2braille
Turns an Image into Braille Art. (Unicode Art / "ASCII Art" (its not rly ascii...))
(now also with color!)

## Arguments
|flag|value|description|
|--|--|--|
| `input` | string (path) | path to image file |
| `-w` `--width` | integer | output width (characters) |
| `--noinvert` | - | deactivates inverted colors. for light backgrounds with dark text |
| `-d` `--dither` | - | activates dithering |
| `-c` `--calculation` | `RGBsum` `R` `G` `B` `BW` | determines the way in which is checked wether a dot is black or white |
| `--noempty` | - | don\'t use U+2800 "Braille pattern dots-0" |
| `--color` | `none` `ansi` `html` `htmlbg` `htmlall` | color support for either HTML style with font tags or ANSI escaped for cli use (html also puts br tags at the end of each line) htmlbg colors the background instead of the characters and all colors both |

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
- divide image into 2x4 blocks
- calculate block value by adding [dot values](#Dot-values) to `0x2800`
- create braille character by outputting block value as char (UTF-16)

### Dot-values:
|||
|--|--|
|+1|+8|
|+2|+16|
|+4|+32|
|+64|+128|

For calculating which braille symbol represents a 2x4 pixel block.

## TODO:
- differentiate between ansi, ansibg and ansiall in color settings
