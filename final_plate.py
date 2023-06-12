import cv2
import easyocr
import re
import os
import pandas as pd
import openpyxl


def saveToSheet(cplates,image_names):
    
    data = pd.DataFrame({'Plate': cplates, 'Image Name': image_names})
    data.to_excel('plate_data.xlsx', index=False)


def chooseRead(pscans, img_names):
    cln_plates = []
    for s, img_name in zip(pscans, img_names):
        if len(s) == 1:
            cln_plates.append(s[0])
        elif len(s) == 2:
            if len(s[0]) > len(s[1]):
                cln_plates.append(s[0])
            else:
                cln_plates.append(s[1])
        elif len(s) > 1:
            cln_plates.append(s[1])
    print("++++++++++++++ CLEANED PLATES ++++++++++++++")
    print(cln_plates)
    saveToSheet(cln_plates, img_names)

def scanPlate():
    haarcascade = "model\haarcascade_russian_plate_number.xml"
    cap = cv2.VideoCapture(0)

    cap.set(3,640) # width
    cap.set(4,480) # height

    min_area = 1000
    count = 0

    while True:
        success, img = cap.read()

        plate_cascade = cv2.CascadeClassifier(haarcascade)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x,y,w,h) in plates:
            area = w * h

            # detect plate number
            if area > min_area:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255), 2)
        
                img_roi = img[y:y+h, x:x+w]
                cv2.imshow("ROI", img_roi)

        cv2.imshow("Result", img)

        # take 1 screenshot and save to plates folder
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("plates/scanned_img_" + str(count) + ".jpg", img_roi)
            cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
           
            readPlate()

            cv2.putText(img, "Plate Saved", (150,265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,255), 2)
            cv2.imshow("Results", img)
            cv2.waitKey(1)
            cv2.destroyWindow("Results")
            count += 1


        # terminate scan
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def readPlate():
    img_path = "plates/"

    # list of the file names of the screenshots in plates folder
    pics = os.listdir(img_path)

    # list of read plates
    plate_scans = []
    img_names = []

    # read each plate
    reader = easyocr.Reader(['en'], gpu = False)
    for p in pics:
        output = reader.readtext(img_path + p)
        outs = []
        
        for i in output:
            cln = re.sub(r"\W+", "", i[-2])
            outs.append(cln)
        plate_scans.append(outs)
        img_names.append(p)

    print("======= PLATE SCANS =======")
    print(plate_scans)

    chooseRead(plate_scans, img_names)


scanPlate()
# readPlate()



