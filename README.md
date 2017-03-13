# ![avatar](assets/icon/icon.png) CSC-245 Final Project
Winter 17 class project

## Sources
- Buttons: https://pythonprogramming.net/pygame-python-3-part-1-intro/
- Avatars: http://www.chimakier.com/games/chimaki/avata/
- Tiles:
- 2gei Free Game Tiled, 60 different kinds of tiled: http://www.2gei.com/view/4149.html?order=name&page=4
- RPG Maker VX Ace Tiled: http://www.rpgmakerweb.com/

## Dev Notes
- Pycharm will claim that it can't find modules even if it runs. To resolve this
right click on src folder>"Mark Directory As">"Sources Root"
- Change prompt in campaign from campaign_start to input_example w/ same parameters to see an example of text input

### Known bugs
- Can't slide on walls when pressing two direction keys
- Fullscreen

## Todo

### World Editor
- [ ] (optional) Saving/loading during full screen crashes -> Create popup dialog
    - Create list of available worlds
- [ ] (optional) Make world size editable in game
- [x] Place impassible tiles (with some visual indication)

#### Campaign
- [ ] Add enemies and boss to final 3 worlds
- [ ] (Optional) Make winning a battle increase ability strength
- [ ] Fix fullscreen in switch between campaign/battle and back
- [x] Create Demo (Matt, Josh)
    - [x] Restrict user movement
    - [x] Enter battle demo
- [x] Create animation (Monica)
- [x] Add animation to campaign
- [x] Make user inherit from party (Matt)
- [x] Add levels
- [ ] (Optional) Create fog of war
- [ ] (Cancelled) Inventory
- [ ] (Future) Tutorial
    - Make a state machine

#### Battle
- [ ] Script boss
- [x] Basic Demo (Caleb)
    - [x] Add abilities functionality
    - [x] Add non-arbitrary player placement
    - [x] Add more players to each team
    - [ ] (Cancelled) Animations
        - [ ] Melee
        - [ ] Projectile
        - [ ] Effects? (death, non-offensive ability use, melee animations, collision anims)
    - [x] Ability buff/debuff functionality
- [ ] (Optional) Option to flee
- Background images
    - [x] olin 107
    - [x] olin hallway
    - [ ] olin lobby
    - [ ] nott approach
    - [ ] nott interior
- [x] Add battle text - make the tutorial message only appear once

### Other
- [ ] Make some instruction sheet
- [ ] Make executable (matt)
- [x] Add a 'back' button - still need this for editor
- [x] Add text input functionality
- [x] (Optional) Add version number to menu
- [ ] (Extremely Important) Add Credits
- [ ] (Optional) Drop down menu
- [ ] (Optional) Menu
- [ ] (Optional) Improve switching between screens

### Bugs

- [x] Scrolling bug
- [x] Walking "on" tables
- [x] Exit when lose (add lose result)
- [ ] Fullscreen
