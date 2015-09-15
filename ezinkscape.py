## @package EzInkscape
# GUI/Level editor for InkScape
# and more...
# Author: Thanh Vinh<thanh.vinh@hotmail.com>

import argparse
import subprocess
import sys
import time
from xml.etree import ElementTree

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
INKSCAPE_NAMESPACE = 'http://www.inkscape.org/namespaces/inkscape'

LANGUAGE_OBJECTIVE_C = 'm'
LANGUAGE_CPP = 'cpp'
LANGUAGE_CS = 'cs'
LANGUAGE_JAVA = 'java'

QUERY_POSITION = 'position'
QUERY_SIZE = 'size'
QUERY_ALL = 'all'

ANCHOR_CENTER = 'center'
ANCHOR_TOP_LEFT = 'top-left'

DEFAULT_DPI = 90

##
# Format source code.
#
class Source:
    @staticmethod
    def getheaderfileheader(classname, language):
        classinterface = ''
        if language == LANGUAGE_OBJECTIVE_C:
            classinterface = '@interface {0} : NSObject'.format(classname)
        elif language == LANGUAGE_CPP:
            classinterface = 'public class {0} \n{{\npubic:\n'.format(classname)
        else:
            classinterface = 'public class {0} \n{{'.format(classname)

        header = (
            '//\n'
            '// Generate by EzInkscape\n'
            '// Language: {0}\n'
            '// Date: {1}\n'
            '//\n\n'
            '{2}\n\n'
        ).format(language, time.strftime('%d/%m/%Y %H:%M:%S'), classinterface)

        return header

    @staticmethod
    def getheaderfooter(language):
        if language == LANGUAGE_OBJECTIVE_C:
            return '@end\n'
        else:
            return '}\n'

    @staticmethod
    def getsourcefileheader(classname, language):
        importfile = ''
        if language == LANGUAGE_OBJECTIVE_C:
            importfile = '#import "{0}.h"'.format(classname)
        elif language == LANGUAGE_CPP:
            importfile = '#include "{0}.h"'.format(classname)

        classinterface = ''
        if language == LANGUAGE_OBJECTIVE_C:
            classinterface = '@implementation {0}\n'.format(classname)
        elif language == LANGUAGE_CS or language == LANGUAGE_JAVA:
            classinterface = 'public class {0} \n{{'.format(classname)

        header = (
            '//\n'
            '// Generate by EzInkscape\n'
            '// Language: {0}\n'
            '// Date: {1}\n'
            '//\n\n'
            '{2}\n\n'
            '{3}\n\n'
        ).format(language, time.strftime('%d/%m/%Y %H:%M:%S'), importfile, classinterface)

        return header

    @staticmethod
    def getsourcefooter(language):
        if language == LANGUAGE_OBJECTIVE_C:
            return '@end\n'
        elif language == LANGUAGE_CPP:
            return '\n'
        else:
            return '}\n'

    @staticmethod
    def getextern(typename, variable, language):
        if language == LANGUAGE_OBJECTIVE_C:
            return 'extern const {0} {1};'.format(typename, variable)
        elif language == LANGUAGE_CPP:
            return '\textern const {0} {1};'.format(typename, variable)
        else:
            return 'Only support languages: objective-c, cpp.'

    @staticmethod
    def getexternstringconstant(variable, language):
        if language == LANGUAGE_OBJECTIVE_C:
            return Source.getextern('NSString', '*{0}'.format(variable), language)
        elif language == LANGUAGE_CPP:
            return Source.getextern('char*', variable, language)
        elif language == LANGUAGE_CS:
            return Source.getextern('string', variable, language)
        elif language == LANGUAGE_JAVA:
            return Source.getextern('String', variable, language)

    @staticmethod
    def getexternfloatconstant(variable, language):
        return Source.getextern('float', variable, language)

    @staticmethod
    def getsource(typename, variable, value, language):
        if language == LANGUAGE_OBJECTIVE_C:
            return 'const {0} {1} = {2};'.format(typename, variable, value)
        elif language == LANGUAGE_CPP:
            return 'const {0} {1} = {2};'.format(typename, variable, value)
        elif language == LANGUAGE_CS:
            return '\tpublic const {0} {1} = {2};'.format(typename, variable, value)
        elif language == LANGUAGE_JAVA:
            return '\tpublic static {0} {1} = {2};'.format(typename, variable, value)
        else:
            return 'Only support languages: objective-c, cpp, cs, java.'

    @staticmethod
    def getstringconstant(variable, value, language):
        if language == LANGUAGE_OBJECTIVE_C:
            return Source.getsource('NSString', '*{0}'.format(variable), '@{0}'.format(value), language)
        elif language == LANGUAGE_CPP:
            return Source.getsource('char*', variable, value, language)
        elif language == LANGUAGE_CS:
            return Source.getsource('string', variable,  value, language)
        elif language == LANGUAGE_JAVA:
            return Source.getsource('String', variable,  value, language)

    @staticmethod
    def getfloatconstant(variable, value, language):
        return Source.getsource('float', variable, '{0}f'.format(value), language)

