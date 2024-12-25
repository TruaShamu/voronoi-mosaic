import cv2
import numpy as np
import random
import math
import time
class VoronoiMosaic:
    def __init__(self, input_image):
        self.input_image = input_image
        self.region_assignment = None
        self.output_image = None
    
    # Generate seeds for the Voronoi diagram
    def generate_seeds(self, num_seeds):
        h, w = self.input_image.shape[:2]
        seeds = np.column_stack((
            np.random.randint(0, w, num_seeds),
            np.random.randint(0, h, num_seeds)
        ))
        return seeds.tolist()

    # Generate the Voronoi diagram
    def voronoi(self, seeds):
        seeds = np.array(seeds, dtype=np.float32)

        # Generate a grid of all pixels in the image
        x = np.arange(self.input_image.shape[1], dtype=np.float32)
        y = np.arange(self.input_image.shape[0], dtype=np.float32)
        xx, yy = np.meshgrid(x, y)

        # The shape of points is [height, width, 2]
        points = np.stack((xx, yy), axis=-1)
        
        # Chunking
        chunk_size = 100
        # Initialize region assignment for each pixel
        self.region_assignment = np.zeros(self.input_image.shape[:2], dtype=np.int32)
        
        # Chunking points
        for i in range(0, points.shape[0], chunk_size):
            for j in range(0, points.shape[1], chunk_size):
                chunk = points[i:i+chunk_size, j:j+chunk_size]
                distances = np.sum((chunk[..., np.newaxis, :] - seeds) ** 2, axis=-1)
                self.region_assignment[i:i+chunk_size, j:j+chunk_size] = np.argmin(distances, axis=-1)

    # Assign colors to each region
    def region_color(self, num_seeds):
        region_colors = np.zeros((num_seeds, 3), dtype=np.uint8)
        for i in range(num_seeds):
            mask = self.region_assignment == i
            if np.any(mask):
                region_colors[i] = np.mean(self.input_image[mask], axis=0)
        return region_colors
    
    def region_color(self, num_seeds):
        region_colors = np.zeros((num_seeds, 3), dtype=np.uint8)
        masks = [self.region_assignment == i for i in range(num_seeds)]
        for channel in range(3):
            for i, mask in enumerate(masks):
                if np.any(mask):
                    pixels = self.input_image[mask, channel]
                    region_colors[i, channel] = np.mean(pixels)
        return region_colors

    # Generate the Voronoi mosaic
    def generate_mosaic(self, num_seeds):
        seeds = self.generate_seeds(num_seeds)
        print("Seeds generated")
        self.voronoi(seeds)
        print("Voronoi diagram generated")
        region_colors = self.region_color(num_seeds)
        print("Region colors generated")
        self.output_image = region_colors[self.region_assignment]
        # draw the seeds on the output image
        for seed in seeds:
            cv2.circle(self.output_image, (seed[0], seed[1]), 1, (255, 255, 255), -1)
        return self.output_image
    
def process_chunk(args):
    chunk, seeds = args
    distances = np.sum((chunk[..., np.newaxis, :] - seeds) ** 2, axis=-1)
    return np.argmin(distances, axis=-1)
if __name__ == '__main__':
    time_init = time.time()
    image = cv2.imread('lena.png')
    voronoi_mosaic = VoronoiMosaic(image)
    output_image = voronoi_mosaic.generate_mosaic(10000)
    cv2.imwrite('output.jpg', output_image)
    print("Time taken: ", time.time() - time_init)