welcome to python-fps, A python fps written in python3
Thanks for viewing this fps example. It's coded using the python scripting language version 3.6.5 by kianoosh shakeri.
*feel free to use this fps thing to make your games with much less effert. Hopefully this brings more bgt loving people to python.
This fps thing features an awesome translator which works exactly how you want. All you need is the poedit software to compile .po files and put them in the required directory to get your translation up and running. Please take a look at the locale folder to have a better understanding of how this translation system works. If you want to translate the game in your language, Read the persian translater file which is located in locale/fa/LC_MESSAGES and is named fa.po. msgid is the actual sentence, word or better say "string" to be translated, and msgstr is the translation string. With my very very very little knowledge of spanish, an example would be this:
msgid "hello"
msgstr "hola"
This translates the word hello to the word hola.
It was all I could say about the translator. This thing also features a bunch of useful functions for fps movements and rotation, along a fiew modules that might be needed in an fps game such as the random ambience player(randomambience.py), doors(doors.py), consoles(console.py), map parsing along with the stuff that might be in the map(map.py). Rotation formulas and movement formulas(movement.py).
Globals.py. What the heck is this? Simple: Global variables. Everything that might be needed in more than a module such as the variable "currentroom" and "roomsound" to handle roomsound and roomsound changes, Or walktimer which is the timer that is used to move the player in each fiew mili seconds, menu which holds a value of true or false(yuup you guessed it! boolian) to recognize if a menu is opened or not, menulist which holds a list of elements for the current menu and other variables which you can take a look at in the globals.py file.
Finally, fps.py. It's the heart of the game. The game runs within this file, Key handlings are in this file and the things that should be looped is also in this file. Take a look at it!
Oh my, I forgot about the logger. It logs what ever you like just like in bgt. Although I didn't made the game log the errors, Instead it usually speaks the errors. You can change it yourself if you like.

required modules:
pyglet
Note. Please copy and paste the pyglet folder that is in this folder to your python directory/lib/site-packages. Make sure you have pyglet installed before doing this. It removes the exiting with the escape key. By default, It exits the program whenever, whereever(in the program) you press escape.
pyopenal
wxpython
Accessible output
Get the Accessible Output library from carter temm's mirror of code formally available on hg.q-continuum.net on github:
https://github.com/cartertemm/continuum-repositories

keys
w, a, s, d, walk
up, down, move in the menus
enter, activate a menu item, interact with objects.
n, navigation menu
p, Tells you the angle to turn to the right to face a point on 2 1 0. I just did it for you to get an insperation of how this system works.
holding q or e, Turn left or right constantly
holding alt, then pressing q or e, turning left or right by 45 degrees.
escape, Exit the menus, return to the main menu.

last but not least, credits
Thanks to Aprone for his movement codes. He shared them with us on audio games forum a very while ago
Thanks to sam tupy for his rotation package. Although i just took a formula from it and it was the calculate_x_y_angle which is function calculate_angle here. I changed it to work correctly with this system though.
Thanks to mason armstrong and carter temm for the AGK3 module. I changed the name to AGK for my own easier writing and stuff like that. I think it also includes a soundpool which is my work but it's buggy i think.
Honestly a fiew months ago a fiew guys were working on porting sam's rotation package to python and make it work with openal's coordinating system. One or a fiew functions are also taken from that module. I'm sure one of them was colton hill. BTW Those functions that I copied was turnleft and turnright and get_distance which I think I modifyed a fiew of them to work correctly. Thank you guys that were working on porting that rotation package!
Others are my own work. At least i can't remember anything else that must be written here.

Please note. I haven't provided any sounds with it. You have to add them yourself.
Please note again. This game is still under development. Check my git hub if  You like this thing!
I hope you like this thing and More than that, I hope this could be a great help for you to start learning python. Or if you already know it, I hope this could improve your python skills. I hope this could be a help after all!
