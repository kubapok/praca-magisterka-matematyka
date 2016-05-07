import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import sys

if len(sys.argv) < 2:
    sys.exit('Jako argument podaj nazwę pliku z rozszerzeniem')


print('Proszę czekać, to może zająć chwilkę. \nW razie czego można przeskalować obraz na mniejszy')



'''tutaj ładujemy zdjęcie i zmieniamy z kolorowego na szary'''
im = Image.open(sys.argv[1]).convert('LA')
#im.show()

'''reversed dla współrzędnej y, bo obrazek ma współrzędne (0,0) w lewym górnym rogu, czyli inaczej niż się patrzy
na zdjęcie - (0,0) jest wtedy w lewym dolnym rogu
'''
im_plot = [[im.getpixel((i,j))[0] for i in range(im.width)] for j in reversed(range(im.height))]

fig = plt.figure()
ax = fig.gca(projection='3d')
x = np.arange(0, im.width, 1)
y = np.arange(0, im.height, 1)
x,y  = np.meshgrid(x, y)
surf = ax.plot_surface(x, y, im_plot, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)


ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
'''odwracamy oś z żeby wygodniej się patrzyło
'''
plt.gca().invert_zaxis()

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
