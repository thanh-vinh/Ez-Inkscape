@echo off

echo Export Inkscape file using EzInkscape module...

set INKSCAPE="/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
set EZ_INKSCAPE="../ezinkscape.py"
set INPUT="drawing.svg"
set SOURCE="Output/Sources/Drawing.h"
set LANGUAGE="objective-c"
set TEXTURES="Output/Textures"
set DPI=90

python %EZ_INKSCAPE% -inkscape=%INKSCAPE% -input=%INPUT% -source=%SOURCE% -language=%LANGUAGE% -textures=%TEXTURES% -dpi=%DPI%

echo Done...
