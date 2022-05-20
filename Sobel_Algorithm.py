# #!/usr/bin/env python3

import cv2
import numpy as np

laplacian_k=[[1,-2,1],[-2,5,-2],[1,-2,1]]
gx=[[-1,0,1],[-2,0,2],[-1,0,1]]
gy=[[-1,-2,-1],[0,0,0],[1,2,1]]


def dosomething(x):
  pass

cv2.namedWindow('Maximum gradient')
cv2.createTrackbar('G','Maximum gradient',0,255,lambda x:dosomething(x))

cap=cv2.VideoCapture("/dev/video2")
cap.set(cv2.CAP_PROP_CONVERT_RGB,0)
cap.set(cv2.CAP_PROP_MODE,3)

grad_x=np.zeros((20,20))
grad_y=np.zeros((20,20))
laplacian=np.zeros((20,20))
out=np.zeros((20,20),np.uint8)

while True:
  # get image
  ret,img=cap.read()

  if ret:
    # crop middle area
    img=np.reshape(img,(180,160))[50:70,70:90]

    # median filter for special three pixels
    img[16][8]=np.sort((img[15][7],img[15][8],img[15][9],img[16][7],img[16][9],img[17][7],img[17][8],img[17][9]))[4]
    img[18][19]=np.sort((img[17][18],img[17][19],128,img[18][18],128,img[19][18],img[19][19],128))[4]
    img[5][18]=np.sort((img[4][17],img[4][18],img[4][19],img[5][17],img[5][19],img[6][17],img[6][18],img[6][19]))[4]

    # find gradient x and y
    for y in range(img.shape[1]-2):
      for x in range(img.shape[0]-2):
        laplacian[y+1][x+1]=laplacian_k[0][0]*img[y][x]+laplacian_k[0][1]*img[y][x+1]+laplacian_k[0][2]*img[y][x+2]+laplacian_k[1][0]*img[y+1][x]+laplacian_k[1][1]*img[y+1][x+1]+laplacian_k[1][2]*img[y+1][x+2]+laplacian_k[2][0]*img[y+2][x]+laplacian_k[2][1]*img[y+2][x+1]+laplacian_k[2][2]*img[y+2][x+2]
        grad_x[y+1][x+1]=gx[0][0]*img[y][x]+gx[0][1]*img[y][x+1]+gx[0][2]*img[y][x+2]+gx[1][0]*img[y+1][x]+gx[1][1]*img[y+1][x+1]+gx[1][2]*img[y+1][x+2]+gx[2][0]*img[y+2][x]+gx[2][1]*img[y+2][x+1]+gx[2][2]*img[y+2][x+2]
        grad_y[y+1][x+1]=gy[0][0]*img[y][x]+gy[0][1]*img[y][x+1]+gy[0][2]*img[y][x+2]+gy[1][0]*img[y+1][x]+gy[1][1]*img[y+1][x+1]+gy[1][2]*img[y+1][x+2]+gy[2][0]*img[y+2][x]+gy[2][1]*img[y+2][x+1]+gy[2][2]*img[y+2][x+2]
        out[y+1][x+1]=np.sqrt(grad_x[y+1][x+1]**2+grad_y[y+1][x+1]**2)/10
        # out=cv2.addWeighted(cv2.convertScaleAbs(grad_x/10),0.5,cv2.convertScaleAbs(grad_y/10),0.5,0)

    # display grade
    cv2.setTrackbarPos('G','Maximum gradient',np.max(out))

    # display all
    cv2.imshow('raw',cv2.resize(np.vstack((np.hstack((cv2.convertScaleAbs(laplacian),out)),np.hstack((cv2.convertScaleAbs(grad_x),cv2.convertScaleAbs(grad_y))))),(600,600),interpolation=cv2.INTER_NEAREST))

  # close app
  if cv2.waitKey(33)==27:
    break

cap.release()
