#Universidad del Valle de Guatemala
#Graficas por Computadoras
#Fernando Jose Garavito Ovando 18071
#Lab 1: Filling any Polygon
#gl
#Catedratico Carlos Alonso: https://uvg.instructure.com/courses/21985/modules/items/413892
#https://stackoverflow.com/questions/67822179/find-polygon-top-left-top-right-bottom-right-and-bottom-left-points
#https://es.stackoverflow.com/questions/386520/como-mostrar-un-poligono-en-python
#https://stackoverflow.com/questions/66784929/edit-polygon-coords-using-python-shapely-and-fiona

import struct

def char(c):
    # 1 byte
		return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
	return struct.pack('=h', w)
	
def dword(d):
    # 4 bytes
	return struct.pack('=l', d)

def ColorArray(Colors):
    return [round(i*255) for i in Colors]

def color(r,g,b):
    # Acepta valores de 0 a 1
    # Se asegura que la información de color se guarda solamente en 3 bytes
	return bytes([b, g, r])

BLACK = color(0,0,0)

class Renderer(object):
    def __init__(self):
        self.framebuffer = []
        self.width = 500
        self.height = 500
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 500
        self.viewport_height = 500
        self.Polygons = []
        self.glClear()

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    def glViewport(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def glClear(self):
        self.framebuffer = [
            [BLACK for x in range(self.width)] for y in range(self.height)
        ]

    def glClearColor(self, r=1, g=1, b=1):
        Order = ColorArray([r,g,b])
        clearColor = color(Order[0], Order[1], Order[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def glVertex(self, x, y):
        XX = round((x+1) * (self.viewport_width/2) + self.viewport_x)
        YY = round((y+1) * (self.viewport_height/2) + self.viewport_y)
        self.point(XX, YY)

    def glColor(self, r=0, g=0, b=0):
        Order = ColorArray([r,g,b])
        self.color = color(Order[0], Order[1], Order[2])

    def glPosition(self, value, value2):
        Position = ((value+1) * (self.viewport_height/2) + self.viewport_y) if value2 else ((value+1) * (self.viewport_width/2) + self.viewport_x)
        return round(Position)

    def glDrawPolygon(self, vertices):
        self.Polygons = vertices
        Value = len(vertices)
        for limit in range(Value):
            Value1 = vertices[limit]
            Value2 = vertices[(limit + 1) % Value]
            self.glLine(Value1[0], Value1[1], Value2[0], Value2[1])

    def Vertex(self, XPosition, YPosition): 
        A = []
        B = []

        Vertexs = len(self.Polygons)
        limit = Vertexs - 1;

        for i in range(Vertexs):
            if(YPosition[limit] == YPosition[i]):
                A.append(XPosition[i])
                B.append(0)
            else:
                A.append(XPosition[i] - (YPosition[i] * XPosition[limit]) / (YPosition[limit] - YPosition[i]) + (YPosition[i] * XPosition[i]) / (YPosition[limit] - YPosition[i]))
                B.append((XPosition[limit] - XPosition[i]) / (YPosition[limit] - YPosition[i])) 
            limit = i;
            
        return (A, B)
    
    def Figures(self, x, y):
        XPosition = [axis[0] for axis in self.Polygons]
        YFigurePosition = [axis[1] for axis in self.Polygons]
        (A, B) = self.Vertex(XPosition, YFigurePosition)
        Figure = False
        Number_of_vertex = len(self.Polygons)
        current_node = YFigurePosition[Number_of_vertex - 1] > y
        
        for i in range(Number_of_vertex):
            previous_node = current_node
            current_node = YFigurePosition[i] > y; 
            if (current_node != previous_node):
                Figure ^= y * B[i] + A[i] < x
        return Figure
 
    def glFillPolygon(self):
           # Parte de adentro de la figura
        XMin = min(self.Polygons, key = lambda i : i[0])[0]
        YMin = min(self.Polygons, key = lambda i : i[1])[1]
        XMax = max(self.Polygons, key = lambda i : i[0])[0]
        YMax = max(self.Polygons, key = lambda i : i[1])[1]
        for y in range(YMin, YMax):
            for x in range(XMin, XMax):                 
                if self.Figures(x, y):
                    self.point(x,y) 
    
    # Colocar una linea entre las dos coordenadas
    def glLine(self, x0, y0, x1, y1) :

    # Devolver el valor absoluto
        C = abs(y1 - y0) > abs(x1 - x0)
        if C:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        offset = 0 
        y = y0
        threshold =  dx
        for x in range(x0, x1):
            self.point(y, x) if C else self.point(x, y)
            offset += 2*dy
            if offset >= threshold:
                y += -1 if y0 > y1 else 1
                threshold += 2*dx
                
    def glFinish(self, filename='Filling any Polygon.bmp'):
        #Crea un archivo BMP y lo llena con la información dentro de self.pixels
        f = open(filename, 'wb')

        # Header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # InfoHeader
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Colocar los puntos
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()
