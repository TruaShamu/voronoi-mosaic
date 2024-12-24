# voronoi-mosaic

# game plan:
1. generate n random seeds / points.
2. brute force the generation of a voronoi diagram - for each pixel, allocate it to a region depending on the seed to which it has the shortest euclidean distance. we can naively persist the regions and all the pixels are in it.
3. for each region, find a representative color, which is the mean of all pixel RGB values in the region.
4. recolor each region with the representative color.
----
extra items:
e1. run edge detection on the input image using adaptive thresholding and 'paint' the edges back onto the mosaic to give better form or shape to the main subjects of the image.
(there's probably some other visual saliency things we could do too)
e2. a trivial way to optimize is to chunk pixels together (so a nxn pixel image can be translated to mxm chunks, where m < n)
e3. look into better ways of finding the voronoi diagram (i.e. fortunes, lloyds)
e4. look into hausner's paper on mosaic tiling
