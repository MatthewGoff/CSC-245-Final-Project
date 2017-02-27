# A camera class
# Author: Matthew Anderson
# Winter 2017

import pygame


class Camera:

    def __init__(self, center, width, height, world):

        # The dimensions of the camera
        self.width = width
        self.height = height

        # The center the camera is following
        self.center = center

        # How far the camera is offset from the position of the center.
        self.x_offset = 0.5 * width
        self.y_offset = 0.5 * height

        # The world the camera is viewing.
        self.world = world

        # Moves the camera to follow the position of the center.
        self.update_viewport()

    # Moves the camera to follow the position of the center.
    # Clamps the camera to stay within the boundaries of the world.
    def update_viewport(self):

        self.viewport = pygame.Rect(self.center[0] - self.x_offset, self.center[1] - self.y_offset,
                                    self.width, self.height)
        #self.viewport.clamp_ip(self.world.get_border())

    # Draw the view of the camera into the given window at position x,y with dimension width, height.
    def draw(self, x,y, width, height, window):

        # Make sure the camera is focus on center.
        self.update_viewport()
        # Have the world draw what the viewport can see.  This processes the whole world, but
        # only draw what the camera could actually see.  (This is called clipping.)
        world_buffer = self.world.get_draw_buffer(self.viewport)
        # Extracts the view from the full world.
        view = pygame.Surface((self.width, self.height))
        view.blit(world_buffer, (-1*self.viewport.left,
                                 -1*self.viewport.top))
        # Scales view to the appropriate size.
        view = pygame.transform.smoothscale(view,(width,height))
        # Display the resulting view to the visible window.
        window.blit(view,(x,y))

    def get_location(self):
        return (self.viewport.x, self.viewport.y)
