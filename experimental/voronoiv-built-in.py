import cv2
import numpy as np
from scipy.spatial import Voronoi
import time

class VoronoiMosaic:
    def __init__(self, input_image):
        self.input_image = input_image
        self.output_image = None

    # Generate seeds for the Voronoi diagram
    def generate_seeds(self, num_seeds):
        h, w = self.input_image.shape[:2]
        seeds = np.column_stack((
            np.random.randint(0, w, num_seeds),
            np.random.randint(0, h, num_seeds)
        ))
        return seeds

    # Assign colors to Voronoi regions based on seeds
    def region_color(self, vor, seeds):
        region_colors = np.zeros((len(seeds), 3), dtype=np.uint8)

        for i, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]
            if region and -1 not in region:
                mask = np.zeros(self.input_image.shape[:2], dtype=np.uint8)
                polygon = np.array([vor.vertices[vertex] for vertex in region], dtype=np.int32)
                cv2.fillPoly(mask, [polygon], 1)
                if np.any(mask):
                    region_colors[i] = np.mean(self.input_image[mask.astype(bool)], axis=0)
        return region_colors

    # Generate the Voronoi mosaic
    def generate_mosaic(self, num_seeds):
        seeds = self.generate_seeds(num_seeds)
        print("Seeds generated")

        # Create Voronoi diagram
        vor = Voronoi(seeds)
        print("Voronoi diagram generated")

        # Assign region colors
        region_colors = self.region_color(vor, seeds)
        print("Region colors generated")

        # Initialize output image
        self.output_image = np.zeros_like(self.input_image)

        for i, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]
            if region and -1 not in region:
                # Fill the region with the assigned color
                polygon = np.array([vor.vertices[vertex] for vertex in region], dtype=np.int32)
                cv2.fillPoly(self.output_image, [polygon], region_colors[i].tolist())

        return self.output_image

if __name__ == '__main__':
    time_init = time.time()

    # Load input image
    image = cv2.imread('lena.png')
    #image = cv2.resize(image, (0, 0), fx=0.3, fy=0.3)
    #print(image.shape)

    # Create VoronoiMosaic instance and generate mosaic
    voronoi_mosaic = VoronoiMosaic(image)
    output_image = voronoi_mosaic.generate_mosaic(3000)

    # Save output image
    cv2.imwrite('output.jpg', output_image)
    print("Time taken: ", time.time() - time_init)
