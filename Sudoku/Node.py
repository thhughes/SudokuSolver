class Node():
    """
    This class is a class that feeds the Sudoku class (in the Sudoku.py file).

    This class is a data structure for managing what nodes have ben tried in
    specific places.
    """
    def __init__(self, value, usedList = None, maxSize = 9, minSize = 1):
        self._maxSize = maxSize
        self._minSize = minSize
        self._usedVals = []
        self._value = None
        self.setVal(value)

        if not (usedList is None):
            for v in usedList:
                if not(v in self._usedVals):
                    self._usedVals.append(v)





            
    def __str__(self):          return self.string()
    def __repr__(self):         return self.string()
    def __eq__(self,other):     return self._value == other ## Overloads the == operator
    def __hash__(self):         return hash(self._value)^13
    def __call__(self):         return self._value
    def maxSize(self):          return self._maxSize
    def minSize(self):          return self._minSize
    def usedVals(self):         return self._usedVals
    def hasUsed(self, value):   return value in self._usedVals
    def setMax(self, max):      self._maxSize = max
    def setMin(self,min):       self._minSize = min



    def setVal(self, value):
        if value is None: self._value = None
        elif not self._inBounds(value): pass ## _inBounds function will raise exception
        elif value in self._usedVals:
            print "ERROR: \t\t Value, _usedVals", value, self._usedVals
            raise NodeException("Value has already been tried")
        else:
            self._value = value
            self._usedVals.append(value)

    def _inBounds(self, value):
        if value > self._maxSize : raise NodeException("Value is greater than maxSize")
        elif value < self._minSize : raise NodeException("Value is less than minSize")
        else: return True

    def addConstraint(self, value):
        """
        Adds a constraint to a node, this means that the node cannot be set to
        the value passed if it returns True
        :param value: <int>
        :return: Boolean True : if everything returns well.
        :raise: NodeException : if the value is out of bounds
        """
        if not self._inBounds(value): pass
        self._usedVals.append(value)
        return True

    def string(self, displayName = False):
        """ Mainly for printing
        displayName :: Used for debugging purposes"""
        start = ""
        body = ""
        end = ""
        if displayName: start = " N(";end   = ")"
        if self._value == None: body = "_"
        else: body = str(self._value)

        return start + body + end


    
class NodeException(Exception):
    """ NODE Exception Class """
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)



