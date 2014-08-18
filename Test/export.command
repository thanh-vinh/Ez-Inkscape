#!/usr/bin/env bash

echo Export Inkscape file using EzInkscape module...

INKSCAPE="/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
EZ_INKSCAPE="../ezinkscape.py"
INPUT="drawing.svg"
SOURCE="Output/Sources/Drawing.h"
LANGUAGE="objective-c"
TEXTURES="Output/Textures"
DPI=90

python $EZ_INKSCAPE -inkscape=$INKSCAPE -input=$INPUT -source=$SOURCE -language=$LANGUAGE -textures=$TEXTURES -dpi=$DPI

echo Done...



