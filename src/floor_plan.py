import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pytesseract
from PIL import Image

class Map:
    def __init__(self, image_path, scale=None):
        self.image_path = image_path
        self.matrix = self.image_to_matrix()
        self.marker_point = {}
        self.current_location = None
        self.marker_label = []
        self.scale = None
        
    def process_image(self):
        areas = self.recognize_text()
        height, width = self.matrix.shape
        # self.matrix = cv2.bitwise_not(self.matrix)
        counter = 1
        for area in areas:
            # Add the text detected as the label of the area
            self.marker_label.append(area[0])

            # Get the coordinates and dimensions of the inner matrix
            x2, y2, w2, h2 = area[1]

            # Insert the smaller matrix into the filled_matrix
            self.matrix[y2:y2+h2, x2:x2+w2] = 255

            # mask = np.zeros((height+2, width+2), np.uint8)

            cv2.floodFill(self.matrix, None, (x2,y2), counter)
            self.matrix[y2:y2+h2, x2:x2+w2] = counter

            # Note te marker point with the centroid of the area
            # TODO: need to find the centroid of the point to improve navigation
            self.marker_point[area[0]] = [x2,y2,w2,h2]
            print('processed', area[0], area[1],counter)
            counter += 1

    def image_to_matrix(self):
       # Load the image in grayscale (0 = black, 255 = white)
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)

        # Threshold the image to binary (0 = black, 255 = white)
        _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        # Find the bounding box of the non-white pixels
        # TODO this assume that the outer boundary is a box
        coords = np.argwhere(binary_image != 255)
        x_min, y_min = coords.min(axis=0)
        x_max, y_max = coords.max(axis=0) + 1   # slices are exclusive at the top

        # Crop the image to this bounding box
        cropped_image = binary_image[x_min:x_max, y_min:y_max]

        # Convert the image to a matrix
        matrix = np.array(cropped_image)
        
        return matrix


    def visualize_matrix(self):
        '''
        TODO this could be cached as plot and refreshed
        matrix: x,y of the map representation
        location: x,y of the location inside the matrix
        '''
        # Create a figure and a set of subplots
        fig, ax = plt.subplots()

        if self.current_location is not None:
            self.add_point(self.current_location[0], self.current_location[1])

        # Display an image on the axes
        cmap = plt.cm.colors.ListedColormap(['black', 'lime', 'yellow','red','green','red','brown','purple','pink','brown','gray','cyan','white'])
        ax.imshow(self.matrix, cmap=cmap,vmin=0,vmax=13)

        # Hide grid lines
        ax.grid(True)

        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])

        plt.show()
    
    def recognize_text(self):
        '''
        Using pytesseract to do OCR on a set image
        '''
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(self.matrix, (5, 5), 0)

        # Apply adaptive thresholding
        binary_image = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Perform dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        binary_image = cv2.dilate(binary_image, kernel, iterations=1)
        binary_image = cv2.erode(binary_image, kernel, iterations=1)

        # Use Tesseract to find text in the image
        custom_config = r'--oem 3 --psm 6'
        data = pytesseract.image_to_data(binary_image, output_type=pytesseract.Output.DICT, config=custom_config)

        # Initialize a list to hold the recognized text and its position
        areas = []

        # Iterate over each detected word
        for i in range(len(data['text'])):
            # If the word is not empty
            if data['text'][i].strip():
                # Get the bounding box coordinates for the word
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                # Add the word and its bounding box coordinates to the list
                areas.append((data['text'][i], (x, y, w, h)))

        # Return the list of recognized text and positions
        return areas

if __name__ == '__main__':
    obj = Map("sample2.jpg")
    obj.process_image()
    print(obj.matrix)
    obj.visualize_matrix()
    
    



