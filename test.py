import numpy as np
import random
a = [random.choice(range(100)) for i in range(100)]
a = np.array(a)
print(a)
print(a[1:])
print(a[:-1])
print()
b = np.append(a[0], a[1:] - 0.97 * a[:-1])
print(b)
print(len(a), len(b))