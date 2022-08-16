
"""
__add__(self, other) - Сложение.
__sub__(self, other) - Вычитание.
__mul__(self, other) - Умножение.
__str__ - Строковые представления print
__repr__ - Строковые представления
__dict__ - все атрибуты класса или объекта
__cmp__(self, other)	self == other, self > other, etc.	Вызывается для любого сравнения
__pos__(self)	+self	Унарный знак плюса
__neg__(self)	-self	Унарный знак минуса
"""



"""
import random
lst = [random.randint(-10000, 10000) for i in range(1000)]
arr = [2, 6, 1, 5, 3, 4]
res = bubbleSortOptimized(arr)
"""
def bubbleSortOptimized(arr):
    for i in range(len(arr)):
        swapped = False
        for j in range(0, len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        # if no elements are swapped, break the loop
        if swapped == False:
            break
    return arr

# ========== 
# Default
class Object:
    counter = 0
    dco = False
    
    def __init__(self, pos_x = None, pos_y = None, pos_z = None, dco = False):
        self.indx = self.__class__.counter
        self.__class__.dco = dco
        if self.__class__.dco == False:
            self.__class__.counter += 1
        self.type = 'Object'
        self.pos_x = 0
        self.pos_y = 0
        self.pos_z = 0
        self.Set_def_name()
        self.Set_pos(pos_x, pos_y, pos_z)
    
    @classmethod
    def __del__(cls):
        if cls.dco == False:
            cls.counter -= 1
    
    @classmethod
    
    def Count(cls):
        return cls.counter
    
    def __str__(self):
        return self.name+': '+str(list(self.PosXY()))
    
    def Set_pos(self, pos_x = None, pos_y = None, pos_z = None):
        if pos_x != None:
            self.pos_x = pos_x
        if pos_y != None:
            self.pos_y = pos_y
        if pos_z != None:
            self.pos_z = pos_z
    
    def Set_def_name(self):
        self.name = self.type+'_'+str(self.indx)
    
    def Set_name(self, name = None):
        if name != None:
            self.name = name
    
    def Set_type(self, type = None):
        if type != None:
            self.type = type
    
    def PosXY(self):
        return [self.pos_x, self.pos_y]
    
    def PosXYZ(self):
        return [self.pos_x, self.pos_y, self.pos_z]
    
    def Name(self):
        return self.name
    
    def __dict__(self):
        ans = {}
        ans['Count'] = self.Count()
        ans['Indx'] = self.indx
        ans['Name'] = self.name
        ans['Type'] = self.type
        return ans
    
    def Info(self):
        ret = self.__dict__()
        def dict_crauler(my_dict, tab = 0):
            ans = ''
            for key in my_dict.keys():
                if type(my_dict[key]) == type({}):
                    ret = dict_crauler(my_dict[key], tab+2)
                    ans += ' '*tab+str(key)+': \n'
                    ans += ret
                else:
                    ans += ' '*tab+str(key)+': '+str(my_dict[key])+'\n'
            return ans
        ans = dict_crauler(ret)
        print(ans)

class Point(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'Point'
        self.Set_def_name()
        self.my_color = '#000'
        self.my_size = 0.1
    
    def Set_color(self, color = None):
        if color != None:
            self.my_color = color
    
    def Set_size(self, size = None):
        if size != None:
            self.my_size = size
    
    def __dict__(self):
        ret = super().__dict__()
        ans = {}
        for key in ret.keys():
            ans[key] = ret[key]
        ans['Color'] = self.my_color
        ans['Size'] = self.my_size
        ans['PosXY'] = self.PosXY()
        ans['PosXYZ'] = self.PosXYZ()
        return ans


class Line(Point):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'Line'
        self.Set_def_name()
        self.points = {}
        self.p_ind = 0
    
    def Add(self, pos_x = None, pos_y = None, pos_z = None, color = None, size = None, name = None, dco = False):
        p = Point(pos_x = pos_x, pos_y = pos_y, pos_z = pos_z, dco = dco)
        p.Set_name(name)
        p.Set_color(self.my_color)
        p.Set_color(color)
        p.Set_size(self.my_size)
        p.Set_size(size)
        self.points[self.p_ind] = p
        self.p_ind += 1
    
    def PointsColor(self):
        return [i.my_color for i in self.points.values()]
    
    def PointsSize(self):
        return [i.my_size for i in self.points.values()]
    
    def PointsXY(self):
        return [i.PosXY() for i in self.points.values()]
    
    def PointsXYZ(self):
        return [i.PosXYZ() for i in self.points.values()]
    
    def __dict__(self):
        ret = super().__dict__()
        ans = {}
        for key in ret.keys():
            ans[key] = ret[key]
        ans['Points'] = {}
        for key in self.points.keys():
            ans['Points'][key] = self.points[key].__dict__()
        return ans
    
    def __str__(self):
        return super().__str__()+' '+str(self.PointsXY())

class Polygon(Line):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'Polygon'
        self.Set_def_name()
        self.line_color = self.my_color
    
    def Set_line_color(self, color = None):
        if color != None:
            self.line_color = color
    
    def CheckLineCloses(self):
        if str(self.points[0].PosXYZ()) != str(self.points[self.p_ind-1].PosXYZ()):
            self.CloseLine()
    
    def CloseLine(self):
        x, y, z = self.points[0].PosXYZ()
        Name = None
        Color = self.points[0].my_color
        Size = self.points[0].my_size
        self.Add(pos_x = x, pos_y = y, pos_z = z, name = Name, color = Color, size = Size)
    
    def PointsColor(self):
        self.CheckLineCloses()
        return [i.my_color for i in self.points.values()]
    
    def PointsSize(self):
        self.CheckLineCloses()
        return [i.my_size for i in self.points.values()]
    
    def PointsXY(self):
        self.CheckLineCloses()
        return [i.PosXY() for i in self.points.values()]
    
    def PointsXYZ(self):
        self.CheckLineCloses()
        return [i.PosXYZ() for i in self.points.values()]

class Camera(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'Camera'
        self.Set_def_name()
        self.my_width = 20
        self.my_height = 20
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
    
    def Set_width(self, width = None):
        if width != None:
            self.my_width = width
    
    def Set_height(self, height = None):
        if height != None:
            self.my_height = height
    
    def Set_angle(self, angle_x = None, angle_y = None, angle_z = None):
        if angle_x != None:
            self.angle_x = angle_x
        if angle_y != None:
            self.angle_y = angle_y
        if angle_z != None:
            self.angle_z = angle_z
    
    def __dict__(self):
        ret = super().__dict__()
        ans = {}
        for key in ret.keys():
            ans[key] = ret[key]
        ans['Width'] = self.my_width
        ans['Height'] = self.my_height
        ans['Angle_x'] = self.angle_x
        ans['Angle_y'] = self.angle_y
        ans['Angle_z'] = self.angle_z
        return ans
        

class Axes_singleton(Object):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'Axes'
        self.Set_def_name()
        self.my_width = 21
        self.my_height = 21
        self.my_scale = 1
        self.my_size = 0.5
        self.grid = []
    
    def Set_width(self, width = None):
        if width != None:
            self.my_width = width
    
    def Set_height(self, height = None):
        if height != None:
            self.my_height = height
    
    def Set_scale(self, scale = None):
        if scale != None:
            self.my_scale = scale
    
    def __dict__(self):
        ret = super().__dict__()
        ans = {}
        for key in ret.keys():
            ans[key] = ret[key]
        ans['Width'] = self.my_width
        ans['Height'] = self.my_height
        ans['Scale'] = self.my_scale
        return ans
    
    def GenGrid(self, style = 'all'):
        w = (self.my_width-self.my_width%2)/2
        h = (self.my_height-self.my_height%2)/2
        w = int(w)
        h = int(h)
        left = self.pos_x-w
        right = self.pos_x+w
        top = self.pos_y+h
        bottom = self.pos_y-h
        size_left = left
        size_right = right
        size_top = top
        size_bottom = bottom
        if type(style) in [float, int]:
            size_left = self.pos_x-style
            size_right = self.pos_x+style
            size_top = self.pos_y+style
            size_bottom = self.pos_y-style
        size_left = float(size_left)
        size_right = float(size_right)
        size_top = float(size_top)
        size_bottom = float(size_bottom)
        
        for i in range(bottom, top, self.my_scale):
            L = Line(dco = True)
            L.Add(pos_x = size_left, pos_y = i, dco = True)
            L.Add(pos_x = size_right, pos_y = i, dco = True)
            self.grid.append(L)
        for i in range(left, right, self.my_scale):
            L = Line(dco = True)
            L.Add(pos_x = i, pos_y = size_top, dco = True)
            L.Add(pos_x = i, pos_y = size_bottom, dco = True)
            self.grid.append(L)
        L = Line(dco = True)
        L.Set_color = '#f00'
        L.Set_size = self.my_size
        L.Add(pos_x = 0, pos_y = top, dco = True)
        L.Add(pos_x = 0, pos_y = bottom, dco = True)
        L = Line(dco = True)
        L.Set_color = '#00f'
        L.Set_size = self.my_size
        L.Add(pos_x = left, pos_y = 0, dco = True)
        L.Add(pos_x = right, pos_y = 0, dco = True)
        self.grid.append(L)
        



if __name__ == '__main__':
    pass
