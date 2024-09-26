import cv2
import numpy as np
from matplotlib import pyplot as plt
from astropy.stats import sigma_clipped_stats
from photutils.datasets import make_100gaussians_image
from photutils.detection import find_peaks
from astropy.visualization import simple_norm
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils.aperture import CircularAperture

# Open the default camera
# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam = cv2.VideoCapture(0)

cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cam.set(cv2.CAP_PROP_EXPOSURE, -10) 

# cam.set(cv2.CAP_PROP_SETTINGS,1)

# input("Press Enter to continue...")

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 1, (frame_width, frame_height))

i = 0
# frameHSV = cv2.CreateImage((frame_width, frame_height), 1, 3)
# frameHSV = np.zeros((frame_height, frame_width, 3), np.uint8)

while True:
    ret, frame = cam.read()

    if i > 20:
        print("changing exposure")

        # cam.set(cv2.CAP_PROP_EXPOSURE, -10) 
        # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0); 
        # cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)


    # cv2.CvtColor(frame, frameHSV, cv2.CV_BGR2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # print("dimensione frame")
    # print(frame.shape)
    # print(" ")

    # Write the frame to the output file
    out.write(frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    # if i == 20:
    #     print("dimensione hsv")
    #     print(hsv.shape)
    #     print(" ")
        
        # # cv2.imshow('Camera HSV', hsv)
        # plt.imshow(hsv[:,:,2], cmap='gray')
        # plt.colorbar()
        # plt.show()

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

    i = i + 1

# Release the capture and writer objects
cam.release()
out.release()
cv2.destroyAllWindows()

# Peak detection

data = hsv[:,:,2]

box_size = 11
sigma = 3
mean, median, std = sigma_clipped_stats(data, sigma=sigma)
threshold = median + (5.0 * std)
threshold = 200
tbl = find_peaks(data, threshold, box_size=box_size)
tbl['peak_value'].info.format = '%.8g'  # for consistent table output
print(tbl[:10])  # print only the first 10 peaks

positions = np.transpose((tbl['x_peak'], tbl['y_peak']))
apertures = CircularAperture(positions, r=5.0)
norm = simple_norm(data, 'sqrt', percent=99.9)
plt.imshow(data, cmap='Greys_r', origin='lower', norm=norm,
           interpolation='nearest')
apertures.plot(color='#0547f9', lw=1.5)
plt.xlim(0, data.shape[1] - 1)
plt.ylim(0, data.shape[0] - 1)
plt.colorbar()
plt.show()

