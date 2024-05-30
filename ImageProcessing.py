import cv2
import numpy as np
class ImageProcessing(object):
    def __init__(self, window_name, image_name):
        self.window_name = window_name
        self.image_name = image_name
        self.image = cv2.imread(self.image_name)


    def show(self, title=None, image=None):
        if image is None:
            image = self.image
        if title is None:
            title = self.window_name
            cv2.imshow(title, image)
            
    def rmbg_by_color(self, hsv_lower, hsv_upper, image = None):
        if image is None:
            image = self.image
        imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, hsv_lower, hsv_upper)
        mask = 255 - mask
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        bg_removed = cv2.bitwise_and(image, mask)
        return bg_removed, mask 

    # def remove_background_by_color(self,hsv_lower,hsv_upper,image=None):
    #     if image is None:
    #         image = self.image
    #     imgHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #     mask = cv2.inRange(imgHSV, hsv_lower, hsv_upper)
    #     mask = 255 - mask
    #     mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #     bg_removed = cv2.bitwise_and(image, mask)
    #     return bg_removed, mask     

    def blend_with_mask(self, blend, mask, image=None):
        if image is None:
            image = self.image
        blend = cv2.resize(blend, image.shape[1::-1])
        mask = cv2.resize(mask, image.shape[1::-1])
        result = cv2.bitwise_and(blend, mask) + cv2.bitwise_and(image,(255-mask))
        return result

    def resize(self, percent, image = None):
        if image is None:
            image = self.image
        # width = int(image.shape[1]*percent/100)
        # height = int(image.shape[0]*percent/100)
        # resize_image = cv2.resize(image, (width, height))

        width = (image.shape[1] * percent / 100)
        height = (image.shape[0] * percent / 100)
        resize_image = cv2.resize(image, (width, height))
        return resize_image
    
    def crop(self, pt_first, pt_second, image = None):
        if image is None:
            image = self.image
        
        x_tl, y_tl = pt_first
        x_dr, y_dr = pt_second

        if x_dr < x_tl:
            x_tl, x_dr = x_dr, x_tl
        if y_dr < y_tl:
            y_dr, y_tl = y_tl, y_dr
        
        image = image[y_tl: y_dr, x_tl: x_dr]
        return image
    
    def ronate(self, angel, image = None, scale = 1.0):
        if image is None:
            image = self.image
        (h,w) = image.shape[:2]
        center = (w/2, h/2)

        rot_mat = cv2.getRotationMatrix2D(center, angel, scale)
        result = cv2.warpAffine(image, rot_mat, (h, w))

        return result   
    
    def contrast_brightness(self, contrast,brightness, image=None):
        # contrast:
        # between 0 and 1: less contrast;
        # > 1: more contrast;
        # 1: unchanged
        # brightness: -127 to 127;
        # 0 unchanged
        if image is None:
            image = self.image
        zeros = np.zeros(image.shape, image.dtype)
        result = cv2.addWeighted(image, contrast, zeros, 0, brightness) #y(i, j) = g(i, j) * contrast + brighness
        return result    
    
    def hue_saturation_value(self, hue, saturation, value, image=None):
        if image is None:
            image = self.image
        hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsvImage)
        zeros = np.zeros(h.shape, h.dtype)
        h = cv2.addWeighted(h, 1.0, zeros, 0, hue)
        s = cv2.addWeighted(s, 1.0, zeros, 0, saturation)
        v = cv2.addWeighted(v, 1.0, zeros, 0, value)
        result = cv2.merge([h, s, v])
        result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

        return result

    def blend(self, blend, alpha, image = None):
        if image is None:
            image = self.image
        blend = cv2.resize(blend, (image.shape[1], image.shape[0]))
        result = cv2.addWeighted(image, alpha, blend, (1.0 - alpha), 0)
        return result
