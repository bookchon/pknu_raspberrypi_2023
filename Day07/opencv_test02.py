import cv2

# 1. 일반이미지
# img = cv2.imread('./Day07/calcifer.jpeg')

# 2. 흑백이미지
# img = cv2.imread('./Day07/calcifer.jpeg', cv2.IMREAD_GRAYSCALE)

# 4. 원본을 그대로 두고 흑백을 추가
img = cv2.imread('./Day07/calcifer.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. 이미지 사이즈 축소
# img_small = cv2.resize(img, (200, 90))

# 5. 이미지 자르기
height, width, channel = img.shape
print(height, width, channel)

img_crop = img[:, :int(width / 2)] # height, width
gray_crop = gray[:, :int(width / 2)]

# 6. 이미지 블러
img_blur = cv2.blur(img_crop, (10,10)) # 숫자가 클 수록 더 많이 블러 됨

# 4. 원본
# cv2.imshow('Original', img) 
# cv2.imshow('Gray', gray)

# 5. 이미지 자르기
# cv2.imshow('Original half', img_crop)
# cv2.imshow('Gray half', gray_crop)

# 6. 이미지 블러
cv2.imshow('Blur half', img_blur)

cv2.waitKey(0)
cv2.destroyAllWindows()