class Node():
    def __init__(self, value, maxSize = 9, minSize = 1):
        self._maxSize = maxSize
        self._minSize = minSize
        self._value = None
        self._usedVals = []
        self.setVal(value)



            
    def __str__(self):      return self.string()
    def __repr__(self):     return self.string()
    def __eq__(self,other): return self._value == other ## Overloads the == operator
    def __hash__(self):     return hash(self._value)^13
    def __call__(self):     return self._value
    def maxSize(self):      return self._maxSize
    def minSize(self):      return self._minSize

    def setMax(self, max):
        self._maxSize = max

    def setMin(self,min):
        self._minSize = min

    def setVal(self, value):
        if value is None: self._value = None
        elif value > self._maxSize : raise NodeException("Value is greater than maxSize")
        elif value < self._minSize : raise NodeException("Value ie less than minSize")
        elif value in self._usedVals:raise NodeException("Value has already been tried")
        else:
            self._value = value
            self._usedVals.append(value)


    def string(self):
        """ Mainly for printing"""
        if self._value == None:
            return "_"
        else:
            return str(self._value)


    
class NodeException(Exception):
    """ NODE Exception Class """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)



