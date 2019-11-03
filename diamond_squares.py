import random as rand
import numpy as np
from collections import deque

# n - velikost stranice kvadratne mreze
# r - nakljucnost

rand.seed(4)
def diamond_squares(n, r, visina=256):
	# Naredimo mrezo
	mreza = [[0]*n for i in range(n)]

	# Nastavimo vrednosti v ogliscih
	mreza[0][0] = rand.randint(-visina, visina)
	mreza[n - 1][0] = rand.randint(-visina, visina)
	mreza[0][n - 1] = rand.randint(-visina, visina)
	mreza[n - 1][n - 1] = rand.randint(-visina, visina)

	tlakovec = n - 1

	# "Tlakujemo mrezo"
	# Vsakic razpolovimo tlakovec
	while tlakovec > 1:
		polovica = tlakovec // 2

		# Nastavimo vrednosti v sredini tlakovcev (Diamantni korak)
		for x in range(0, n - 1, tlakovec):
			for y in range(0, n - 1, tlakovec):
				sestevekKotov = mreza[x][y] + mreza[x + tlakovec][y] + mreza[x][y + tlakovec] + mreza[x + tlakovec][y + tlakovec]
				avg = sestevekKotov / 4
				avg += rand.randint(-r, r)
				mreza[x + polovica][y + polovica] = avg

		# Nastavimo vrednosti v sredinah stranic tlakovcev (Kvadratni korak)
		for x in range(0, n - 1, polovica):
			for y in range((x + polovica) % tlakovec, n - 1, tlakovec):
				avg = mreza[(x - polovica + n - 1) % (n - 1)][y] + mreza[(x + polovica) % (n - 1)][y] + mreza[x][(y + polovica) % (n - 1)] + mreza[x][(y - polovica + n - 1) % (n - 1)]

				avg /= 4.0
				avg += rand.randint(-r, r)

				mreza[x][y] = avg

				
				if x == 0:
					mreza[n - 1][y] = avg
				if y == 0:
					mreza[x][n - 1] = avg

		# Vsak krog zmanjsamo nakljucnost, nikoli pa ne sme pasti na nic!
		r = max(r // 2, 1)
		tlakovec = tlakovec // 2

	return mreza

# Generiraj relief
n =  2**10 + 1
r = 10 * n
height = n//5
m = diamond_squares(n, r, height)
x = np.arange(n)
y = np.arange(n)
X, Y = np.meshgrid(x, y)

# Ustvarjanje slike
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook
import matplotlib.colors as colors

# Velikosti pisav
velikost = 15
plt.rc('font', size=velikost)
plt.rc('axes', titlesize=velikost)
plt.rc('axes', labelsize=velikost)
plt.rc('xtick', labelsize=velikost)
plt.rc('ytick', labelsize=velikost)
plt.rc('legend', fontsize=velikost)
plt.rc('figure', titlesize=velikost)
fig, ax = plt.subplots(constrained_layout=True)


colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 256))
colors_land = plt.cm.terrain(np.linspace(0.25, 1, 256))
all_colors = np.vstack((colors_undersea, colors_land))
terrain_map = colors.LinearSegmentedColormap.from_list('terrain_map', all_colors)
divnorm = colors.DivergingNorm(vmin=-r-height, vcenter=0, vmax=r+height)
pcm = ax.pcolormesh(X, Y, m, rasterized=True, norm=divnorm, cmap=terrain_map,)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal', 'box')
fig.colorbar(pcm, shrink=0.6, extend='both', label='Nadmorska višina [m]')
plt.savefig('diamond_squares.png', bbox_inches='tight')
plt.show()
# plt.close()