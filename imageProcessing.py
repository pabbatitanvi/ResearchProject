import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import os
import DobotDllType as dType
import time as t


CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "COM10", 115200)[0]
print("Connect status:", CON_STR[state])


#opencv stores images in BGR format
def resize(image):
    # x_start, x_end = 170, 300
    # y_start, y_end = 0, 238

    # cropped_image = image[y_start:y_end, x_start:x_end]
    #resize_image = cv.resize(cropped_image, (200, 200))
    resize_image = cv.resize(image, (200, 200))

    cv.imshow('resize_image', resize_image)
    cv.waitKey(0)
    return resize_image

#canny edge detection
def canny(image, msg = 'n'):
    canny_image = None
    if msg == 'y':
        smooth_edges = cv.GaussianBlur(image, (3, 3), 1)
        canny_image = cv.Canny(smooth_edges, 45, 200)
    else:
        canny_image = cv.Canny(image, 45, 200)
    smooth_edges = cv.GaussianBlur(canny_image, (9, 9), 1)
    cv.imshow('canny_image', canny_image)
    cv.waitKey(0)
    
    return canny_image  

#gets coordinates of the image
def getCoordinates(image, x = (170, 300), y = (-190, 238)):
    coordinates = np.argwhere(image > 0)

    return coordinates


    adjusted_coordinates = [coord for coord in coordinates if 
                            coord[1] >= x[0] and coord[1] <= x[1] or
                            coord[0] >= y[0] and coord[0] <= y[1]]
    print(adjusted_coordinates)
    
    return adjusted_coordinates

def plotCoordinates(coordinates, size = 7):
    coordinates_np = np.array(coordinates)
    #plt.plot(coordinates_np[:, 1], coordinates_np[:, 0], "-o", markersize = size)
    plt.plot(coordinates_np[:, 1], coordinates_np[:, 0], "k.", markersize = size)
    plt.gca().invert_yaxis()
    plt.show()

#draws coordinates using the dobot api
def drawCoordinates(coordinates):

    for x, y in coordinates:
        #addinag values to the coordinates so they will be in range
        x1 = x+ 175
        y1 = y + 100
        print(f"({x1}, {y1})")
        move = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x1, y1, -54.4, 0, isQueued = 1)

        if move == 0:
            print(f"Error moving to ({x1}, {y1})")

        #delays it for 2 seconds
        t.sleep(2)

    return 0


if __name__ == "__main__":

    #gets the home parameters using the api
    print(dType.GetHOMEParams(api))
    #sets the home parameters
    dType.SetHOMEParams(api, 250, 0, 0, 0)
    #prints the home parameters to check if it changed
    print(dType.GetHOMEParams(api))

    image_1 = cv.imread("landscape.jpg",0)
    resized_image = resize(image_1)
    modified_image = canny(resized_image, 'y')
    coordinates = getCoordinates(modified_image)
    plotCoordinates(coordinates, 3)
    #drawCoordinates(coordinates)

    image_2 = cv.imread("dog.jpeg", 0)
    resized_image = resize(image_2)
    modified_image = canny(resized_image, 'y')
    coordinates = getCoordinates(modified_image)
    plotCoordinates(coordinates, 3)
    #drawCoordinates(coordinates)

    image_3 = cv.imread("shapes.jpg", 0)
    resized_image = resize(image_3)
    modified_image = canny(resized_image)
    coordinates = getCoordinates(modified_image)
    plotCoordinates(coordinates)
    #drawCoordinates(coordinates)

    image_4 = cv.imread("stickfigure.jpeg", 0)
    resized_image = resize(image_4)
    modified_image = canny(resized_image)
    coordinates = getCoordinates(modified_image)
    print(coordinates)
    plotCoordinates(coordinates)
    #drawCoordinates(coordinates)

    image_5 = cv.imread("circle.jpg", 0)
    resized_image = resize(image_5)
    modified_image = canny(resized_image)
    coordinates = getCoordinates(modified_image)
    print(coordinates)
    plotCoordinates(coordinates)
    #drawCoordinates(coordinates)

    image_6 = cv.imread("line.jpg", 0)
    resized_image = resize(image_6)
    modified_image = canny(resized_image)
    coordinates = getCoordinates(modified_image)
    print(coordinates)
    plotCoordinates(coordinates)
    #drawCoordinates(coordinates)
    
    dType.DisconnectDobot(api)

  