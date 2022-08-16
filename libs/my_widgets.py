import sys
import os
from enum import Enum

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout  #Позиционирование
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QProgressBar, QToolTip, QListWidget, QListWidgetItem, QSpacerItem, QSizePolicy, QTextEdit, QCommandLinkButton
from PyQt5.QtWidgets import QColorDialog, QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect, QRectF, QPointF
from PyQt5.QtGui import QIcon, QFont, QEnterEvent, QPainter, QColor, QPen, QTransform, QPixmap, QBrush, QPolygon, QImage, QPolygonF


class Render:
    def __init__(self, axes_area, WidgetDraw):
        self.axes_area = axes_area
        self.axes_area.GenGrid(style = 0.1)
        self.axes_show = False
        self.changed = False
        self.listOfObj = {}
        self.ind_obj = 0
        self.widget = WidgetDraw
    
    def Axes_show(self):
        if self.axes_show == True:
            self.axes_show = False
        else:
            self.axes_show = True

    def centre_all(self):
        boundingRect = self.widget.scene.itemsBoundingRect()
        self.widget.scene.setSceneRect(0, 0, boundingRect.right(), boundingRect.bottom())
    
    def renderAll(self):
        
        if self.changed == True:
            self.changed = False
            # Render Axes
            if self.axes_show == True:
                for obj in self.axes_area.grid:
                    p1, p2 = obj.points.values()
                    p1 = p1.PosXY()
                    p2 = p2.PosXY()
                    polygon = QPolygonF([QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1])])
                    p = self.widget.scene.addPolygon( polygon, self.widget.pencil, self.widget.brush)
                    self.widget.figs.append(p)
            
            # Render objects
            if len(self.listOfObj)>0:
                for obj in self.listOfObj.values():
                    if obj.type == 'Point':
                        x, y = obj.PosXY()
                        size = obj.my_size
                        color = obj.my_color
                        self.widget.set_pen(color, size)
                        self.widget.set_brush(color)
                        self.draw_point(x, y, size)
                    
                    if obj.type == 'Line':
                        data = obj.points
                        keys = list(data.keys())
                        color_line = obj.my_color
                        size_line = obj.my_size
                        
                        for i in range(len(keys)-1):
                            p1 = data[keys[i]]
                            x, y = p1.PosXY()
                            size = p1.my_size
                            color = p1.my_color
                            self.widget.set_pen(color, size)
                            self.widget.set_brush(color)
                            self.draw_point(x, y, size)
                            p1 = [x, y]
                            
                            p2 = data[keys[i+1]]
                            x, y = p2.PosXY()
                            p2 = [x, y]
                            
                            self.widget.set_pen(color_line, size_line)
                            # set color = color_line
                            self.draw_line(p1, p2)
                            
                        p_end = data[keys[-1]]
                        x, y = p_end.PosXY()
                        size = p_end.my_size
                        color = p_end.my_color
                        self.widget.set_pen(color, size)
                        self.widget.set_brush(color)
                        self.draw_point(x, y, size)
                        
                    if obj.type == 'Polygon':
                        print('Polygon')
                        print(obj.Info())
                        data = obj.points
                        keys = list(data.keys())
                        color_poly = obj.my_color
                        color_line = obj.line_color
                        size_line = obj.my_size
                        points = []
                        
                        for i in range(len(keys)-1):
                            p1 = data[keys[i]]
                            x, y = p1.PosXY()
                            size = p1.my_size
                            color = p1.my_color
                            self.widget.set_pen(color, size)
                            self.widget.set_brush(color)
                            self.draw_point(x, y, size)
                            points.append(QPointF(x, y))
                        
                        p_end = data[keys[-1]]
                        x, y = p_end.PosXY()
                        size = p_end.my_size
                        color = p_end.my_color
                        self.widget.set_pen(color, size)
                        self.widget.set_brush(color)
                        self.draw_point(x, y, size)
                        points.append(QPointF(x, y))
                        
                        self.widget.set_pen(color_line, size)
                        self.widget.set_brush(color_poly)
                        self.draw_polygon(points)
                    
    def draw_point(self, x, y, size):
        p = self.widget.scene.addEllipse (x, y, size, size, self.widget.pencil, self.widget.brush)
        self.widget.figs.append(p)
        
    def draw_line(self, p1, p2):
        polygon = QPolygonF([QPointF(p1[0], p1[1]), QPointF(p2[0], p2[1])])
        p = self.widget.scene.addPolygon( polygon, self.widget.pencil)
        self.widget.figs.append(p)
    
    def draw_polygon(self, points):
        polygon = QPolygonF(points)
        p = self.widget.scene.addPolygon( polygon, self.widget.pencil, self.widget.brush)
        self.widget.figs.append(p)
    
    def add_Obj(self, obj):
        self.listOfObj[self.ind_obj] = obj
        self.ind_obj += 1
        self.changed = True

