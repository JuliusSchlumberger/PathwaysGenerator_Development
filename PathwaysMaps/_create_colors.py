import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


# Generate colors
color_scale = 'viridis'
drought_agr_colors = plt.get_cmap(color_scale)(np.linspace(0.1, .9, 5))
drought_shp_colors = plt.get_cmap(color_scale)(np.linspace(0.1, .9, 4))
flood_agr_colors = plt.get_cmap(color_scale)(np.linspace(0.1, .9, 6))
flood_urb_colors = plt.get_cmap(f'{color_scale}_r')(np.linspace(0.1, .9, 7))

MEASURE_COLORS = {
    '100': 'Grey',
    '0': 'Grey',}

for i in range(1, 6):
    MEASURE_COLORS[str(i)] = mcolors.to_hex(drought_agr_colors[i-1])

for i in range(6, 10):
    MEASURE_COLORS[str(i)] = mcolors.to_hex(drought_shp_colors[i-6])

for i in range(10, 16):
    MEASURE_COLORS[str(i)] = mcolors.to_hex(flood_agr_colors[i - 10])

for i in range(13, 20):
    MEASURE_COLORS[str(i)] = mcolors.to_hex(flood_urb_colors[i-13])


BASE_COLORS_SECTORS = {
    'flood_agr': 'darkviolet',
    'drought_agr': 'violet',
    'flood_urb': 'orangered',
    'drought_shp': 'gold'
}