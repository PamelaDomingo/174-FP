import cv2
import easyocr
from IPython.display import Image
from pylab import rcParams

haarcascade = "model\haarcascade_russian_plate_number.xml"

cap = cv2.VideoCapture(0)

cap.set(3,640) # width
cap.set(4,480) # height

min_area = 1000
count = 0

pics = ['plates/try0.jpg', 'plates/try1.jpg']

# Image("plates/scanned_img_0.jpg")
reader = easyocr.Reader(['en'], gpu = False)
for p in pics:
    output = reader.readtext(p)
    print(output)
    print()
# cord = output[-1][0]
# a = list(zip(*cord))
# min(a[0])
# min(a[1])

# max(a[0])
# max(a[1])

# print(min(a[0]), min(a[1]), max(a[0]), max(a[1]))

# x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
# x_max, y_max = [int(max(idx)) for idx in zip(*cord)]

# # from pylab import rcParams
# rcParams['figure.figsize'] = 20, 30

# image = cv2.imread('plates/scanned_img_0.jpg')
# cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,0,255),2)
# cv2.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# cv2.waitKey(0)
# cv2.destroyAllWindows()