from bin import operation
from helper import load
import numpy as np

class labCustom(operation.operations):
    def __init__(self):
        super().__init__()
        
    def opt_myCustomFunc1(self, A:load.single_line, B:load.single_line) -> tuple[np.ndarray,np.ndarray]:
        X = A.abs_cords_x
        Y = A.abs_cords_y
        return X, Y
    
    def opt_myCustomFunc2(self, A:load.single_line, B:load.single_line) -> tuple[np.ndarray,np.ndarray]:
        X = B.abs_cords_x
        Y = B.abs_cords_y
        return X, Y