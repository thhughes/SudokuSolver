class Node():
    def __init__(self, value):
        self._value = value
        self._all = [1,2,3,4,5,6,7,8,9]
        if value is not None:
            self._p = self._all
            self._p.remove(value)
            self._np = [value]
        else:
            self._p = []
            self._np = []
            
    def __str__(self):      return self.string()
    def __repr__(self):     return self.string()
    def __eq__(self,other): return self._value == other
    def __hash__(self):     return hash(self._value)^13
    def val(self):          return self._value
    
    def string(self):
        if self._value == None:
            return "_"
        else:
            return str(self._value)
    
    def set_p(self,possible):
        self._p = possible
        self._np = []
        for v in self._all:
            if v not in self._p:
                self._np.append(v)
        self._p = sorted(self._p)
        self._np = sorted(self._np)

    def set_np(self,not_possible):
        self._np = not_possible
        self._p = []
        for v in self._all:
            if v not in self_np:
                self._p.append(v)
        self._p = sorted(self._p)
        self._np = sorted(self._np)
                
    def add_p(self, value):
        if value in self._p: raise RuntimeError("Value already in possible list")
        elif value not in self._np: raise RuntimeError("Only values that are Not Possible can become psosible")
        else:
            self._p.append(value)
            self._np.remove(value)
            self._p = sorted(self._p)
            self._np = sorted(self._np)

    def remove_p(self,value):
        if value not in self._p: raise RuntimeError("Value cannot be removed, is not originally in list")
        elif value in self._np: raise RuntimeError("Value duplicated in _p and _np of Node class")
        else:
            self._p.remove(value)
            self._np.append(value)
            self._p = sorted(self._p)
            self._np = sorted(self._np)
        
    def get_possible(self):
        """ Returns empty list when the value's been set to simplify logic for
            knowing 'how many items are possible' for other nodes"""
        if self._value is not None:
            return []
        else:
            return self._p
    def get_notp(self):
        """ If the 'value' has been set, return all but that value """
        if self._value is not None:
            return self_all.remove(self._value)
        else:
            return self._np
    

