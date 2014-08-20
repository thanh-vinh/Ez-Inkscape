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

##
# Format source code.
#
class Source:
    @staticmethod
    def getheaderfileheader(classname, language):
        classinterface = ''
        if language == 'm':
            classinterface = '@interface {0} : NSObject'.format(classname)
        elif language == 'cpp':
            classinterface = 'public class {0} {{\npubic:\n'.format(classname)
        else:
            classinterface = 'public class {0} {{\n'.format(classname)
        
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
        if language == 'm':
            return '@end\n'
        else:
            return '}\n'
    
    @staticmethod
    def getsourcefileheader(classname, language):
        importfile = ''
        if language == 'm':
            importfile = '#import "{0}.h"'.format(classname)
        elif language == 'cpp':
            importfile = '#include "{0}.h"'.format(classname)
        
        classinterface = ''
        if language == 'm':
            classinterface = '@implementation {0}\n'.format(classname)
        elif language == 'cs' or language == 'java':
            classinterface = 'public class {0} {{\n'.format(classname)
        
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
        if language == 'm':
            return '@end\n'
        elif language == 'cpp':
            return '\n'
        else:
            return '}\n'
    
    @staticmethod
    def getextern(typename, variable, language):
        if language == 'm':
            return 'extern const {0} {1};'.format(typename, variable)
        elif language == 'cpp':
            return '\textern const {0} {1};'.format(typename, variable)
        else:
            return 'Only support languages: objective-c, cpp.'
    
    @staticmethod
    def getexternstringconstant(variable, language):
        if language == 'm':
            return Source.getextern('NSString', '*{0}'.format(variable), language)
        elif language == 'cpp':
            return Source.getextern('char*', variable, language)
        elif language == 'cs':
            return Source.getextern('string', variable, language)
        elif language == 'java':
            return Source.getextern('String', variable, language)
    
    @staticmethod
    def getexternfloatconstant(variable, language):
        return Source.getextern('float', variable, language)
    
    @staticmethod
    def getsource(typename, variable, value, language):
        if language == 'm':
            return 'const {0} {1} = {2};'.format(typename, variable, value)
        elif language == 'cpp':
            return 'const {0} {1} = {2};'.format(typename, variable, value)
        elif language == 'cs':
            return '\tpublic const {0} {1} = {2};'.format(typename, variable, value)
        elif language == 'java':
            return '\tpublic static {0} {1} = {2};'.format(typename, variable, value)
        else:
            return 'Only support languages: objective-c, cpp, cs, java.'
    
    @staticmethod
    def getstringconstant(variable, value, language):
        if language == 'm':
            return Source.getsource('NSString', '*{0}'.format(variable), '@{0}'.format(value), language)
        elif language == 'cpp':
            return Source.getsource('char*', variable, value, language)
        elif language == 'cs':
            return Source.getsource('string', variable,  value, language)
        elif language == 'java':
            return Source.getsource('String', variable,  value, language)
    
    @staticmethod
    def getfloatconstant(variable, value, language):
        return Source.getsource('float', variable, value, language)

class Element:
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
    def __init__(self, query):
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
        name = 'k%s' % self._id;
        name = name.replace(' ', '_')
        return name;
    
    def getheader(self, language):
        if language == 'm' or language == 'cpp':
            name = self.getname()
            source = '{0}\n{1}\n{2}\n{3}\n{4}\n\n'.format(
                Source.getexternstringconstant(name, language),
                Source.getexternfloatconstant('{0}_X'.format(name), language),
                Source.getexternfloatconstant('{0}_Y'.format(name), language),
                Source.getexternfloatconstant('{0}_W'.format(name), language),
                Source.getexternfloatconstant('{0}_H'.format(name), language)
            )
            
            return source
        else:
            return None
    
    ##
    # Generate source code.
    #
    def getsource(self, language, anchor):
        x = self._x
        y = self._y
        
        # Change position base on anchor
        if anchor == 'top-left':
            # Anything changes
            pass
        elif anchor == 'center':
            x = float(x) + (float(self._width) / 2)
            y = float(y) + (float(self._height) / 2)
        
        # Source
        name = self.getname()
        source = '{0}\n{1}\n{2}\n{3}\n{4}\n\n'.format(
            Source.getstringconstant(name, '"{0}.png"'.format(self._id), language),
            Source.getfloatconstant('{0}_X'.format(name), x, language),
            Source.getfloatconstant('{0}_Y'.format(name), y, language),
            Source.getfloatconstant('{0}_W'.format(name), self._width, language),
            Source.getfloatconstant('{0}_H'.format(name), self._height, language)
        )
        
        return source
    
    def __str__(self):
        return self._id