class PointsGraphicsScene(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)
        self.opt = "Generate"
        self.axes_area = None
        
    def setOption(self, opt):
        self.opt = opt
    
class My_Canvas2(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = PointsGraphicsScene(self)
        self.setScene( self.scene )
        self.setRenderHint(QPainter.Antialiasing)

        self.pencil = QPen( Qt.black, 2)
        self.pencil.setStyle( Qt.SolidLine )
        self.brush = QBrush( QColor( 125, 125, 125, 125 ) )
    
        self.figs = []
        
        self.f_select = False
        self.movable = False
        self.f_area = False
        self.p_area = [0.0, 0.0]
        
        self.scale_zoom = 0.5
        self.def_zoom = 1.0
        self.cur_zoom = self.def_zoom
    
    
    def zoom_In(self):
        self.cur_zoom /= self.scale_zoom
        self.scale(self.cur_zoom, self.cur_zoom)
        self.update()
        
    def zoom_Out(self):
        self.cur_zoom *= self.scale_zoom
        self.scale(self.cur_zoom, self.cur_zoom)
        self.update()
        
    def zoom_default(self):
        self.cur_zoom = self.def_zoom
        self.scale(self.def_zoom, self.def_zoom)
        self.update()
    
    def set_pen(self, color, size):
        self.pencil = QPen( QColor(color), size)
        self.pencil.setStyle( Qt.SolidLine )
    def set_brush(self, color):
        self.brush = QBrush(QColor(color))
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            x_0 = self.p_area[0]
            y_0 = self.p_area[1]
            
            if self.movable == True:
                boundingRect = self.scene.itemsBoundingRect()
                dx = x_0-x if x_0>x else x-x_0
                dx = dx if x_0>x else -dx
                dy = y_0-y if y_0>y else y-y_0
                dy = dy if y_0>y else -dy
                self.scene.setSceneRect(dx, dy, boundingRect.right(), boundingRect.bottom())
                self.scene.update()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.RightButton:
            x = event.pos().x()
            y = event.pos().y()
        if event.button() & Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            if self.f_area == False and self.movable == True:
                self.p_area = [float(x), float(y)]
                self.f_area = True
        self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            if self.f_area == True:
                self.f_area = False
    
    
    def selectable(self):
        for item in self.scene.items():
            if self.f_select == True:
                item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            else:
                item.setFlag(QGraphicsItem.ItemIsMovable, False)
        for item in self.figs:
            if self.f_select == True:
                item.setFlag(QGraphicsItem.ItemIsSelectable, True)
            else:
                item.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.update()
                
    
    def remove(self):
        for item in self.scene.items():
            if item.isSelected():
                self.scene.removeItem(item)
    
    def sbrush(self):
        for item in self.scene.items():
            item.setBrush(QColor("red"))
    
    def rotate(self, value):
        items = self.scene.selectedItems()
        for item in items:
            item.setRotation(value)

    def up(self):
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

    def down(self):
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z - 1)
    
    def add(self, x, y):
        self.polygon = QPolygonF( [QPointF( 25+x, 30+y ), \
            QPointF( 40+x, 40+y ), QPointF( 20+x, 80+y ) ] )
        p = self.scene.addPolygon( self.polygon, self.pencil, self.brush )
        self.figs.append(p)
    
    def changepos(self):
        self.figs[0].setPos(50, 20)
        ellipse = QGraphicsEllipseItem(0, 0, 100, 100)
        ellipse.setPos(75, 30)
        pen = QPen(Qt.green)
        pen.setWidth(5)
        ellipse.setPen(pen)
        ellipse.setZValue(500)
        self.scene.addItem(ellipse)
        textitem = self.scene.addText("QGraphics is fun!")
        textitem.setPos(100, 100)
        self.scene.addPolygon(
            QPolygonF(
                [
                    QPointF(30, 60), 
                    QPointF(270, 40), 
                    QPointF(400, 200), 
                    QPointF(20, 150), 
                ]), 
            QPen(Qt.darkGreen), 
        )

        self.update()

    def rot(self):
        transform = QTransform()
        transform.translate(20, 100)
        transform.rotate(-90)
        for i in range(len(self.figs)):
            self.figs[i].setTransform(transform)
        self.update()

    def DrawArea(self):
        self.update()
    
    def resizeEvent(self, event):
        pass
        #self = self.scaled(self.width(), self.height())