class Element:
    _svg = None
    _query = ''
    _id = ''
    _x = 0
    _y = 0
    _width = 0
    _height = 0

    ##
    # Format data like: svg2,177.14285,223.79076,285.71428,314.28571
    # store in a line of query info
    #
    def __init__(self, svg, query):
        self._svg = svg
        self._query = query
        attributes = query.split(',')
        self._id = attributes[0]
        self._x = attributes[1]
        self._y = attributes[2]
        self._width = attributes[3]
        self._height = attributes[4]

    def getquery(self):
        return self._query

    def getid(self):
        return self._id;

    def getx(self):
          return self._x;

    def gety(self):
          return self._y;

    def getwidth(self):
          return self._width;

    def getheight(self):
          return self._height;

    def getname(self):
        name = 'k{0}'.format(self._id)
        name = name.replace(' ', '_')
        return name;

    def getheader(self, language, query):
        if language == LANGUAGE_OBJECTIVE_C or language == LANGUAGE_CPP:
            name = self.getname()
            texture = Source.getexternstringconstant(name, language)
            x = Source.getexternfloatconstant('{0}_X'.format(name), language)
            y = Source.getexternfloatconstant('{0}_Y'.format(name), language)
            width = Source.getexternfloatconstant('{0}_W'.format(name), language)
            height = Source.getexternfloatconstant('{0}_H'.format(name), language)
            source = ''

            if (query == QUERY_ALL):
                source = '{0}\n{1}\n{2}\n{3}\n{4}\n\n'.format(texture, x, y, width, height)
            elif (query == QUERY_POSITION):
                source = '{0}\n{1}\n{2}\n\n'.format(texture, x, y)
            elif (query == QUERY_SIZE):
                source = '{0}\n{1}\n{2}\n\n'.format(texture, width, height)

            return source
        else:
            return None

    ##
    # Generate source code.
    #
    def getsource(self, language, query):
        # Change position base on anchor
        name = self.getname()
        x = self._x
        y = float(self._svg.getheight()) - float(self._y)
        if self._svg.getanchor() == 'center':
            x = float(x) + (float(self._width) / 2)
            y = float(y) - (float(self._height) / 2)

        # Source
        texture = Source.getstringconstant(name, '"{0}.png"'.format(self._id), language)
        x = Source.getfloatconstant('{0}_X'.format(name), x, language)
        y = Source.getfloatconstant('{0}_Y'.format(name), y, language)
        width = Source.getfloatconstant('{0}_W'.format(name), self._width, language)
        height = Source.getfloatconstant('{0}_H'.format(name), self._height, language)
        source = ''

        if (query == QUERY_ALL):
            source = '{0}\n{1}\n{2}\n{3}\n{4}\n\n'.format(texture, x, y, width, height)
        elif (query == QUERY_POSITION):
            source = '{0}\n{1}\n{2}\n\n'.format(texture, x, y)
        elif (query == QUERY_SIZE):
            source = '{0}\n{1}\n{2}\n\n'.format(texture, width, height)

        return source

    def __str__(self):
        return self._id

##
# Present a layer in SVG file.
#
class Layer:
    _svg = None
    _name = ''          #layer name
    _x = 0
    _y = 0
    _elements = list()  #objects

    def __init__(self, svg, layer):
        # Init
        self._svg = svg
        self._name = layer.get('{%s}label' % INKSCAPE_NAMESPACE)
        id = layer.get('id')
        element = self._svg.getelement(id)
        self._x = element.getx()
        self._y = element.gety()

        # TODO support sub-layers + sub-groups
        # Elements
        print(' - Parsing layer: {0}'.format(self._name))
        self._elements = list() #should be initialized here for instances
        for node in layer:
            id = node.get('id')
            print('  + Found element: {0}'.format(id))
            element = self._svg.getelement(id)
            self._elements.append(element)

    ##
    # Get an element of this layer.
    #
    def getelements(self):
        return self._elements;

    def getname(self):
        name = 'k{0}'.format(self._name)
        name = name.replace(' ', '_')
        return name;

    def __str__(self):
        return self._name

