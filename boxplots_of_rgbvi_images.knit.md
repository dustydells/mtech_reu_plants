
<!-- rnb-text-begin -->

---
title: "R Notebook"
output: html_notebook
editor_options: 
  chunk_output_type: inline
---




<!-- rnb-text-end -->



<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuYGBgclxuaW1nX2ludG9fZGF0YWZyYW1lX2ludG9fYm94cGxvdCA8LSBmdW5jdGlvbihmaWxlX25hbWUsIHBhdGgpIHtcbiAgXG4gICMgUmVhZCBpbiB0aGUgaW1hZ2VcbiAgaW1nIDwtIHJlYWRKUEVHKGZpbGVfbmFtZSlcbiAgXG4gICMgRmxhdHRlbiB0aGUgaW1hZ2UgaW50byBhIHZlY3RvciAoMUQgYXJyYXkpXG4gIGltZ192ZWN0b3IgPC0gYXMudmVjdG9yKGltZylcbiAgXG4gICMgQ29udmVydCB0aGF0IHZlY3RvciBpbnRvIGEgc2luZ2xlIGNvbHVtbiBkYXRhZnJhbWUuXG4gIGltZ19kZiA8LSBkYXRhLmZyYW1lKHBpeGVsX2ludGVuc2l0eSA9IGltZ192ZWN0b3IpXG4gIFxuICAjIEJ1aWxkIHRoZSBwbG90XG4gIHBsb3QgPC0gZ2dwbG90KGltZ19kZiwgYWVzKHggPSBwaXhlbF9pbnRlbnNpdHksIHkgPSAxKSkgK1xuICAgIGdlb21fYm94cGxvdChmaWxsID0gJ29saXZlZHJhYicpICtcbiAgICBjb29yZF9mbGlwKCkgK1xuICAgIGxhYnMoXG4gICAgICB4ID0gJ1BpeGVsIEx1bWlub3NpdHknLFxuICAgICAgeSA9IGZpbGVfbmFtZVxuICAgICkgK1xuICAgIHRoZW1lKFxuICAgICAgcGFuZWwuYmFja2dyb3VuZCA9IGVsZW1lbnRfYmxhbmsoKSxcbiAgICAgIGF4aXMudGlja3MgPSBlbGVtZW50X2JsYW5rKCksXG4gICAgICBheGlzLnRleHQueCA9IGVsZW1lbnRfYmxhbmsoKSxcbiAgICAgIHBhbmVsLmdyaWQgPSBlbGVtZW50X2JsYW5rKCksXG4gICAgICBwYW5lbC5ncmlkLm1ham9yLnkgPSBlbGVtZW50X2xpbmUoJ2dyYXk3NScpXG4gICAgICApXG4gIFxuICBwbG90X25hbWUgPC0gcGFzdGUwKCdib3hwbG90XycsIGZpbGVfbmFtZSlcbiAgXG4gIGdnc2F2ZShmaWxlbmFtZT1wbG90X25hbWUsIHBsb3Q9cGxvdCwgcGF0aD1wYXRoLCB3aWR0aD0xLjI1LCBoZWlnaHQgPSA4KVxuICBcbiAgbWVzc2FnZShwYXN0ZShcXFBsb3Qgc2F2ZWQgZm9yOlxcLCBmaWxlX25hbWUpKVxuXG4gIFxufVxuYGBgXG5gYGAifQ== -->

```r
```r
img_into_dataframe_into_boxplot <- function(file_name, path) {
  
  # Read in the image
  img <- readJPEG(file_name)
  
  # Flatten the image into a vector (1D array)
  img_vector <- as.vector(img)
  
  # Convert that vector into a single column dataframe.
  img_df <- data.frame(pixel_intensity = img_vector)
  
  # Build the plot
  plot <- ggplot(img_df, aes(x = pixel_intensity, y = 1)) +
    geom_boxplot(fill = 'olivedrab') +
    coord_flip() +
    labs(
      x = 'Pixel Luminosity',
      y = file_name
    ) +
    theme(
      panel.background = element_blank(),
      axis.ticks = element_blank(),
      axis.text.x = element_blank(),
      panel.grid = element_blank(),
      panel.grid.major.y = element_line('gray75')
      )
  
  plot_name <- paste0('boxplot_', file_name)
  
  ggsave(filename=plot_name, plot=plot, path=path, width=1.25, height = 8)
  
  message(paste(\Plot saved for:\, file_name))

  
}
```
```

<!-- rnb-source-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuYGBgclxuIyBSdW4gaW1nX2ludG9fZGF0YWZyYW1lIGZ1bmN0aW9uIG9uIGV2ZXJ5IGZpbGUgaW4gdGhlIGZvbGRlclxuaW1nX2RmIDwtIHNhcHBseShmaWxlX25hbWVfZGYkZmlsZW5hbWUsIGltZ19pbnRvX2RhdGFmcmFtZSlcblxuYGBgXG5gYGAifQ== -->

