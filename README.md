# Fuel Asset Pipeline

## Instructions

Fix models and place them in a dierctory, assuming it is called `MODEL_DIR`.

```bash
# Setup
git clone https://github.com/aaronchongth/fuel_asset_pipeline
cd fuel_asset_pipeline
source scripts/setup.bash

# Create the necessary temporary directories
mkdir -p wip/zips
mkdir -p wip/output

# Create thumbnails for each of the models in MODEL_DIR
# the outputs are zips
generate_thumbnails MODEL_DIR wip/zips/

# Unzip each model, and rename the thumbnail folders
unzip_rename_thumbnails wip/zips/ wip/output/
```

## Testing

Be sure to test the final models. `gazebo` should be launched without any issues finding any asset, while no warnings or errors should pop up when the model is placed into the world using the `insert` tab.

```bash
export GAZEBO_MODEL_PATH=wip/output/; gazebo --verbose
```
