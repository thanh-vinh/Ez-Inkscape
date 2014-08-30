Ez-Inkscape
===========

Ez-Inkscape is a simple Python module for helper the developers who using Inkscape for design their games/and or applications.

Features
===========

* Export all elements of a SVG file to PNG format.
* Query all elements information:
	- Position.
	- Size.
* Generate source code for multiple languages: C++, Objective C, C# and Java.

Requirement
===========

* OSX, Linux or Windows system.
* Python >=2.7.
* InkScape.

Prepare Inkscape file
===========
TBD

How to use
===========

Usage: ```ezinkscape.py [-h] -inkscape INKSCAPE -input INPUT [-class CLASS]
                     [-source SOURCE] [-language LANGUAGE] [-anchor ANCHOR]
                     [-query QUERY] [-textures TEXTURES] [-dpi DPI]```

optional arguments:

```
  -h, --help          show this help message and exit
  -inkscape INKSCAPE  Inkscape execute path
  -input INPUT        Inkscape input file
  -class CLASS        class name
  -source SOURCE      source path
  -language LANGUAGE  source language
  -anchor ANCHOR      anchor: center or top-left
  -query QUERY        query information, position, size or all
  -textures TEXTURES  textures output path
  -dpi DPI            DPI, default 90
```
 
Example
===========
TBD 