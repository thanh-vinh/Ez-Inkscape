# ezsvg
# GUI/Level editor by InkScape
# and more...

import argparse
import subprocess
import sys
import time
from xml.etree import ElementTree

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
INKSCAPE_NAMESPACE = 'http://www.inkscape.org/namespaces/inkscape'

class Element:
    _query = ''
    _id = ''
    _x = 0
    _y = 0
    _width = 0
    _height = 0
    
    """
    Format data like:
        svg2,177.14285,223.79076,285.71428,314.28571
    store in a line of query info
    """
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
    
    """
    Generate source code.
    """
    def getsource(self, language = 'objective-c'):
        if language == 'objective-c':
            source = 'const NSString *%s = @"%s.png";\n' % (self.getname(), self._id)
            source += 'const static float %s_X = %s;\n' % (self.getname(), self._x)
            source += 'const static float %s_Y = %s;\n' % (self.getname(), self._y)
            source += 'const static float %s_W = %s;\n' % (self.getname(), self._width)
            source += 'const static float %s_H = %s;\n\n' % (self.getname(), self._height)
        elif language == 'cpp':
            source = 'WIP\n'
        elif language == 'cs':
            source = 'WIP\n'
        else:
            source = 'Not support\n'
        
        return source
    
    def __str__(self):
        return self._id

"""
Present a layer in SVG file.
"""
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
    
    """
    Get an element of this layer.
    """
    def getelements(self):
        # print('**Layer::getelements: %s' % self._elements.count)
        return self._elements;
    
    def getname(self):
        name = 'k%s' % self._name;
        name = name.replace(' ', '_')
        return name;
    
    """
    Print layer source only, not include elements source
    """
    def getsource(self, language = 'objective-c'):
        if language == 'objective-c':
            source = 'const static float %s_X = %s;\n' % (self.getname(), self._x)
            source += 'const static float %s_Y = %s;\n\n' % (self.getname(), self._y)
        elif language == 'cpp':
            source = 'WIP\n'
        elif language == 'cs':
            source = 'WIP\n'
        else:
            source = 'Not support\n'
        
        return source
    
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
    
    """
    TODO Parse svg file for support layer.
    """
    def _parse(self):
        print('Parse SVG file: %s...' % self._filename)
        self._queryall()
        tree = ElementTree.parse(self._filename)
        for node in tree.findall('{%s}g' % SVG_NAMESPACE):
            layer = Layer(self, node)
            self._layers.append(layer)
    
    """
    Query all objects
    """
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
    
    def exportsource(self, outputfile, language):
        print('Export source...')
        # Write header
        f = open(outputfile, 'w');
        f.write('//\n');
        f.write('// Generated by ezsvg\n');
        f.write('// Source: %s\n' % self._filename);
        f.write('// Date: %s\n' % time.strftime('%d/%m/%Y %H:%M:%S'));
        f.write('//\n\n');
        
        # Get source
        for layer in self._layers:
            print(' - Layer %s' % layer)
            f.write('// %s\n' % layer)
            f.write(layer.getsource())
            for element in layer.getelements():
                print('  + Element: %s' % element)
                f.write(element.getsource())
        
        f.close()
        print('Done.')
    
    """
    Export all elements, except elements sub-elements.
    """
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
    parser.add_argument('-source', help = 'Source file', default = None)
    parser.add_argument('-language', help = 'Source language', default = 'objective-c')
    parser.add_argument('-textures', help = 'Textures path', default = None)
    parser.add_argument('-dpi', help = 'DPI, default 90', type = int, default = 90)
    args = vars(parser.parse_args(argv))
    
    # Parse args
    inkscape = args['inkscape']
    inputfile = args['input']
    sourcefile = args['source']
    language = args['language']
    texturespath = args['textures']
    dpi = args['dpi']
    
    # SVG
    svg = SVG(inkscape, inputfile)
    if sourcefile is not None:
        svg.exportsource(sourcefile, language)
    if texturespath is not None:
        svg.exporttexures(texturespath, dpi)

if __name__ == '__main__':
    main(sys.argv[1:])
