# A camera class
# Author: Matthew Anderson, Matthew Goff
# Winter 2017

import pygame


class Camera:
    ZOOM_FACTOR = 0.9

    def __init__(self, width, height, world):

        self.width = width
        self.height = height
        self.world = world
        self.zoom = 1.0

        self.viewport = None

    def set_zoom(self, zoom):
        self.zoom = zoom

    def zoom_in(self):
        self.zoom *= Camera.ZOOM_FACTOR

    def zoom_out(self):
        self.zoom /= Camera.ZOOM_FACTOR

    def update_viewport(self):
        pass

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
        return self.viewport.x, self.viewport.y

    def get_click_location(self, click_loc):
        """
        Take a click position on the camera view and translate it to a click
        position on the world
        :param click_loc:
        :return:
        """

        return (click_loc[0]*self.zoom+self.viewport.left,
                click_loc[1]*self.zoom+self.viewport.top)

"""
A Camera which always follows a party
"""
class BoundCamera(Camera):

    def __init__(self, party, width, height, world):
        Camera.__init__(self, width, height, world)
        self.party = party

    # Moves the camera to follow the position of the center.
    # Clamps the camera to stay within the boundaries of the world.
    def update_viewport(self):
        width = int(self.width * self.zoom)
        height = int(self.height * self.zoom)

        self.viewport = pygame.Rect(self.party.position.x - width/2,
                                    self.party.position.y - height/2,
                                    width,
                                    height)
        self.viewport.clamp_ip(self.world.get_border())


"""
A Camera which goes wherever
"""
class UnboundCamera(Camera):

    def __init__(self, center, width, height, world):

        Camera.__init__(self, width, height, world)
        self.center = center


    # Moves the camera to follow the position of the center.
    # Clamps the camera to stay within the boundaries of the world.
    def update_viewport(self):
        width = int(self.width * self.zoom)
        height = int(self.height * self.zoom)

        self.viewport = pygame.Rect(self.center[0] - width/2,
                                    self.center[1] - height/2,
                                    width,
                                    height)
