import cv2
import numpy as np
from matplotlib import pyplot as plt
from astropy.stats import sigma_clipped_stats
from photutils.datasets import make_100gaussians_image
from photutils.detection import find_peaks
from astropy.visualization import simple_norm
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils.aperture import CircularAperture

data = np.load("immagine_test.npy")

box_size = 200
sigma = 3
mean, median, std = sigma_clipped_stats(data, sigma=sigma)
threshold = median + (5.0 * std)
# threshold = 200
tbl = find_peaks(data, threshold, npeaks=1, box_size=box_size)

print(f"mean: {mean} median: {median} std: {std}")
print(f"threshold: {threshold}")
tbl['peak_value'].info.format = '%.8g'  # for consistent table output
print(tbl[:10])  # print only the first 10 peaks

positions = np.transpose((tbl['x_peak'], tbl['y_peak']))
apertures = CircularAperture(positions, r=5.0)
norm = simple_norm(data, 'sqrt', percent=99.9)
plt.imshow(data)
# plt.imshow(data, cmap='Greys_r', origin='lower', norm=norm,
#            interpolation='nearest')
apertures.plot(color='#0547f9', lw=1.5)
plt.xlim(0, data.shape[1] - 1)
plt.ylim(0, data.shape[0] - 1)
plt.colorbar()
plt.show()

