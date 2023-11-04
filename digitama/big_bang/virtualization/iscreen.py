from abc import *       # Abstract Base Class

from .display import IDisplay

###############################################################
class IScreen(ABC):
    @abstractmethod
    def display(self) -> IDisplay: pass
    
    @abstractmethod
    def get_extent(self): pass

    @abstractmethod
    def get_client_extent(self): pass

    @abstractmethod
    def frame_rate(self): pass

    @abstractmethod
    def refresh(self): pass

    @abstractmethod
    def begin_update_sequence(self): pass
    
    @abstractmethod
    def is_in_update_sequence(self): pass

    @abstractmethod
    def end_update_sequence(self): pass
    
    @abstractmethod
    def should_update(self): pass

    @abstractmethod
    def notify_updated(self): pass
