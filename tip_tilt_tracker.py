import cv2
import numpy as np
from matplotlib import pyplot as plt
from astropy.stats import sigma_clipped_stats
from photutils.datasets import make_100gaussians_image
from photutils.detection import find_peaks
from astropy.visualization import simple_norm
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils.aperture import CircularAperture
from time import sleep
import serial.tools.list_ports
import sys

# print([comport.device for comport in serial.tools.list_ports.comports()])
# ports = serial.tools.list_ports.comports()
# serialInst = serial.Serial()

# print( ports )
# for onePort in ports:
#     print( str(onePort))

# sys.exit

def find_one_peak( data ):
    #data is 2d array
    # Peak detection

    # np.save("immagine_test",data)

    box_size = 5
    sigma = 3
    mean, median, std = sigma_clipped_stats(data, sigma=sigma)
    # print(median, std )
    threshold = min( [median + (10.0 * std), 250] )
    # print(threshold)
    #threshold = 200
    tbl = find_peaks(data, threshold, box_size=box_size, npeaks=1)
    if( tbl ):
        tbl['peak_value'].info.format = '%.8g'  # for consistent table output
        # print(tbl[:10])  # print only the first 10 peaks

        positions = np.transpose((tbl['x_peak'], tbl['y_peak'], tbl['peak_value']))
        x = positions[0][0]
        y = positions[0][1]
        val = positions[0][2]
    else:
        positions = None
        x = None
        y = None
        val = None
    # apertures = CircularAperture(positions, r=5.0)
    # norm = simple_norm(data, 'sqrt', percent=99.9)
    # plt.imshow(data, cmap='Greys_r', origin='lower', norm=norm,
    #         interpolation='nearest')
    # apertures.plot(color='#0547f9', lw=1.5)
    # plt.xlim(0, data.shape[1] - 1)
    # plt.ylim(data.shape[0] - 1, 0)
    # plt.colorbar()
    # plt.show()

    return x, y, val



# Open the default camera
# cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam = cv2.VideoCapture(1)

cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
cam.set(cv2.CAP_PROP_EXPOSURE, -10) 

# cam.set(cv2.CAP_PROP_SETTINGS,1)

# input("Press Enter to continue...")

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frame_width,'x',frame_height )

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('output.mp4', fourcc, 1, (frame_width, frame_height))

i = 0
# frameHSV = cv2.CreateImage((frame_width, frame_height), 1, 3)
# frameHSV = np.zeros((frame_height, frame_width, 3), np.uint8)

xlist=[]
ylist=[]
x=-1
y=-1
xold=x
yold=y
cmd='o'
nbad = 0
while True:
    ret, frame = cam.read()

    # cv2.CvtColor(frame, frameHSV, cv2.CV_BGR2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Write the frame to the output file
    # out.write(frame)

    

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('z'):
        print('zero' )
        cmd='z'
    elif cv2.waitKey(1) == ord('n'):
        print('minimum' )
        cmd='n'
    elif cv2.waitKey(1) == ord('m'):
        print('maximum' )
        cmd='m'
    elif cv2.waitKey(1) == ord('s'):
        print('start tracking' )
        cmd='s'
    elif cv2.waitKey(1) == ord('o'):
        print('off' )
        cmd='o'
    elif cv2.waitKey(1) == ord('r'):
        print('resetting angle' )
        cmd='r'
    # elif cv2.waitKey(1) == ord('c'):
    #     print('finding peak')
    #     data = hsv[:,:,2]
    #     pos = find_one_peak( data )
    #     print( pos, pos.shape, pos[0][0], pos[0][1] )

    if( cmd != 'o' ):
        data = hsv[:,:,2]
        x, y, val = find_one_peak( data )
        if( x ):
            nbad = 0
            # print( x, y, val )
            xold = x
            yold = y
            # xlist.append(x)
            # ylist.append(y)
        else:
            nbad+=1
            if( nbad > 100 ):
                cmd = 'o'
                print('no spot')
            print( i, 'no peaks', xold, yold )

    if( x ):
        smessage="%d,%d,%s" %(x,y,cmd)
    else:
        smessage="%d,%d,%s" %(xold,yold,cmd)

# Display the captured frame
    cv2.line(frame, (x, 0), (x, 480), (0, 0, 255), 1)
    cv2.line(frame, (0, y), (640, y), (0, 0, 255), 1)
    cv2.imshow('Camera', frame)
    

    # print(smessage)
    i = i + 1

    # sleep(0.5)

# Release the capture and writer objects
cam.release()
# out.release()
cv2.destroyAllWindows()

# plt.plot(xlist,ylist)
# plt.show()



