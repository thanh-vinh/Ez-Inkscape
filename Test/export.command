#!/usr/bin/env bash

echo Export Inkscape file using EzInkscape module...

INKSCAPE="/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
EZ_INKSCAPE="../ezinkscape.py"
INPUT="drawing.svg"
CLASS="Assets"
SOURCE="Output/Sources"
LANGUAGE="m" #m, cpp, cs, java
ANCHOR="center" #top-lef, center
QUERY="xy" #xy, size, all
TEXTURES="Output/Textures"
DPI=90

python $EZ_INKSCAPE -inkscape=$INKSCAPE -input=$INPUT -class=$CLASS -source=$SOURCE -language=$LANGUAGE -anchor=$ANCHOR -query=$QUERY -textures=$TEXTURES -dpi=$DPI

echo Done...
