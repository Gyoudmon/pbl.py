import pygame

###############################################################################
def get_current_mouse_location():
    # The docs says the result is relative to the screen
    # But it actually seems to relative to the focused window
    return pygame.mouse.get_pos()
