import cv2
import numpy as np
import random
import math

class VoronoiMosaic:
    input_image = None
    output_image = None
    region_assignment = None
    seeds = None
    regionpixels = [] # List of pixels in each region
    regioncolors = [] # rgb values of each region
    
    def __init__(self, input_image):
        self.input_image = input_image
        self.output_image = np.zeros_like(input_image)
        self.region_assignment = np.zeros((input_image.shape[0], input_image.shape[1]), dtype=int) 
        self.regionpixels = [[] for _ in range(0)]
    
    def generate_seeds(self, num_seeds):
        seeds = []
        for i in range(num_seeds):
            seeds.append((random.randint(0, self.input_image.shape[1] - 1), random.randint(0, self.input_image.shape[0] - 1)))
        return seeds
    
    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def voronoi(self, seeds):
        for i in range(self.input_image.shape[1]):
            for j in range(self.input_image.shape[0]):
                distances = [self.distance((i, j), seed) for seed in seeds]
                self.region_assignment[j, i] = distances.index(min(distances))
                self.regionpixels[self.region_assignment[j, i]].append((i, j))
    
    def region_color(self):
        for i in range(len(self.regionpixels)):
            r = 0
            g = 0
            b = 0
            for pixel in self.regionpixels[i]:
                r += self.input_image[pixel[1], pixel[0]][0]
                g += self.input_image[pixel[1], pixel[0]][1]
                b += self.input_image[pixel[1], pixel[0]][2]
            r = r // len(self.regionpixels[i])
            g = g // len(self.regionpixels[i])
            b = b // len(self.regionpixels[i])
            self.regioncolors.append((r, g, b))
    
    def generate_mosaic(self, num_seeds):
        # Generate seeds
        seeds = self.generate_seeds(num_seeds)
        self.regionpixels = [[] for _ in range(num_seeds)]
        # Generate Voronoi diagram
        self.voronoi(seeds)
        # Generate region colors
        self.region_color()
        # color each pixel with its region color
        for i in range(self.input_image.shape[1]):
            for j in range(self.input_image.shape[0]):
                self.output_image[j, i] = self.regioncolors[self.region_assignment[j, i]]
        return self.output_image

# Load the image
image = cv2.imread('lena.png')
voronoi_mosaic = VoronoiMosaic(image)
output_image = voronoi_mosaic.generate_mosaic(100)
cv2.imwrite('output.jpg', output_image)
