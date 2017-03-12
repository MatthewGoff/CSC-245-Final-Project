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
- Fullscreen in battle

## Todo

### World Editor
- [ ] (optional) Saving/loading during full screen crashes -> Create popup dialog
    - Create list of available worlds
- [ ] (optional) Make wold size editable in game
- [x] Place impassible tiles (with some visual indication)

#### Campaign
- [x] Create Demo (Matt, Josh)
    - [x] Restrict user movement
    - [x] Enter battle demo
- [x] Create animation (Monica)
- [ ] Add animation to campaign
- [ ] Make user inherit from party (Matt)
- [ ] Add levels
- [ ] (Optional) Create fog of war
- [ ] (Future) Inventory
- [ ] (Future) Tutorial
    - Make a state machine

#### Battle
- [x] Basic Demo (Caleb)
    - [x] Add abilities functionality
    - [x] Add non-arbitrary player placement
    - [x] Add more players to each team
    - [ ] Animations
        - [ ] Melee
        - [ ] Projectile
        - [ ] Effects? (death, non-offensive ability use, melee animations, collision anims)
    - [ ] Buffs?
- [ ] (Future) Option to flee
- [ ] Background image
- [ ] Add battle text 

### Other
- [ ] Make some instruction sheet
- [ ] Make executable (matt)
- [ ] Add a 'back' button
- [x] Add text input functionality
- [ ] (Optional) Add version number to menu
- [ ] (Optional) Add Credits
- [ ] (Optional) Drop down menu
- [ ] (Optional) Menu
- [ ] (Optional) Improve switching between screens

### Bugs

- [ ] Scrolling bug
- [ ] Walking "on" tables
- [ ] Exit when lose (add lose result)
