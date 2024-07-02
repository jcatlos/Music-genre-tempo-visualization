# Music tempo vizualization
Explore the tempo of different genres. See how they look in comparison. Here are all music genres from the [FMA dataset](https://github.com/mdeff/fma/tree/master).

![vizualization_loop](viz-loop.gif | width=200)


## Drill-down into the data
Click on a genre from thi inner circle to zoom in. click into the centre to zoom out.

![vzooming_in_and_out](drill-down.gif | width=200)

## About
All you need to explore the data yourself is to download the `songs.html` file and open it in your browser.

The visualization is done using [d3.js](https://d3js.org/). It was done by using [this template](https://observablehq.com/@d3/zoomable-sunburst) as a beseline.


## Documentation
The visualization runs solely from the `songs.html` file. It downloads the file `genre_data.json` from a *Github gist*. The file `genre_data.json` is in the repo only for demonstration - editing it will not result in any change of the visualization.

The `genre_data.json` is created by the script `data_prep.py`. It requires files `data/echonest.csv`, `data/genres.csv` and `data/tracks.csv` (files `echonest.csv`, `genres.csv` and `tracks.csv` from the [FMA dataset](https://github.com/mdeff/fma/tree/master), all placed into a folder `data`). 
