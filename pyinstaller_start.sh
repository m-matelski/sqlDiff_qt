#!/bin/bash

# launch script from project root directory

pyinstaller \
 --clean \
 --log-level INFO \
 --windowed \
 --noconfirm \
 --distpath build/dist \
 --workpath build/tmp \
  pyinstaller_base.spec