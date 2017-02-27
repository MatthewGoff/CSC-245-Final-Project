# ![avatar](assets/images/avatar.png) CSC-245 Final Project
Winter 17 class project

## Dev Notes
- Pycharm will claim that it can't find modules even if it runs. To resolve this
right click on src folder>"Mark Directory As">"Sources Root"

- Uncomment the import statement in main_game and then run it to see the battle demo.

## Todo
- Have beta version ready for March 6th

### World Editor
- Good enough, no more required
- [ ] Make it possibile to create different sized world (get click event from sprite) (matt)
    - Remove cam_width and cam_height attributes
- [x] Fix inability to edit while zoomed in/out (caleb? - talk with matt)
- [ ] Saving/loading during full screen crashes -> Create popup dialog
    - Create list of available worlds
- [x] Add support for foreground sprites to import/export functions

### Main Game
- [ ] Create menu to choose between editor and campaign
- [x] Make world zoomable (caleb, matt)

#### Campaign
- [ ] Create Demo (Matt, Josh)
    - [x] Display world
    - [ ] Display user
    - [ ] Move user
    - [ ] Restrict user movement
    - [ ] Enter battle demo
- [ ] Create animation (Monica)
- [x] Make fullscreen
- [ ] (Optional) Create FOW

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

### Other
- [ ] Make world able to load different sizes (update world.border) (matt)
- [x] Make camera center start at the center of the world (matt)
- [ ] Make executable (matt)