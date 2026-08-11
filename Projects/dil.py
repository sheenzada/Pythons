import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111,projection='3d')

t = np.linspace(0,2*np.pi, 100)
x = 16 * np.sin(t)**3
y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)

z = np.linspace(-5, 5 , 100)
X,Z = np.meshgrid(x , z)
Y, _ = np.meshgrid(y,z)

ax.plot_surface(X, np.tile(y , (100, 1)) , Z , cmap='Reds' , alpha=0.9)
ax.set_axis_off()
plt.show()