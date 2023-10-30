class Number:
    def __init__(self, value) -> None:
        self.value = value 
        self.set_position()
    

    def set_position(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start 
        self.pos_end = pos_end
        return self
    
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value), None
        
    def subbed_to(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value), None
        
    def divided_to(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value), None
        
    def multiplied_to(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value), None
    def __repr__(self) -> str:
        return str(self.value)