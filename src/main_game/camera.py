# A camera class
# Author: Matthew Anderson
# Winter 2017

import pygame


class Camera:
    ZOOM_FACTOR = 0.9
    CAMERA_SPEED = 5

    def __init__(self, center, width, height, world):

        self.width = width
        self.height = height
        self.center = center
        self.world = world
        self.zoom = 1.0

        self.viewport = None
        self.update_viewport()

    def zoom_in(self):
        self.zoom *= Camera.ZOOM_FACTOR

    def zoom_out(self):
        self.zoom /= Camera.ZOOM_FACTOR

    def move_up(self):
        self.center = (self.center[0],
                       self.center[1]-Camera.CAMERA_SPEED*Camera.ZOOM_FACTOR)

    def move_down(self):
        self.center = (self.center[0],
                       self.center[1]+Camera.CAMERA_SPEED*Camera.ZOOM_FACTOR)

    def move_left(self):
        self.center = (self.center[0]-Camera.CAMERA_SPEED*Camera.ZOOM_FACTOR,
                       self.center[1])

    def move_right(self):
        self.center = (self.center[0]+Camera.CAMERA_SPEED*Camera.ZOOM_FACTOR,
                       self.center[1])

    # Moves the camera to follow the position of the center.
    # Clamps the camera to stay within the boundaries of the world.
    def update_viewport(self):
        width = int(self.width * self.zoom)
        height = int(self.height * self.zoom)

        self.viewport = pygame.Rect(self.center[0] - width/2,
                                    self.center[1] - height/2,
                                    width,
                                    height)
        #self.viewport.clamp_ip(self.world.get_border())

    # Draw the view of the camera into the given window at position x,y with dimension width, height.
    def draw(self, x, y, width, height, window):

        # Make sure the camera is focus on center.
        self.update_viewport()

        world_buffer = self.world.get_draw_buffer(self.viewport)
        # Extracts the view from the full world.
        view = pygame.Surface((self.viewport.width, self.viewport.height))
        view.blit(world_buffer, (-1*self.viewport.left,
                                 -1*self.viewport.top))

        # Scales view to the appropriate size.
        view = pygame.transform.smoothscale(view, (width, height))

        window.blit(view, (x, y))

    def get_location(self):
        return (self.viewport.x, self.viewport.y)
