#!/bin/bash
# Automation script for compiling *.ui files from QtDesigner into *.py files
# Params: root project directory, ui directory, output compiled python files directory
# Example sh pyuic_compile_design.sh . design ui

project_root=$1
ui_dir=$2
py_dir=$3
root_ui="$project_root/$ui_dir"
root_py="$project_root/$py_dir"

find "$root_ui" -type f -name "*.ui" | while read line; do
  echo "Processing file '$line'"
  current_file=${line#"$root_ui"}
  current_py_dir="$(dirname "$root_py$current_file")"
  current_py_filepath="$current_py_dir/ui_$(basename -s .ui "$current_file").py"
  mkdir -p "$current_py_dir"
  touch "$current_py_filepath"
  touch "$current_py_dir/__init__.py"
  pyuic5 "$line" -o "$current_py_filepath" --resource-suffix=_rc --import-from=.
done

# Compile resource file "resources.qrc" if exists
pyrcc5 "${root_ui}/resources.qrc" -o "${root_py}/resources_rc.py"
