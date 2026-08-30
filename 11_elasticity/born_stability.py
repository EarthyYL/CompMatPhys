"""Verify Born stability criteria of fcc-Al with the experimental
values given in the lecture
"""

import numpy as np

C = np.zeros((6,6))
C[[0,1,2],[0,1,2]] = 176.7 #C11
C[[0,0,1,1,2,2],[1,2,0,2,0,1]] = 122.4 #C12
C[[3,4,5],[3,4,5]] = 78.0 #C44
print(C)
print(np.linalg.det(C))
assert np.linalg.det(C) > 0