class Entry(QLineEdit):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def checkFormat(self, path, fmt):
        f_fmt = path.split('/')[-1]
        if '.' not in f_fmt:
            return False
        else:
            f_fmt = f_fmt.split('.')[-1]
            return f_fmt == fmt
    
    def dragEnterEvent(self, event):
        if self.checkFormat(event.mimeData().text(), 'txt'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self.checkFormat(event.mimeData().text(), 'txt'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if self.checkFormat(event.mimeData().text(), 'txt'):
            event.accept()
            path = event.mimeData().text().replace('file:///', '')
            path = path.replace('/', '\\')
            self.setText(path)
        else:
            event.ignore()

class TitleBar(QWidget):    # Имитация верхней панели окна программы
    # Сигнал минимизации окна
    windowMinimumed = pyqtSignal()
    # Сигнал максимизации окна
    windowMaximumed = pyqtSignal()
    # Сигнал восстановления окна
    windowNormaled = pyqtSignal()
    # Сигнал закрытия окна
    windowClosed = pyqtSignal()
    # Сигнал перемещения окна
    windowMoved = pyqtSignal(QPoint)

    def __init__(self, height = 32, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = height
        self.heightW = self.height
        self.widthW = self.height
        self._old_pos = None
        self.widgets = {"size":0, 'elements':{}}

        self.setAttribute(Qt.WA_StyledBackground, True) # Поддержка настройки фона qss
        self.setObjectName('TitleBar')
        #self.setContentsMargins(0, 0, 0, 0)
        # Цвет фона (он прозрачный изза родительского класса)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 0, 0))
        self.setPalette(palette)

        # значок окна
        self.iconSize = self.height-10  # Размер значка по умолчанию
        self.iconLabel = QLabel(objectName = 'tb_ico')
        #self.iconLabel.setScaledContents(True)

        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self.setAutoFillBackground(True)

        # название окна
        self.titleLabel = QLabel()
        self.titleLabel.setObjectName('tb_title')
        #self.titleLabel.setMargin(2)

        # Слой для добавляемых виджетов
        self.layout_custom_widget = QHBoxLayout()
        #self.layout_custom_widget.setContentsMargins(0, 0, 0, 0)
        self.layout_custom_widget.setObjectName('tb_layout_widgets')
        
        # Стандартные кнопки окна 
        font = self.font() or QFont()
        font.setFamily('Webdings')  # Шрифты Webdings для отображения значков
        self.buttonMinimum = QPushButton('0', clicked = self.windowMinimumed.emit, font = font)
        self.buttonMinimum.setObjectName('tb_b_min')
        self.buttonMaximum = QPushButton('1', clicked = self.showMaximized, font = font)
        self.buttonMaximum.setObjectName('tb_b_max')
        self.buttonClose = QPushButton('r', clicked = self.windowClosed.emit, font = font)
        self.buttonClose.setObjectName('tb_b_close')

        # Группировка элементов на слое
        layout = QHBoxLayout(spacing = 0)
        layout.setContentsMargins(1, 2, 6, 1)
        layout.setObjectName('tb_layout')

        layout.addWidget(self.iconLabel)
        layout.addWidget(self.titleLabel)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addLayout(self.layout_custom_widget)
        layout.addWidget(self.buttonMinimum)
        layout.addWidget(self.buttonMaximum)
        layout.addWidget(self.buttonClose)

        self.setLayout(layout)

        # начальная высота
        self.setHeight(self.height)

    def setSizeBtns(self, width = None, height = None):
        change = 0
        if height != None and self.heightW != height:
            self.heightW = height
            change += 1
        if width != None and self.widthW != width:
            self.widthW = width
            change += 1
        if change != 0:
            self.RefreashSize()
    
    def setHeight(self, height = None):
        if height != None:
            self.height = height
            self.heightW = self.height
            self.widthW = self.height
            self.setMinimumHeight(self.height)
            self.setMaximumHeight(self.height)
            self.RefreashSize()
    
    def RefreashSize(self): # Обновить размеры icon, buttonMinimum, buttonMaximum, buttonClose
        def setSize(width, height, func):
            func.setMinimumSize(width, height)
            func.setMaximumSize(width, height) 
            #func.resize(width, height)
        setSize(self.widthW, self.heightW, self.iconLabel)
        setSize(self.widthW, self.heightW, self.buttonMinimum)
        setSize(self.widthW, self.heightW, self.buttonMaximum)
        setSize(self.widthW, self.heightW, self.buttonClose)
        for key in self.widgets['elements'].keys():
            widget = self.widgets['elements'][key]
            setSize(widget[1], widget[2], widget[0])
    
    def addWidget(self, widget, width = None, height = None):
        width = width if width != None else self.widthW
        height = height if height != None else self.heightW
        widget.setMinimumSize(width, height)
        widget.setMaximumSize(width, height)
        self.layout_custom_widget.addWidget(widget)
        ind = str(self.widgets['size'])
        self.widgets['elements'][ind] = [widget, width, height]
        self.widgets['size'] += 1
        self.RefreashSize()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit() # Максимизировать окно
        else:
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()  # Восстановить окно
    
    def setTitle(self, title = ""):
        self.titleLabel.setText(title)
    
    def setIcon(self, icon = None):
        if icon == None and self.icon != None:
            self.iconLabel.setPixmap(self.icon.pixmap(self.iconSize, self.iconSize))
        else:
            self.icon = icon
            self.iconLabel.setPixmap(self.icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        self.iconSize = size
        self.setIcon()
    
    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().enterEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.showMaximized()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()
        event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = None
        event.accept()
    
    def mouseMoveEvent(self, event):
        if self._old_pos and self.buttonMaximum.text() != '2':#event.buttons() == Qt.LeftButton
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self._old_pos))
        event.accept()

class Direction(Enum):  # Перечисление направлений
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4
    LEFT_TOP = 5
    RIGHT_TOP = 6
    LEFT_BOTTOM = 7
    RIGHT_BOTTOM = 8

class FramelessWindow(QWidget):
    def __init__(self, TitleBar_height = 35):
        super().__init__()
        # Поддержка настройки фона qss
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('FramelessWindow')
        self._old_pos = None
        self._direction = None

        self._widget = None

        self.setAttribute(Qt.WA_TranslucentBackground, True)    # Фон прозрачный
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)    #Не рисовать рамку оконного менеджера
        # or self.setWindowFlag(Qt.FramelessWindowHint)

        self.setMouseTracking(True)

        layout = QVBoxLayout(spacing = 0)

        # Отступы от полей дочернего окна
        #p.s.: т.к. виджет без рамки, это значение является шириной рамки изменения размера (образованной отступом)
        self.MARGINS = 5
        layout.setContentsMargins(self.MARGINS, self.MARGINS, self.MARGINS, self.MARGINS)

        # Панель заголовка
        self.titleBar = TitleBar(TitleBar_height, self)
        layout.addWidget(self.titleBar)

        self.setLayout(layout)

        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)

    def addWidget(self, widget):
        self._widget = widget

        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        
        self.layout().addWidget(self._widget)
        
    def showMaximized(self):
        super().showMaximized()
        # Растяжение layout до границ экрана при максимизации, т.к. у нас есть еще невидимая рамка
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        super().showNormal()
        # Возврат к нормальному состоянию размеров, с учетом невидимой рамки
        self.layout().setContentsMargins(self.MARGINS, self.MARGINS, self.MARGINS, self.MARGINS)

    def eventFilter(self, obj, event):  # Фильтр событий
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)  # Восстановление стандартного стиля мыши
        return super().eventFilter(obj, event)

    def paintEvent(self, event):    #Событие перерисовывания
        super().paintEvent(event)
        # Т.к. само окно прозрачное, рисуется жесткая граница чтобы контролировать размер окна
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.MARGINS))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self._old_pos = None
        self._direction = None

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.MARGINS, self.height() - self.MARGINS

        if self.isMaximized() or self.isFullScreen():
            self._direction = None
            self.setCursor(Qt.ArrowCursor)
            return

        if event.buttons() == Qt.LeftButton and self._old_pos:
            self._resizeWidget(pos)
            return

        if xPos <= self.MARGINS and yPos <= self.MARGINS:
            # Верхний левый угол
            self._direction = Direction.LEFT_TOP
            self.setCursor(Qt.SizeFDiagCursor)

        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # Нижний правый угол
            self._direction = Direction.RIGHT_BOTTOM
            self.setCursor(Qt.SizeFDiagCursor)

        elif wm <= xPos and yPos <= self.MARGINS:
            # верхний правый угол
            self._direction = Direction.RIGHT_TOP
            self.setCursor(Qt.SizeBDiagCursor)

        elif xPos <= self.MARGINS and hm <= yPos:
            # Нижний левый угол
            self._direction = Direction.LEFT_BOTTOM
            self.setCursor(Qt.SizeBDiagCursor)

        elif 0 <= xPos <= self.MARGINS and self.MARGINS <= yPos <= hm:
            # Влево
            self._direction = Direction.LEFT
            self.setCursor(Qt.SizeHorCursor)

        elif wm <= xPos <= self.width() and self.MARGINS <= yPos <= hm:
            # Право
            self._direction = Direction.RIGHT
            self.setCursor(Qt.SizeHorCursor)

        elif self.MARGINS <= xPos <= wm and 0 <= yPos <= self.MARGINS:
            # выше
            self._direction = Direction.TOP
            self.setCursor(Qt.SizeVerCursor)

        elif self.MARGINS <= xPos <= wm and hm <= yPos <= self.height():
            # ниже
            self._direction = Direction.BOTTOM
            self.setCursor(Qt.SizeVerCursor)

        else:
            # Курсор по умолчанию
            self.setCursor(Qt.ArrowCursor)

    def _resizeWidget(self, pos):
        if self._direction is None:
            return
        
        mpos = pos - self._old_pos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        if self._direction == Direction.LEFT_TOP:          # Верхний левый угол
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos

            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos

        elif self._direction == Direction.RIGHT_BOTTOM:    # Нижний правый угол
            if w + xPos > self.minimumWidth():
                w += xPos
                self._old_pos = pos

            if h + yPos > self.minimumHeight():
                h += yPos
                self._old_pos = pos

        elif self._direction == Direction.RIGHT_TOP:       # верхний правый угол
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos

            if w + xPos > self.minimumWidth():
                w += xPos
                self._old_pos.setX(pos.x())

        elif self._direction == Direction.LEFT_BOTTOM:     # Нижний левый угол
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos

            if h + yPos > self.minimumHeight():
                h += yPos
                self._old_pos.setY(pos.y())

        elif self._direction == Direction.LEFT:            # Левый
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return

        elif self._direction == Direction.RIGHT:           # Правый
            if w + xPos > self.minimumWidth():
                w += xPos
                self._old_pos = pos
            else:
                return

        elif self._direction == Direction.TOP:             # Верх
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return

        elif self._direction == Direction.BOTTOM:          # Низ
            if h + yPos > self.minimumHeight():
                h += yPos
                self._old_pos = pos
            else:
                return

        self.setGeometry(x, y, w, h)
