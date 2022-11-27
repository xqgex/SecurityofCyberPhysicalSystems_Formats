# Generate `.xodr` file from `.gpx` file

## Description

The following scripts will generate an [OpenDRIVE](https://www.asam.net/standards/detail/opendrive/)
`.xodr` file from a route navigation direction between two points.
The input is a [`.gpx` file](https://topografix.com/GPX) that is obtained from
[OSRM map](https://map.project-osrm.org).

## prerequisites

Install OddLOT from COVISE repository <https://github.com/hlrs-vis/covise>.

Although it is not mandatory, it is recommended as the tool will visualize the content of the
`.xodr` file on top of Google Map satellite image.

## Create the `.gpx` file

1. Run OddLOT: `source .covise.sh ; oddlot`.
2. Press on `New` and then `Load Google Map`.
3. Enter the coordinates to download, e.g.:
   | Field                              | Value                |
   | ---------------------------------- | -------------------- |
   | Location (address or coordinates): | 35.497000,-83.944306 |
   | Map Type (satellite or roadmap):   | satellite            |
   | Size (XcommaY):                    | 25,25                |

   And press `OK`.
4. Wait for the download to finish (~850MB), there is no GUI indication for the process.
5. Copy the content of the folder `/tmp/oddlot-<random_chars>/` to a non temporary location.
   The folder contains a file called `location.xml` and the folder `OddlotMapImages` with a sub
   folder that contains the satellite images, e.g.
   `./OddlotMapImages/35.497000-83.944306satellite2525/`.
6. Next step is to find the coordinates of the navigation route, in this example I'm using
   [Project OSRM](https://map.project-osrm.org) to get the `.gpx` file.
   Open the website with your browser and navigate to the desired area, e.g.
   <https://map.project-osrm.org/?z=16&center=35.497000%2C-83.944306>.
7. Drag the `start` and `end` points to create a navigation path, e.g. for this `Tail of the Dragon`
   example I am navigating from Mile #1.5 (35.483140, -83.934430) to Mile #8 (35.502830, -83.968010)
   <http://map.project-osrm.org/?z=14&loc=35.483140%2C-83.934430&loc=35.502830%2C-83.968010>.
8. Set the navigation type from `Bike` (the website default) to `Car`.
9. At the bottom left corner of the website, press the `Export GPX file` button.
10. Optional, Re-indent the file with `xmllint`, open a terminal and run the following command:
    `xmllint --output ./route_reformat.gpx --format ./route.gpx`

## Create the `.xodr` file

There are two scripts for this process:

* The first script is called `generate_xodr.py`, the script will generate an OpenDRIVE file with the
  Google Map images and the navigation route as straight lines on top of it.
* The second script is called `post_processing_xodr.py`, the script will create a new OpenDRIVE file
  from the first one, this file will be without the satellite images and the map size is cropped in
  order to comply with [CARLA simulator](https://carla.readthedocs.io/) maximum map size of 2
  kilometers.

Before running the scripts, update the global variables at the beginning of the files with the map
name, coordinates, Google Map folder path and `.gpx` file path.

To generate the OpenDrive file, simple run this scripts `python3 ./generate_xodr.py' and
`python3 ./post_processing_xodr.py'.

## Note

in my example I am focusing on the fifth mile of the `Tail of the Dragon` road
<https://google.com/search?q=tail+of+the+dragon+road>.

The XY coordinates are (35.497000, -83.944306) with OddLOT 25 by 25 grid,

Google Map link:
<https://google.com/maps/place/35%C2%B029'49.2%22N+83%C2%B056'39.5%22W/@35.497000,-83.944306,17z/>.

![Google Map](/gpx_to_xodr/markdown_images/GoogleMap.png)

![OddLOT](/gpx_to_xodr/markdown_images/ODDLOT.png)
