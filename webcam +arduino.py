import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import serial
import time
#사진 마음에 드는지 확인하고 넘어가도록!
# 사진 저장할 때 번호 메겨지도록! 근데 코드가 끝나면 숫자가 남지 않는걸..?
#사진 찍힌게 1:1사진인가.? 잘라도 1:1이도록 카메라 위치 잘 조정해야할듯 (1:1은 성공!)
#집가서 웹캠 사진이 짤리는지 확인해야할듯

CAM_ID = 0
def capture(camid = CAM_ID):

    cam= cv2.VideoCapture(cv2.CAP_DSHOW+1)

    if cam.isOpened() == False:
        print ('cant open the cam (%d)' % camid)
        return None

    ret, frame = cam.read()
    if frame is None:
        print ('frame is not exist')
        return None

    # png로 압축 없이 영상 저장 
    cv2.imwrite('test.png',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])

#이미지 저장
    cam.release()

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')#컵홀더
model2 = tensorflow.keras.models.load_model('keras_model2.h5')#빨대

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
ser = serial.Serial('COM3', 9600)
# Replace this with the path to your image

val = ser.readline()
flag = int(val.decode()[:len(val) - 1])

if flag==100:
    while(1):
        capture()
        image = Image.open('test.png')

        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        #cv2.imwrite('save_image.jpg', src)

        #turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        image.show()
        answer=input("이 사진으로 분류를 진행하시겠습니까? 맞으면 y 아니면 n을 눌러주세요.")
        if answer=='y':
            break
        elif answer=='n':
            continue
        else:
            print("다시 한번 묻습니다. 이 사진으로 분류를 진행하시겠습니까? 맞으면 y 아니면 n을 눌러주세요.")

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array

# run the inference
prediction1 = model.predict(data)
prediction2=model2.predict(data)
print("컵홀더")
print(prediction1)
if prediction1[0,0]>prediction1[0,1]:
    holder=1
    print("컵홀더가 있습니다.\n")
elif prediction1[0,0]<prediction1[0,1]:
    print("컵홀더가 없습니다.\n")
    holder=0
else:
    print("판단 불가! 다시한번 시도해주세요!\n")

print("빨대")
print(prediction2)
if prediction2[0,0]>prediction2[0,1]:
    print("빨대가 있습니다.\n")
    straw=1
elif prediction2[0,0]<prediction2[0,1]:
    print("빨대가 없습니다.\n")
    straw=0
else:
    print("판단 불가! 다시한번 시도해주세요!\n")

if holder==0 and straw==0:
    send= 'a'
    send = send.encode('utf-8')
    ser.write(send)
    time.sleep(0.5)

elif holder==1 and straw==0:
    send= 'b'
    send = send.encode('utf-8')
    ser.write(send)
    time.sleep(0.5)
elif holder==0 and straw==1:
    send= 'c'
    send = send.encode('utf-8')
    ser.write(send)
    time.sleep(0.5)
else:
    send= 'd'
    send = send.encode('utf-8')
    ser.write(send)
    time.sleep(0.5)