```r
```r
# Run img_into_dataframe function on every file in the folder
img_df <- sapply(file_name_df$filename, img_into_dataframe)

```
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiRXJyb3IgaW4gRlVOKFhbW2ldXSwgLi4uKSA6IHVudXNlZCBhcmd1bWVudCAoWFtbaV1dKVxuIn0= -->

```
Error in FUN(X[[i]], ...) : unused argument (X[[i]])
```



<!-- rnb-output-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->


CURSED CHUNK OF CODE HANDLE WITH CARE

<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuYGBgclxuZmlsZW5hbWVzXG5cbmBgYFxuYGBgIn0= -->

```r
```r
filenames

```
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiIFsxXSBcXGltYWdlXzExLmpwZ1xcIFxcaW1hZ2VfMTIuanBnXFwgXFxpbWFnZV8xMy5qcGdcXCBcXGltYWdlXzE0LmpwZ1xcIFxcaW1hZ2VfMTUuanBnXFwgXFxpbWFnZV8xNi5qcGdcXCBcXGltYWdlXzE3LmpwZ1xcIFxcaW1hZ2VfMTguanBnXFwgXFxpbWFnZV8xOS5qcGdcXFxuWzEwXSBcXGltYWdlXzIuanBnXFwgIFxcaW1hZ2VfMjAuanBnXFwgXFxpbWFnZV8yMS5qcGdcXCBcXGltYWdlXzIyLmpwZ1xcIFxcaW1hZ2VfMjMuanBnXFwgXFxpbWFnZV8yNC5qcGdcXCBcXGltYWdlXzMuanBnXFwgIFxcaW1hZ2VfNC5qcGdcXCAgXFxpbWFnZV81LmpwZ1xcIFxuWzE5XSBcXGltYWdlXzYuanBnXFwgIFxcaW1hZ2VfNy5qcGdcXCAgXFxpbWFnZV84LmpwZ1xcICBcXGltYWdlXzkuanBnXFwgXG4ifQ== -->

```
 [1] \image_11.jpg\ \image_12.jpg\ \image_13.jpg\ \image_14.jpg\ \image_15.jpg\ \image_16.jpg\ \image_17.jpg\ \image_18.jpg\ \image_19.jpg\
[10] \image_2.jpg\  \image_20.jpg\ \image_21.jpg\ \image_22.jpg\ \image_23.jpg\ \image_24.jpg\ \image_3.jpg\  \image_4.jpg\  \image_5.jpg\ 
[19] \image_6.jpg\  \image_7.jpg\  \image_8.jpg\  \image_9.jpg\ 
```



<!-- rnb-output-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-plot-begin -->

<img src="data:image/png;base64,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" />

<!-- rnb-plot-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuYGBgclxuIyBUZXN0IG5ldyBpbWFnZSBvbiBvbmUgaW1hZ2VcbmltZ19pbnRvX2RhdGFmcmFtZV9pbnRvX2JveHBsb3QoZmlsZV9uYW1lPVxcaW1hZ2VfNi5qcGdcXCwgcGF0aD0nLi4vdmlfcmdidmlfYm94cGxvdHNfZ3JlZW5ob3VzZScpXG5cbmBgYFxuYGBgIn0= -->

```r
```r
# Test new image on one image
img_into_dataframe_into_boxplot(file_name=\image_6.jpg\, path='../vi_rgbvi_boxplots_greenhouse')

```
```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiUGxvdCBzYXZlZCBmb3I6IGltYWdlXzYuanBnXG4ifQ== -->

```
Plot saved for: image_6.jpg
```



<!-- rnb-output-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->




<!-- rnb-text-end -->


<!-- rnb-chunk-begin -->


<!-- rnb-source-begin eyJkYXRhIjoiYGBgclxuIyBBcHBseSBmdW5jdGlvbiB0byBhbGwgdGhlIGZpbGVzIGluIHRoYXQgbGlzdC4gR29kc3BlZWQsIGxpdHRsZSBvbmUuIFxubGFwcGx5KGZpbGVuYW1lcywgaW1nX2ludG9fZGF0YWZyYW1lX2ludG9fYm94cGxvdCwgcGF0aCA9IG91dHB1dGRpcilcblxuYGBgIn0= -->

```r
# Apply function to all the files in that list. Godspeed, little one. 
lapply(filenames, img_into_dataframe_into_boxplot, path = outputdir)

```

<!-- rnb-source-end -->

<!-- rnb-output-begin eyJkYXRhIjoiUGxvdCBzYXZlZCBmb3I6IHJlc3VsdHMvZ3JlZW5ob3VzZV9waG90b3NfdGhyZXNob2xkZWQvaW1hZ2VfMS5qcGdcbiJ9 -->

```
Plot saved for: results/greenhouse_photos_thresholded/image_1.jpg
```



<!-- rnb-output-end -->

<!-- rnb-chunk-end -->


<!-- rnb-text-begin -->



<!-- rnb-text-end -->