##
# Present a layer in SVG file.
#
class Layer:
    _svg = None
    _name = ""          #layer name
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
        print(' - Parsing layer: %s' % self._name)
        self._elements = list() #should be initialized here for instances
        for node in layer:
            id = node.get('id')
            print('  + Found element: %s' % id)
            element = self._svg.getelement(id)
            self._elements.append(element)
    
    ##
    # Get an element of this layer.
    #
    def getelements(self):
        # print('**Layer::getelements: %s' % self._elements.count)
        return self._elements;
    
    def getname(self):
        name = 'k%s' % self._name;
        name = name.replace(' ', '_')
        return name;
    
    def __str__(self):
        return self._name

class SVG:
    _inkscape = ''
    _filename = ''
    _layers = list()            # list of Layers
    _elements = list()     #all elements from query command
    
    def __init__(self, inkscape, filename):
        self._filename = filename
        self._inkscape = inkscape
        self._layers = list() #should be initialized here for instances
        self._queryall()
        self._parse()
    
    ##
    # TODO Parse svg file for support layer.
    #
    def _parse(self):
        print('Parse SVG file: %s...' % self._filename)
        self._queryall()
        tree = ElementTree.parse(self._filename)
        for node in tree.findall('{%s}g' % SVG_NAMESPACE):
            layer = Layer(self, node)
            self._layers.append(layer)
    
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
        
        # Parse that query
        elements = query.splitlines()
        for line in elements:
            element = Element(line)
            self._elements.append(element)
    
    # def query(self, id):
    #     # Query an object using inkscape command line
    #     popen = subprocess.Popen([self._inkscape, self._filename, '--query-id=%s' % id],
    #         stdout = subprocess.PIPE,
    #         stderr = subprocess.PIPE
    #     )
    #     query, error = popen.communicate()
    #     return query
    
    def getelement(self, id):
        for element in self._elements:
            if id == element.getid():
                return element
    
    def exportsource(self, classname, sourcepath, language, anchor):
        print('Export source...')
        # Header
        if language == 'm' or language == 'cpp':
            headerfile = '{0}/{1}.h'.format(sourcepath, classname)
            print('Header file: {0}'.format(headerfile))
            
            f = open(headerfile, 'w')
            f.write(Source.getheaderfileheader(classname, language))
            
            # Extern values
            for layer in self._layers:
                print(' - Layer %s' % layer)
                f.write('// %s\n' % layer)
                for element in layer.getelements():
                    print('  + Element: %s' % element)
                    f.write(element.getheader(language))
            
            f.write(Source.getheaderfooter(language))
            f.close()
        
        # Source
        sourcefile = '{0}/{1}.{2}'.format(sourcepath, classname, language)
        print('Source file: {0}'.format(sourcefile))
        
        f = open(sourcefile, 'w')
        f.write(Source.getsourcefileheader(classname, language))
        
        for layer in self._layers:
            print(' - Layer %s' % layer)
            f.write('// %s\n' % layer)
            for element in layer.getelements():
                print('  + Element: %s' % element)
                f.write(element.getsource(language, anchor))
        
        f.write(Source.getsourcefooter(language))
        f.close()
        print('Done.')
    
    ##
    # Export all elements, except elements sub-elements.
    #
    def exporttexures(self, outputpath, dpi):
        print('Export textures, saved in: %s...' % outputpath)
        for layer in self._layers:
            print(' - Layer %s' % layer)
            for element in layer.getelements():
                print('  + Element: %s' % element)
                id = element.getid()
                popen = subprocess.Popen(
                    [
                        self._inkscape, '--file=%s' % self._filename,
                        '--export-id-only',
                        '--export-id=%s' % id,
                        '--export-dpi=%s' % dpi,
                        '--export-png=%s/%s.png' % (outputpath, id)
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
    parser.add_argument('-inkscape', help = 'Inkscape execute path', default = 'inkscape')
    parser.add_argument('-input', help = 'Inkscape input file', required = True)
    parser.add_argument('-class', help = 'Class name', default = 'Assets')
    parser.add_argument('-source', help = 'Source path', default = None)
    parser.add_argument('-language', help = 'Source language', default = 'm')
    parser.add_argument('-anchor', help = 'Anchor, default Top+Left', default = 'top-left')
    parser.add_argument('-textures', help = 'Textures path', default = None)
    parser.add_argument('-dpi', help = 'DPI, default 90', type = int, default = 90)
    args = vars(parser.parse_args(argv))
    
    # Parse args
    # TODO source: input class name, and path then generate both .h & .m files
    inkscape = args['inkscape']
    inputfile = args['input']
    classname = args['class']
    sourcepath = args['source']
    language = args['language']
    anchor = args['anchor']
    texturespath = args['textures']
    dpi = args['dpi']
    
    # SVG
    svg = SVG(inkscape, inputfile)
    if sourcepath is not None:
        svg.exportsource(classname, sourcepath, language, anchor)
    if texturespath is not None:
        svg.exporttexures(texturespath, dpi)

if __name__ == '__main__':
    main(sys.argv[1:])
