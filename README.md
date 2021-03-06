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
   |       You need to command The Rainbow Paladin.                   |
   |     Third task is to get a secret password from the              |
   |       Guard of the secret - common techniques should help You." |
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
* Task three - [Secret stealer](/task3)
  * Find a way to login to the portal
  * Find Common Vulnerability & Exposure for used framework
  * Get the flag from the password of *Guard of the secret*
  * Wanted to do here also one more task, but I did not make it on time :c


# Setup
* local:
```sh
# https://docs.docker.com/compose/reference/up/
docker-compose up -d --build
# Build without -d if You want to read logs from apps
```
* remote at:
  * http://167.172.107.163:5000
  * http://167.172.107.163:5001
  * http://167.172.107.163:5002/magic3

# Troubleshooting
  * docker-compose/docker build command says that pip returned non-zero code (137)
    * Clear memory or reboot machine - if that won't help then buy more RAM

# Solutions
* [Solve scripts](/solve) - will be available week or two after workshops, for now they are hidden