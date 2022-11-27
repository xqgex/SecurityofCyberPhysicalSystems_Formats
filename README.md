# ECE 591 (004) Fall 2022 project

## Background

The goal of the project was to generate a map for CARLA, a simulator for autonomous driving research
using open source tools and scripts.

As an example, I choose to create a map from the
[Tail of the Dragon](https://en.wikipedia.org/wiki/Deals_Gap,_North_Carolina) (Deals Gap) road.

## Introduction

The process was tested on:

* [Ubuntu 20.04](https://releases.ubuntu.com/20.04/)
* Python 3.8.10
* [Unreal Engine 4.22](https://github.com/EpicGames/UnrealEngine/tree/4.22.0-release)
* [CARLA 0.9.8](https://carla.readthedocs.io/en/0.9.8/start_quickstart/#downloading-carla)
* [COVISE](https://github.com/hlrs-vis/covise)

Files extensions that will be used in the process:

* `.umap`: An Unreal Engine map that was created with the Unreal Engine Editor.
* `.fbx`: Autodesk Filmbox, a file that contains the geometry of the map.
* `.xodr`: OpenDRIVE, a file that contains the traffic description.
* `.obj`: Map geometry, required in order to generate the `.bin` file.
* `.bin`: Pedestrian navigation, description where the pedestrians can walk and where they can't.
* `.json`: File that contains the description of the package maps.

## Work procedure

### Step 1

Note, see the [GPX to XODR tutorial](/gpx_to_xodr/).

Choose package name (e.g. `package_tail_of_the_dragon`) and map name (e.g. `TailOfTheDragon`).
Create directory for the map at the import directory using the following command:
`mkdir --parents /<your_local_path>/carla-simulator/Import/<package_name>/<map_name>/`
Copy `<map_name>.xodr` and `<map_name>.fbx` files to
`/<your_local_path>/carla-simulator/Import/<package_name>/<map_name>/`.
Create a `.json` file for the package, execute the following command (don't forget to update the
command with the chosen package name and map name):
`echo -e '{\n  "maps": [\n    {\n      "name": "<map_name>",\n      "source": "./<map_name>/<map_name>.fbx",\n      "use_carla_materials": true,\n      "xodr": "./<map_name>/<map_name>.xodr"\n    }\n  ],\n  "props": [\n  ]\n}' >> /<your_local_path>/carla-simulator/Import/<package_name>/<package_name>.json`
Now it is possible to import the new map into Carla, execute the following command:
`make -C /<your_local_path>/carla-simulator/ import ARGS="--packages=<package_name>"`.
Note, during the execution of the command, there are about 30 minutes without any visual feedback,
the only feedback that you have that the command is still running is the CPU usage, be patient and
wait for the command finish.
After the command will finish, there will be a new package directory at:
`/<your_local_path>/carla-simulator/Unreal/CarlaUE4/Content/<package_name>/`.

### Step 2

Note, see the [TIF to UMAP tutorial](/tif_to_umap/).

In this step we will use Epic Games Unreal Engine Editor software to import a `.umap` file and then
export it as a `.obj` file.
Open Unreal Editor by execute the following command:
`make -C /<your_local_path>/carla-simulator/ launch-only`.
Import the map using the upper menu `File`->`Open Level` (`Ctrl+O`) and choose the new map.
e.g. `/Content/package_tail_of_the_dragon/Maps/TailOfTheDragon/TailOfTheDragon.umap`.
Export the map using the upper menu `File`->`Carla Exporter` (`Actors` category).
Note, the export process can take about 40 minutes, be patient.
Once the export process will finish, there will be a new file called `<map_name>.obj` at
`/<your_local_path>/carla-simulator/Unreal/CarlaUE4/Saved/`.
Keep the Unreal Editor open (will be use it again at step 4).

### Step 3

In this step, we will create a `.bin` file from `.xodr` and `.obj` files, this step is necessary
only for maps that support pedestrians (have sidewalks).
Copy both `.xodr` and `.obj` files to `/<your_local_path>/carla-simulator/Util/DockerUtils/dist/`,
execute the following commands:
`cp /<your_local_path>/carla-simulator/Unreal/CarlaUE4/Content/<package_name>/Maps/<map_name>/OpenDrive/<map_name>.xodr /<your_local_path>/carla-simulator/Util/DockerUtils/dist/`
`cp /<your_local_path>/carla-simulator/Unreal/CarlaUE4/Saved/<map_name>.obj /<your_local_path>/carla-simulator/Util/DockerUtils/dist/`
Create the `.bin`, execute the following command:
`/<your_local_path>/carla-simulator/Util/DockerUtils/dist/build.sh <man_name>` (pay attention not to
add the file extension), e.g. `./build.sh TailOfTheDragon`.
Copy the `.bin` file that was generated (at the Docker utils `./dist/` directory) to the content
`./Nav/` folder, e.g.
`cp /<your_local_path>/carla-simulator/Util/DockerUtils/dist/<man_name>.bin /<your_local_path>/carla-simulator/Unreal/CarlaUE4/Content/package_tail_of_the_dragon/Maps/TailOfTheDragon/Nav/`.

### Step 4

Run the simulation from the Unreal Editor using the play icon at the top of the software (`Alt+P`).
Test the process by generating traffic, execute the following command:
`/<your_local_path>/carla-simulator/PythonAPI/examples/spawn_npc.py`.

### Step 5

Generate a stand alone package, execute the following command:
`make -C /<your_local_path>/carla-simulator/ package ARGS="--packages=<package_name>"`.
The new package tarball will be created at:
`/<your_local_path>/carla-simulator/Dist/<package_name>_0.9.8-dirty.tar.gz`.
Copy the package to `/opt/carla-simulator/Import` and run the import assets script:
`sudo cp /<your_local_path>/carla-simulator/Dist/<package_name>_0.9.8-dirty.tar.gz /opt/carla-simulator/Import/`
`cd /opt/carla-simulator/`
`sudo ./ImportAssets.sh`

### Step 6

Finally it is time to run the server and the client.
Open two terminals, at the first one, start the server using the command
`DRI_PRIME=1 sh /opt/carla-simulator/bin/CarlaUE4.sh -prefernvidia`.
At the second terminal, execute the following commands:
`export PYTHONPATH=$PYTHONPATH:/opt/carla-simulator/PythonAPI/carla/dist/carla-0.9.8-py3.5-linux-x86_64.egg`
`python /opt/carla-simulator/PythonAPI/util/config.py -m <map_name>`
`python /opt/carla-simulator/PythonAPI/examples/manual_control.py`
:tada:
