<!--
 TODO:
    - make this look nicer
-->
### how it works:
- divide image into 2x4 blocks
- calculate block value by adding [dot values](#dot-values) to `0x2800`
- create braille character by outputting block value as char (UTF-16)

![image](https://user-images.githubusercontent.com/43345523/124007603-cd474f80-d9db-11eb-9254-9a21392d2b99.png)

### dot-values:
|||
|--|--|
|+1|+8|
|+2|+16|
|+4|+32|
|+64|+128|
