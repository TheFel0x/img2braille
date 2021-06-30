<!--
 TODO:
    - make this look nicer
-->
### how it works:
- divide image into 2x4 blocks
- calculate block value by adding [dot values](#dot-values) to `0x2800`
- create braille character by outputting block value as char (UTF-16)

![image](https://user-images.githubusercontent.com/43345523/124006740-e996bc80-d9da-11eb-8f17-a3f8c5b211f9.png)
![image](https://user-images.githubusercontent.com/43345523/124007049-45f9dc00-d9db-11eb-9c51-55caf23ec58c.png)


### dot-values:
|||
|--|--|
|+1|+8|
|+2|+16|
|+4|+32|
|+64|+128|
