# Fuel Asset Pipeline

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

Check it,

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

Run it,

```bash
source ws/install/setup.bash
# MODELS_DIR is a directory holding all the models you would like to generate thumbnails for
# OUTPUT_MODELS_DIR is an empty directory where model directories with thumbnails will reside
ros2 run fuel_asset_pipeline fuel_asset_pipeline generate_thumbnails --dir MODELS_DIR --output-dir OUTPUT_MODELS_DIR
```

## Testing

Be sure to test the final models. `gazebo` should be launched without any issues finding any asset, while no warnings or errors should pop up when the model is placed into the world using the `insert` tab.

```bash
export GAZEBO_MODEL_PATH=wip/output/; gazebo --verbose
```
