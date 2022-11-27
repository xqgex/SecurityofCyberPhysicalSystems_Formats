# Generate `.umap` file from `.tif` file

## Note

This is a work in progress, there might be errors or missing steps.

## Tutorial

Use `Shuttle Radar Topography Mission (SRTM GL3)` from [OpenTopography](https://opentopography.org)
https://portal.opentopography.org/raster?opentopoID=OTSRTM.042013.4326.1
https://portal.opentopography.org/raster?opentopoID=OTSRTM.082015.4326.1

Press `SELECT A REGION`at the map top left corner and choose the area to download
Validate the following:

* 2. Data Output Formats - `Select Data Output Format` is set to `GeoTiff`.
* 3. Raster Visualization - `Visualization type:` verify that `Hillshade` is not selected.

Fill the data at the `Job Description` section and press `SUBMIT`.

```
   Slope
   Aspect
   Roughness
Output format:      TIF
```

The data will be visible at the
[`Raster Job Results`](https://portal.opentopography.org/rasterJobManager) as `DEM Results`, you
will see a download link with the text `Download compressed raster results: rasters_SRTMGL3.tar.gz`.
Download and extract the file `output_SRTMGL3.tif`
Note, you might will have to edit the file and re-save it as an uncompressed `.tif` file if you will
get an error:

```
Log cleared
CL3DTio_TIFF::LoadMapFile error:
 - unsupported compression mode
CMapGroup::HF_ImportFromFile error:
 - call to LoadMapFile failed
```

At L3DT (version 16.05)
`File` -> `Import` -> `Heightfield...`
Open the `output_SRTMGL3.tif` file.

`Layers` -> `Crop` and change either the X or the Y so the image will be a square.

`Operations` -> `Heightfield` -> `Resize heightfield...`
Lock aspect ratio
Change the width to `2017`
(<https://docs.unrealengine.com/4.26/en-US/BuildingWorlds/Landscape/TechnicalGuide/#recommendedlandscapesizes>).
Press `OK`
`Do you want to retain the same physical map size?`
Select `Yes`

To get the horizontal and vertical scale of the heightfield:
`Operations` -> `Heightfield` -> `Change horizontal scale...`
Remember the value of `grid-spacing (m)` 0.064452
`Operations` -> `Heightfield` -> `Change vertical range...`
Remember the value of `Altitude range (m)` 394.93

To export the layer
`File` -> `Export` -> `Export active map layer...`
Browse at the `File name` field and give the file a name, e.g. `TailOfTheDragon.hfz`.
Press `OK`

`File` -> `Close` -> `Close project` and don't save the project.

Open GIMP
Choose `File` -> `New...` and expand the `Advanced Options` menu.
Width and Height in pixels are the sizes of the L3DT heightfield (`2017`).
Lower the X and Y resolution to 72 pixels/in
Color space should be set to `Grayscale` with a precision of `8-bit integer`.
Fill the image with black color and export it as a `.png` image.

Back to L3DT
`File` -> `Import` -> `Heightfield...`
Open the black `.png` image, `Next > >`, for the horizontal scale write the number we measured
earlier and press `OK`.

`File` -> `Import` -> `Merge heightmaps`
Open the `.hfz` file that we have created earlier.
Disable `Strech to fit` and press `OK`

Now its time to export the file to something Unreal Engine can read.
Create an empty directory that the files will be exported to.
At L3DT select
`File` -> `Export` -> `Export overlapped tiles`
Browse to the empty directory, enter the map file name and select `Save`.
Change the file type to `R16` and the tile size to `2017`.
Check the checkbox of `Format file names for Unreal` and click `OK`.

Open CARLA Unreal Engine project file `CarlaUE4.uproject`.
Open one of CARLA towns as a base.
Select `Window` -> `World Settings` and check the checkbox of `Enable World Composition`.

`Window` -> `Levels`
In the new window, press on `Levels` -> `Import Tiled Landscape...`
In the new window, press on `Select Heightmap Tiles...` and choose the file that was exported from
L3DT.
Unselect the checkbox `Flip Tile Y Coordinate`.
Multiply the L3DT value of `Altitude range (m)` by 0.1953125 and write the results as the Z value
of `Landscape Scale`.
Press `Import`.
