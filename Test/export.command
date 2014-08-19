#!/usr/bin/env bash

echo Export Inkscape file using EzInkscape module...

INKSCAPE="/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
EZ_INKSCAPE="../ezinkscape.py"
INPUT="drawing.svg"
CLASS="Assets"
SOURCE="Output/Sources"
LANGUAGE="m" #m, cpp, cs, java
ANCHOR="top-left" #top-lef, center
TEXTURES="Output/Textures"
DPI=90

python $EZ_INKSCAPE -inkscape=$INKSCAPE -input=$INPUT -class=$CLASS -source=$SOURCE -language=$LANGUAGE -anchor=$ANCHOR -textures=$TEXTURES -dpi=$DPI

echo Done...
