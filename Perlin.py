import noise
import numpy as np
import matplotlib.pyplot as plt
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

# Lastnosti suma
n = 1024
shape = (n,n)
scale = 400
octaves = 8
persistence = 0.3
lacunarity = 4.0

x = np.arange(n)
y = np.arange(n)
X, Y = np.meshgrid(x, y)

m = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        m[i][j] = noise.pnoise2(i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    repeatx=n, 
                                    repeaty=n, 
                                    base=0)

# Reskaliramo sum, da je bolj podoben tistemu ki ga generirata karo-kvadrat in premik sredisca. 
m = m*3000

# Plot
fig, ax = plt.subplots(constrained_layout=True)
colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 256))
colors_land = plt.cm.terrain(np.linspace(0.25, 1, 256))
all_colors = np.vstack((colors_undersea, colors_land))
terrain_map = colors.LinearSegmentedColormap.from_list('terrain_map',
    all_colors)

divnorm = colors.DivergingNorm(vmin=-3000, vcenter=0, vmax=3000)
pcm = ax.pcolormesh(X, Y, m, rasterized=True, norm=divnorm, cmap=terrain_map,)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_aspect('equal', 'box')
fig.colorbar(pcm, shrink=0.6, extend='both', label='Nadmorska višina [m]')
plt.savefig('perlin.png', bbox_inches='tight')
plt.show()