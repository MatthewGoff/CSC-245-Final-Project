# ![avatar](assets/icon/icon.png) CSC-245 Final Project
Winter 17 class project

## Sources
- Buttons: https://pythonprogramming.net/pygame-python-3-part-1-intro/www.2get.com 2gei Free Game Tiled
- 60 different kinds of tiled
- http://www.2gei.com/view/4149.html?order=name&page=4
- RPG Maker VX Ace Tiled

## Dev Notes
- Pycharm will claim that it can't find modules even if it runs. To resolve this
right click on src folder>"Mark Directory As">"Sources Root"
- Uncomment the import statement in main_game and then run it to see the battle demo.

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
- [ ] Create animation (Monica)
- [ ] Make user inherit from party (Matt)
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

### Other
- [ ] Make some instruction sheet
- [ ] Make executable (matt)
- [ ] (Optional) Add version number to menu
- [ ] (Optional) Add Credits
- [ ] (Optional) Drop down menu
- [ ] (Optional) Menu
- [ ] (Optional) Improve switching between screens