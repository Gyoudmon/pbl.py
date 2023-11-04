from ..iscreen import *

###############################################################
class OnionSkin(IScreen):
    def __init__(self, display):
        self.__display = display

    def display(self):
        return self.__display

    def get_extent(self):
        return self.__display.get_extent()
    
    def get_client_extent(self):
        return self.__display.get_client_extent()
    
    def frame_rate(self):
        return self.__display.frame_rate()
        
    def refresh(self):
        self.__display.refresh()

    def begin_update_sequence(self):
        self.__display.begin_update_sequence()

    def is_in_update_sequence(self):
        return self.__display.is_in_update_sequence()

    def end_update_sequence(self):
        self.__display.end_update_sequence()

    def should_update(self):
        return self.__display.should_update()
    
    def notify_updated(self):
        return self.__display.notify_updated()
