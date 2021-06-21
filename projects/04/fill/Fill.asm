// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// a variable for declaring which address is the end of screen pixels
@KBD
D=A

@ENDSCREEN
M=D-1

@SCREEN
D=A

@pixel // current pixel (address)
M=D

(START)
// check if key is pressed
@KBD
D=M
@BLACK
D;JGT

// else
@WHITE
0;JEQ

(WHITE)
// checking if the screen is already white
@SCREEN
D=A-1

@pixel
D=M-D

@START
D;JEQ

// else
@pixel
A=M
D=A
M=0

@pixel
M=M-1

// checking if we reached the start of the screen
@SCREEN
D=D-A
@START
D;JEQ

// else
@WHITE
0;JEQ

(BLACK)
@pixel
A=M
M=-1

// checking if we reached the end
@ENDSCREEN
D=M

@pixel
D=D-M

@START
D;JEQ

// else
@pixel
M=M+1

@BLACK
0;JMP

