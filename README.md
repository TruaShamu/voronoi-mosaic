# voronoi-mosaic

# game plan:
1. generate n random seeds / points.
2. brute force the generation of a voronoi diagram - for each pixel, allocate it to a region depending on the seed to which it has the shortest euclidean distance. we can naively persist the regions and all the pixels are in it.
3. for each region, find a representative color, which is the mean of all pixel RGB values in the region.
4. recolor each region with the representative color.

extra items:

e1. run edge detection on the input image using adaptive thresholding and 'paint' the edges back onto the mosaic to give better form or shape to the main subjects of the image.
(there's probably some other visual saliency things we could do too)

e2. a trivial way to optimize is to chunk pixels together (so a nxn pixel image can be translated to mxm chunks, where m < n)

e3. look into better ways of finding the voronoi diagram (i.e. fortunes, lloyds)

e4. look into hausner's paper on mosaic tiling


#results (as of 12/24)

| Input    | Output (3000 seeds)* |
| -------- | ------- |
| ![image](https://github.com/user-attachments/assets/79113eba-3e28-4853-908a-0e3b4b505c9e)| ![output](https://github.com/user-attachments/assets/ff3293e1-f39e-40f5-82e7-c843d0ed4ca6)|
Takes ~20s for a 512x512 image using 3000 seeds, ~7s for 1000 seeds, ...

