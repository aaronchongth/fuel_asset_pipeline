# Fuel Asset Pipeline

This package contains tools to help with the process of uploading models onto [Ignition Fuel](https://app.ignitionrobotics.org/).

## Prerequisites

```bash
pip3 install \
  colcon-common-extensions \
  progressbar2
```

and Gazebo classic.

## Instructions

Clone it,

```bash
mkdir ws/src
cd ws/src
git clone https://github.com/aaronchongth/fuel-asset-pipeline
```

Build it,

```bash
cd ws
source /opt/ros/foxy/setup.bash
colcon build
```

Grab the models,

```bash
source ws/install/setup.bash
# 
ros2 run fuel_asset_pipeline fuel_asset_pipeline copy_with_ref \
  --ref REFERENCE_ASSETS_DIR \ # Directory that you would like to mimic
  --source SOURCE_ASSETS_DIR \ # Directory that holds all the assets you would like to copy from and more
  --dest DESTINATION_TO_COPY_TO \ # Destination directory to copy to
  --folders-only \ # Only copy folders
  --ignore MODELS_TO_IGNORE
```

Check them all,

```bash
source ws/install/setup.bash
# MODELS_DIR is a directory holding all the models you would like to check
ros2 run fuel_asset_pipeline fuel_asset_pipeline check_all --dir MODELS_DIR
```

Or check one,

```bash
source ws/install/setup.bash
# MODEL_DIR is a single model directory
ros2 run fuel_asset_pipeline fuel_asset_pipeline check --model-dir MODEL_DIR
```

Generate the thumbnails,

```bash
source ws/install/setup.bash
# MODELS_DIR is a directory holding all the models you would like to generate thumbnails for
# OUTPUT_MODELS_DIR is an empty directory where model directories with thumbnails will reside
ros2 run fuel_asset_pipeline fuel_asset_pipeline generate_thumbnails --dir MODELS_DIR --output-dir OUTPUT_MODELS_DIR
```

Upload all (highly unstable for now),

```bash
source ws/install/setup.bash
# MODELS_DIR is a directory holding all the models you would like to upload
# PRIVATE_TOKEN see below on how to generate one
# OWNER optional, if provided will upload under an organization that you are part of
# URL optional, url to fuel
ros2 run fuel_asset_pipeline fuel_asset_pipeline upload_all --dir MODELS_DIR --token PRIVATE_TOKEN --owner OWNER --url URL
```

Upload one (highly unstable for now),

```bash
source ws/install/setup.bash
# MODEL_DIR is a single model directory
# PRIVATE_TOKEN see below on how to generate one
# OWNER optional, if provided will upload under an organization that you are part of
# URL optional, url to fuel
ros2 run fuel_asset_pipeline fuel_asset_pipeline upload --model-dir MODEL_DIR --token PRIVATE_TOKEN --owner OWNER --url URL
```

## Testing

Be sure to test the final models. `gazebo` should be launched without any issues finding any asset, while no warnings or errors should pop up when the model is placed into the world using the `insert` tab.

```bash
export GAZEBO_MODEL_PATH=wip/output/; gazebo --verbose
```

## Ignition Fuel Private Token

Get the prefix and key using a POST request,

```bash
# USERNAME username after logging in
# JWT_TOKEN can be retrieved in browser console, localStorage.id_token, after logging in to Fuel
# NAME any name you choose
curl --request POST   --url https://fuel.ignitionrobotics.org/1.0/users/USERNAME/access-tokens   --header 'Authorization: Bearer JWT_TOKEN' --header 'Content-Type: application/json'   --data '{ "name": "NAME" }'
```

It will return

```bash
{"name":"NAME","prefix":"PREFIX","key":"KEY"}
```

The private token's value will be `PREFIX.KEY`.

## Next up

* Tool to check diff between two sources
* Refer more to https://github.com/luca-della-vedova/gazebo_asset_checker/blob/master/asset_checker.py, for colorful printouts
* Checking texture names
* Checking allowed extension types, refer to Ignition Fuel
* Upload onto Fuel using `ign-fuel-tools`
