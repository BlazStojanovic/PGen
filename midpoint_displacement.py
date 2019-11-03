import random as rand

# n - velikost stranice kvadratne mreze
# r - nakljucnost

rand.seed(0)
def midpoint_displacement(n, r, visina=256):

	# Naredimo mrezo
	mreza = [[0]*n for i in range(n)]

	# Nakljucno nastavimo kotne tocke
	mreza[0][0] = rand.randint(-visina, visina)
	mreza[n - 1][0] = rand.randint(-visina, visina)
	mreza[0][n - 1] = rand.randint(-visina, visina)
	mreza[n - 1][n - 1] = rand.randint(-visina, visina)
	
	# naredimo seznam tock, v katerih znamo izracunati nove vrednosti
	# shranjevali bomo stiri robne tocke in nakljucnost
	q = list()
	q.append((0,0,n-1,n-1,r))

	# dokler imamo na voljo tocke, racunamo srednjo vrednost
	while q:
		zgoraj, levo, spodaj, desno, r = q.pop(0)

		# izracunamo koordinate srednje tocke
		centerX = (levo + desno) // 2
		centerY = (zgoraj + spodaj) // 2

		# nastavimo vrednosti v sredinah stranic
		mreza[centerX][zgoraj] = (mreza[levo][zgoraj] + mreza[desno][zgoraj]) // 2 + rand.randint(-r, r)
		mreza[centerX][spodaj] = (mreza[levo][spodaj] + mreza[desno][spodaj]) // 2 + rand.randint(-r, r)
		mreza[levo][centerY] = (mreza[levo][zgoraj] + mreza[levo][spodaj]) // 2 + rand.randint(-r, r)
		mreza[desno][centerY] = (mreza[desno][zgoraj] + mreza[desno][spodaj]) // 2 + rand.randint(-r, r)

		# nastavimo vrednost v sredini kvadrata
		mreza[centerX][centerY] = (mreza[levo][zgoraj] + mreza[levo][spodaj] 
										+ mreza[desno][zgoraj] + mreza[desno][spodaj]) // 4 + rand.randint(-r, r)

		# Ce imamo prostor, dodamo kote novega kvadrata
		if (desno - levo) > 2:
			q.append((zgoraj, levo, centerY, centerX, r // 2))
			q.append((zgoraj, centerX, centerY, desno, r // 2))
			q.append((centerY, levo, spodaj, centerX, r // 2))
			q.append((centerY, centerX, spodaj, desno, r // 2))

	return mreza

# Generiraj relief
n =  2**10 + 1
r = 10 * n
visina = n//5
m = midpoint_displacement(n, r, visina)
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
terrain_map = colors.LinearSegmentedColormap.from_list('terrain_map',
    all_colors)

divnorm = colors.DivergingNorm(vmin=-r-visina, vcenter=0, vmax=r+visina)

pcm = ax.pcolormesh(X, Y, m, rasterized=True, norm=divnorm,
    cmap=terrain_map,)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal', 'box')
fig.colorbar(pcm, shrink=0.6, extend='both', label='Nadmorska višina [m]')
plt.savefig('midpoint_displacement.png', bbox_inches='tight')
plt.show()