class SVG:
    _inkscape = ''
    _filename = ''
    _width = 0
    _height = 0
    _anchor = 'center'
    _layers = []            # list of Layers
    _elements = []          #all elements from query command

    def __init__(self, inkscape, filename, anchor):
        self._filename = filename
        self._inkscape = inkscape
        self._anchor = anchor
        self._layers = []   #should be initialized here for instances
        self._queryall()
        self._parse()

    ##
    # Query all objects
    #
    def _queryall(self):
        # Query all objects using inkscape command line
        popen = subprocess.Popen([self._inkscape, self._filename, '--query-all'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        query, error = popen.communicate()
        popen.wait()

        # Parse that query
        elements = query.splitlines()
        print error
        for line in elements:
            element = Element(self, line)
            self._elements.append(element)

    ##
    # TODO Parse svg file for support layer.
    #
    def _parse(self):
        print('Parse SVG file: {0}...'.format(self._filename))
        tree = ElementTree.parse(self._filename)
        root = tree.getroot()
        self._width = root.get('width')
        self._height = root.get('height')
        print('********************{0}'.format(self._height))

        for node in root.findall('{%s}g' % SVG_NAMESPACE):
            layer = Layer(self, node)
            self._layers.append(layer)

    def getwidth(self):
        return self._width

    def getheight(self):
        return self._height

    def getanchor(self):
        return self._anchor

    def getelement(self, id):
        for element in self._elements:
            if id == element.getid():
                return element

    def exportsource(self, classname, sourcepath, language, query):
        print('Export source...')
        # Header
        if language == 'm' or language == 'cpp':
            headerfile = '{0}/{1}.h'.format(sourcepath, classname)
            print('Header file: {0}'.format(headerfile))

            f = open(headerfile, 'w')
            f.write(Source.getheaderfileheader(classname, language))

            # Extern values
            for layer in self._layers:
                print(' - Layer {0}'.format(layer))
                f.write('// {0}\n'.format(layer))
                for element in layer.getelements():
                    print('  + Element: {0}'.format(element))
                    f.write(element.getheader(language, query))

            f.write(Source.getheaderfooter(language))
            f.close()

        # Source
        sourcefile = '{0}/{1}.{2}'.format(sourcepath, classname, language)
        print('Source file: {0}'.format(sourcefile))

        f = open(sourcefile, 'w')
        f.write(Source.getsourcefileheader(classname, language))

        for layer in self._layers:
            print(' - Layer {0}'.format(layer))
            f.write('// {0}\n'.format(layer))
            for element in layer.getelements():
                print('  + Element: {0}'.format(element))
                f.write(element.getsource(language, query))

        f.write(Source.getsourcefooter(language))
        f.close()
        print('Done.')

    ##
    # Export all elements, except elements sub-elements.
    #
    def exporttexures(self, outputpath, dpi):
        print('Export textures, saved in: {0}...'.format(outputpath))
        for layer in self._layers:
            print(' - Layer {0}'.format(layer))
            for element in layer.getelements():
                print('  + Element: {0}'.format(element))
                id = element.getid()
                popen = subprocess.Popen(
                    [
                        self._inkscape, '--file={0}'.format(self._filename),
                        '--export-id-only',
                        '--export-id={0}'.format(id),
                        '--export-dpi={0}'.format(dpi),
                        '--export-png={0}/{1}.png'.format(outputpath, id)
                    ],
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE
                )
                query, error = popen.communicate()
                # print(query)

def main(argv):
    # # InkScape command location
    # inkscape = "inkscape"
    # if (platform.system() == "Windows"):
    #     inkscape = "D:\Softwares\InkscapePortable\App\Inkscape\inkscape.exe"
    # else:
    #     inkscape = "/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
    #

    # Args information
    parser = argparse.ArgumentParser(
        description = 'EzSVG, export Inkscape file easy.',
    )
    parser.add_argument('-inkscape', help = 'Inkscape execute path', required = True)
    parser.add_argument('-input', help = 'Inkscape input file', required = True)
    parser.add_argument('-class', help = 'class name', default = 'Assets')
    parser.add_argument('-source', help = 'source path', default = None)
    parser.add_argument('-language',
        help = 'source language, support Objective C (m), C++ (cpp), C# (cs) and Java (java)',
        default = LANGUAGE_OBJECTIVE_C
    )
    parser.add_argument('-anchor', help = 'anchor: center or top-left', default = ANCHOR_CENTER)
    parser.add_argument('-query',
        help = 'query information, {0}, {1} or {2}'.format(QUERY_POSITION, QUERY_SIZE, QUERY_ALL),
        default = QUERY_POSITION
    )
    parser.add_argument('-textures', help = 'textures output path', default = None)
    parser.add_argument('-dpi', help = 'DPI, default 90', type = int, default = DEFAULT_DPI)
    args = vars(parser.parse_args(argv))

    # Parse args
    # TODO source: input class name, and path then generate both .h & .m files
    inkscape = args['inkscape']
    inputfile = args['input']
    classname = args['class']
    sourcepath = args['source']
    language = args['language']
    anchor = args['anchor']
    query = args['query']
    texturespath = args['textures']
    dpi = args['dpi']

    # SVG
    svg = SVG(inkscape, inputfile, anchor)
    if sourcepath is not None:
        svg.exportsource(classname, sourcepath, language, query)
    if texturespath is not None:
        svg.exporttexures(texturespath, dpi)

if __name__ == '__main__':
    main(sys.argv[1:])
