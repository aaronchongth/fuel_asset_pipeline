#!/bin/bash

. /usr/share/gazebo/setup.sh

function generate_thumbnails {
  # $1 folder of models
  # $2 output folder for zips

  INPUT="$(realpath $1)"
  OUTPUT="$(realpath $2)"

  . /usr/share/gazebo/setup.sh
  export GAZEBO_MODEL_PATH=$INPUT

  pushd $OUTPUT > /dev/null

  for d in $INPUT/* ; do
    gzprop $d/model.sdf
  done

  popd > /dev/null
}

function unzip_rename_thumbnails {
  # $1 folder of zips
  # $2 output folder for models with renamed thumbnail folders
  
  INPUT="$(realpath $1)"
  OUTPUT="$(realpath $2)"

  for d in $INPUT/* ; do
    fbname=$(basename "$d" .zip)
    OUTPUT_MODEL_DIR=$OUTPUT/$fbname
    unzip $d -d $OUTPUT_MODEL_DIR
    mv $OUTPUT_MODEL_DIR/meta $OUTPUT_MODEL_DIR/thumbnails
  done
}