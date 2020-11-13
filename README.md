# The Secret Tower

```
              o                             
                   O       /`-.__           You are at the top of the tower of a powerful Mage
                          /  \�'^|          He greets You and starts to talk:
             o           T    l  *
                        _|-..-|_            - So You are looking for some knowledge, Young Adventurer?
                 O    (^ '----' `)          - To my power obtain,
                       `\-....-/^               You have to face three great tasks.
             O       o  ) "/ " (              
                       _( (-)  )_           - Here's The Scroll with instructions. Good luck.
                   O  /\ )    (  /\         
                     /  \(    ) |  \
                 o  o    \)  ( /    \
                   /     |(  )|      \
                  /    o \ \( /       \
            __.--'   O    \_ /   .._   \
           //|)\      ,   (_)   /(((\^)'\
              |       | O         )  `  |
              |      / o___      /      /
             /  _.-''^^__O_^^''-._     /
           .'  /  -''^^    ^^''-  \--'^
         .'   .`.  `'''----'''^  .`. \
       .'    /   `'--..____..--'^   \ \
      /  _.-/                        \ \
  .::'_/^   |                        |  `.
         .-'|                        |    `-.
   _.--'`   \                        /       `-.
  /          \                      /           `-._
  `'---..__   `.                  .�_.._   __       \
           ``'''`.              .'      `'^  `''---'^
                  `-..______..-'
```

# The Scroll

```
                                             _______________________
   _______________________-------------------                       `\
 /:--__                                                              |
||< > |                                   ___________________________/
| \__/_________________-------------------                         |
|                                                                  |
 |                          THE SCROLL                              |
 |                                                                  |
 |      "Remember Young Adventurer, to inform me                    |
  |        about every task completion using Telepathy.              |
  |      First task is to meet The End. The Gryphon is the one,      |
  |        who knows exact location, ask his head.                   |
  |      Second task has to be brutal strenght demonstration          |
   |       You need to impress The Royal Paladin.                     |
   |     Third task.                                                  |
   |                                                                 |
  |                                              ____________________|_
  |  ___________________-------------------------                      `\
  |/`--_                                                                 |
  ||[ ]||                                            ___________________/
   \===/___________________--------------------------
```

* Learn some [Telepathy](/flag_server) first
  * Download client, register, use it to send flags and check Your score
* Task one - [The End](/task1)  
  * Find path to the easy challenge using some reconnaissance (Burp/Web Dev Tools) and by asking Gryphon
  * Solve easy SSTI challenge by finding a flag on the server - exploit SSTI to RCE (Remote Code Execution)
  * Solve medium SSTI challenge by finding a method to escape from sandbox and get access to the *FLAG* variable inside *_\_main__* module
  * You are up for the challenge? Find hard one - there is hidden one (inside SSTI vulnerability) inacessible from web
* Task two - [Strenght Demonstration](/task2)
  * EPILEPSY WARNING
  * Find a method to inject a command to the form
  * There are easter eggs ( ͡° ͜ʖ ͡°)
* Task three


# Setup
* local:
```sh
# https://docs.docker.com/compose/reference/up/
docker-compose up -d --build
```
* remote at:
  * http://167.172.107.163:5000
  * http://167.172.107.163:5001
  * http://167.172.107.163:5002

# Solutions
* [Solve scripts](/solve)