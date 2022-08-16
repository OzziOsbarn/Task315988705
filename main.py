import sys
import os
from enum import Enum

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout  #Позиционирование
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QProgressBar, QToolTip, QListWidget, QListWidgetItem
from PyQt5.QtWidgets import QMessageBox, QTabWidget,QFileDialog, QSpacerItem, QSizePolicy, QTextEdit, QCommandLinkButton
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QEnterEvent, QPainter, QColor, QPen, QPixmap, QBrush, QPolygon

from libs.elements import Object, Point, Line, Polygon, Camera, Axes_singleton
from libs.my_widgets import FramelessWindow, Direction, TitleBar, Entry, My_Canvas2, Render





STYLE_SHEET = """
#default{
    background-color: #0DABD2;
    padding:2px;
    border: 1px solid #000;
    border-radius: 11px;
    color:#fff;
    font-size:16px;
    font-weight:900;
    font-family:Calibri;


}
#default:hover {
    color: white;
    background-color: rgb(232, 17, 35);
    border: 2px solid #00ff00;
}
#default:pressed {
    background-color: rgb(250, 125, 144);
}

#TabW{
    padding:2px;
    color:#000;
    font-size:14px;
    font-family:Calibri;
}
#TabW::pane {
    border: 0;
    border-top:1px solid gray;
    background: rgb(245, 245, 245);
    padding:0px;
}
QTabBar::tab {
    background: rgb(245, 245, 245); 
    border: 1px solid lightgray; 
    border-radius: 5px;
    padding: 3px;
} 
QTabBar::tab:hover { 
  background: rgb(230, 230, 230); 
}
QTabBar::tab:selected { 
  background: rgb(200, 200, 200); 
  margin-bottom: -3px; 
}

#Edit_path{
    background-color: #fff;
    padding:2px;
    border:1px solid #000;
    color:#959595;
    font-size:22px;
    font-family:Calibri;
}
#Edit_path:focus{
    color:#000;
    border: 2px solid #006080;
}

#Btn_main{
    background-color: #008CFF;
    padding:2px;
    border: 2px solid #000;
    border-radius: 11px;
    color:#fff;
    font-size:22px;
    font-weight:900;
    font-family:Calibri;
}
#Btn_main:hover {
    color: #fff;
    background-color: #007EDE;
    border:0;
    border: 2px solid #000;
}
#Btn_main:pressed {
    background-color: #00D0DF;
    border:0;
    border: 1px solid #000;
}
#default_btns{
    background-color: #008CFF;
    padding:2px;
    border: 1px solid #000;
    color:#fff;
    font-size:22px;
    font-weight:900;
    font-family:Calibri;
}
#default_btns:hover {
    color: #fff;
    background-color: #007EDE;
    border:0;
    border: 1px solid #000;
}
#default_btns:pressed {
    background-color: #00D0DF;
    border:0;
    border: 1px solid #cacaca;
}
#default_btns:checked {
    background-color: #00D0DF;
    border: 1px solid #cacaca;
}



#btns_sw {
    background-color: #2BE5F2;
}
#btns_sw:hover {
    background-color: #007EDE;
}
#btns_sw:pressed {
    background-color: #00D0DF;
}
#btns_tg {
    background-color: #2BF2BD;
}
#btns_tg:hover {
    background-color: #007EDE;
}
#btns_tg:pressed {
    background-color: #00D0DF;
}
#btns_cl {
    background-color: #C32BF2;
}
#btns_cl:hover {
    background-color: #007EDE;
}
#btns_cl:pressed {
    background-color: #00D0DF;
}


#Canvas{
    background-color: #fff;
    border: 2px solid #000;
    border: 5px solid #000;
}
#Label_status{
    padding:2px;
    color:#000;
    font-size:14px;
    font-family:Calibri;
}

#tb_title{
    font-size:22px;
    font-family:Calibri;
    color:#959595;
}
#TitleBar, #tb_b_min, #tb_b_max, #tb_b_close, #tb_b_def {
    background-color: #fff;
    border: none;
    margin:0px;
    color: #000;
}
#TitleBar{
    border-color:  #000;
    border-top: 2px solid;
    border-left: 2px solid;
    border-right: 2px solid;
    border-bottom: none;
}
#BodyWindow {
    background-color: #fff;
    color: #000;
    border-color:  #000;
    border-top: 1px solid #000;
    border-left: 2px solid;
    border-right: 2px solid;
    border-bottom: 2px solid;
}
#tb_layout{

}
#tb_b_min, #tb_b_max, #tb_b_close,#tb_b_def {
    margin:1px;
    background-color: #fff;
    border-radius: 11px;
    border: 1px solid #000;
    font-size:12px;
    color:#000;
}
#tb_b_min:hover,#tb_b_max:hover,#tb_b_def:hover {
    background-color: #000;
    color: #fff;
    border: 2px solid #000;
}
#tb_b_min:pressed,#tb_b_max:pressed,#tb_b_def:pressed {
    background-color: #F7891A;
}
#tb_b_close:hover {
    color: #fff;
    border: 2px solid #000;
    background-color: rgb(232, 17, 35);
}
#tb_b_close:pressed {
    color: #fff;
    background-color: rgb(161, 73, 92);
}
"""


class MainWindow(QWidget):
    def __init__(self, title='test', height=300, weight=600):
        super().__init__()
        self.current_directory  = os.path.dirname(__file__)
        
        # Создание окна без рамки
        self.window = FramelessWindow(35)
        #self.titleBar = self.window.titleBar
        
        # Window Settings
        self.title = title
        self.window.setWindowTitle(self.title)
        
        self.window_height, self.window_width = height, weight
        #self.setMinimumSize(self.window_width, self.window_height)
        
        
        self.buttonMy = QPushButton('i', clicked=self.help, objectName='tb_b_def')
        
        dir_ico_logo = os.path.join( self.current_directory, 'icons\\logo.png' )
        ico_logo=QIcon(dir_ico_logo)
        self.window.setWindowIcon(ico_logo)
        self.window.titleBar.setSizeBtns(25,25)
        self.window.titleBar.addWidget(self.buttonMy)#, width=20, height=20)
        
        self.window.addWidget(BodyWindow())
    
    
    def msg(self, title='', Text='', ico=None):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(str(title))
        msgBox.setText(Text)
        if ico!=None:
            msgBox.setWindowIcon(QIcon(ico))
        msgBox.exec_()
    
    def help(self):
        Text='Программа для работы с картографическими данными.\n'+\
                'Программа читает текстовые файлы формата *.txt.\n'+\
                'В файле должны содержаться пары координат точек x и y.\n'+\
                'Пары координат образуют объекты: точка (1 пара), прямая (2 пары), полигон(3 и более пар).\n'+\
                'Все координаты должны быть отделены знаком "пробел". Допускается вносить дробные координаты, с плавающей точкой (знак ".").\n'
        self.msg('Описание', Text, 'icons\\about.png')

    
    def show(self):
        self.window.show()

#   Body
class BodyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Поддержка настройки фона qss
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('BodyWindow')
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.Edit_path = Entry('C:\\Users\\Екатерина\\Desktop\\Python\\QT\\map_vectors\\my-map.txt')
        self.Edit_path.setObjectName('Edit_path')
        self.Edit_path.setMinimumHeight(35)
        self.Edit_path.setMaximumHeight(35)
        self.Edit_path.textChanged.connect(self.Check_Edit)
        self.Edit_path.returnPressed.connect(self.Load_file)
        
        
        stgs={
            'name': 'Обзор',
            'obj_name': 'Btn_main',
            'property_name': 'get_path',
            'property_type': 'click',
            'tooltip': 'Обзор',
            'ico': '',
            'width': 200,
            'height': 35,
            'cmd': self.Choose_file
        }
        self.Btn_open=self.gen_btns(stgs)
        stgs={
            'name': '',
            'obj_name': 'Btn_main',
            'property_name': 'save_file',
            'property_type': 'click',
            'tooltip': 'Сохранить',
            'ico': 'icons\\save.png',
            'shortcut': 'Ctrl+S',
            'width': 35,
            'height': 35,
            'cmd': self.Save_file
        }
        self.Btn_save=self.gen_btns(stgs)

        self.Canvas= My_Canvas2()
        #self.Canvas.update()
        self.Canvas.setObjectName('Canvas')
        self.Canvas.setMinimumSize(200, 300)
        #self.Canvas.setMaximumSize(200, 300)
        
        self.Label_status = QLabel('Документ прочитан без ошибок')
        self.Label_status.setObjectName('Label_status')
        self.Label_status.setMinimumHeight(35)
        self.Label_status.setMaximumHeight(35)
        
        Layout_t1= QHBoxLayout()
        Layout_t1.setSpacing(0)
        Layout_t1.addWidget(self.Label_status,2)
        
        Layout_t2= QHBoxLayout()
        Layout_t2.setSpacing(1)
        Layout_t2.setObjectName('Layout_t2')
        Layout_t2_sw= QHBoxLayout()
        Layout_t2_sw.setSpacing(0)
        Layout_t2_sw.setObjectName('Layout_t2_sw')
        Layout_t2_tg= QHBoxLayout()
        Layout_t2_tg.setSpacing(0)
        Layout_t2_tg.setObjectName('Layout_t2_tg')
        Layout_t2_cl= QHBoxLayout()
        Layout_t2_cl.setSpacing(0)
        Layout_t2_cl.setObjectName('Layout_t2_cl')
        Layout_t2.addLayout(Layout_t2_tg)
        Layout_t2.addLayout(Layout_t2_cl)
        Layout_t2.addLayout(Layout_t2_sw)
        
        stgs={
            'switch': [
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'grid',
                    'property_type': 'switch',
                    'tooltip': 'grid',
                    'ico': 'icons\\grid.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.switch_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'move',
                    'property_type': 'switch',
                    'tooltip': 'move',
                    'ico': 'icons\\move.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.switch_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'rotate',
                    'property_type': 'switch',
                    'tooltip': 'rotate',
                    'ico': 'icons\\rotate.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.switch_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'select',
                    'property_type': 'switch',
                    'tooltip': 'select',
                    'ico': 'icons\\select.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.switch_btn
                }
            ],
            'toggle': [
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'point',
                    'property_type': 'toggle',
                    'tooltip': 'point',
                    'ico': 'icons\\point.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.toggle_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'line',
                    'property_type': 'toggle',
                    'tooltip': 'line',
                    'ico': 'icons\\line.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.toggle_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'polygon',
                    'property_type': 'toggle',
                    'tooltip': 'polygon',
                    'ico': 'icons\\polygon.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.toggle_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'rectangle',
                    'property_type': 'toggle',
                    'tooltip': 'rectangle',
                    'ico': 'icons\\rectangle.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.toggle_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'sphere',
                    'property_type': 'toggle',
                    'tooltip': 'sphere',
                    'ico': 'icons\\sphere.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.toggle_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'brush',
                    'property_type': 'toggle',
                    'tooltip': 'brush',
                    'ico': 'icons\\brush.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.toggle_btn
                }
            
            ],
            'click': [
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'pen_size',
                    'property_type': 'click',
                    'tooltip': 'pen_size',
                    'ico': 'icons\\pen_size.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'color_select',
                    'property_type': 'click',
                    'tooltip': 'color_select',
                    'ico': 'icons\\color_select.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'copy',
                    'property_type': 'click',
                    'tooltip': 'copy',
                    'ico': 'icons\\copy.png',
                    'width': 35,
                    'height': 35,
                    'shortcut': 'Ctrl+C',
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'clear',
                    'property_type': 'click',
                    'tooltip': 'clear',
                    'ico': 'icons\\clear.png',
                    'width': 35,
                    'height': 35,
                    'shortcut': 'del',
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'zoom_in',
                    'property_type': 'click',
                    'tooltip': 'zoom_in',
                    'ico': 'icons\\zoom_in.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'zoom_out',
                    'property_type': 'click',
                    'tooltip': 'zoom_out',
                    'ico': 'icons\\zoom_out.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'zoom_def',
                    'property_type': 'click',
                    'tooltip': 'zoom_def',
                    'ico': 'icons\\zoom_def.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'center',
                    'property_type': 'click',
                    'tooltip': 'center',
                    'ico': 'icons\\center.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.click_btn
                },
                {
                    'name': '',
                    'obj_name': 'default_btns',
                    'property_name': 'group',
                    'property_type': 'click',
                    'tooltip': 'group',
                    'ico': 'icons\\group.png',
                    'width': 35,
                    'height': 35,
                    'cmd': self.click_btn
                }
            ]
        }
        # switch - переключатель, связан с группой кнопок
        # toggle - нажатье и освобождение кнопки по клику
        # click - однократные клики
        self.tab_btns={
            'switch': {},
            'toggle': {},
            'click': {}
        }
        for key in stgs.keys():
            for stg in stgs[key]:
                btn = self.gen_btns(stg)
                if key in ['toggle', 'switch']:
                    btn.setCheckable(True)
                    btn.setChecked(False)
                    btn.toggle()
                    btn.clicked.connect(self.btns_style_change)
                    #btn.setProperty('clicked', '0')
                self.tab_btns[key][btn.property('name')] = btn
                if key=='switch':
                    Layout_t2_sw.addWidget(btn)
                elif key == 'toggle':
                    Layout_t2_tg.addWidget(btn)
                elif key == 'click':
                    Layout_t2_cl.addWidget(btn)
        Layout_t2.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab1.setLayout(Layout_t1)
        self.tab2.setLayout(Layout_t2)
        self.TabW = QTabWidget()
        self.TabW.setObjectName('TabW')
        self.TabW.setMinimumHeight(80)
        self.TabW.setMaximumHeight(80)
        self.TabW.addTab(self.tab1, "Tab 1")
        self.TabW.addTab(self.tab2, "Tab 2")
        
        
        
        HLayout_1= QHBoxLayout()
        HLayout_1.setObjectName('HLayout_1')
        HLayout_1.addWidget(self.Edit_path,2)
        HLayout_1.addWidget(self.Btn_open)
        HLayout_1.addWidget(self.Btn_save)
        
        HLayout_2= QHBoxLayout()
        HLayout_2.setObjectName('HLayout_2')
        HLayout_2.addWidget(self.Canvas,1)
        
        HLayout_3= QHBoxLayout()
        HLayout_3.setObjectName('HLayout_3')
        HLayout_3.addWidget(self.TabW,2)
        
        VLayout_menu = QVBoxLayout()
        VLayout_menu.setObjectName('VLayout_menu')
        VLayout_menu.setContentsMargins(6, 6, 6, 6)
        VLayout_menu.addLayout(HLayout_1)
        VLayout_menu.addLayout(HLayout_2)
        VLayout_menu.addLayout(HLayout_3)
        
        self.setLayout(VLayout_menu)
        
        self.Axes=Axes_singleton()
        self.Axes.Set_width(self.Canvas.width())
        self.Axes.Set_height(self.Canvas.height())
        self.p_size=2
        self.p_color='#0f0'
        self.l_size=1
        self.l_color='#000'
        self.p_brush='#00f'
        self.Render = Render(self.Axes, self.Canvas)
        
    
    def gen_btns(self, stgs):
        btn=None
        if 'name' in stgs.keys():
            btn=QPushButton(stgs['name'])
            if 'obj_name' in stgs.keys():
                btn.setObjectName(stgs['obj_name'])
            if 'property_name' in stgs.keys():
                btn.setProperty('name', stgs['property_name'])
            if 'property_type' in stgs.keys():
                btn.setProperty('type', stgs['property_type'])
            if 'tooltip' in stgs.keys():
                btn.setToolTip(stgs['tooltip'])
            if 'ico' in stgs.keys():
                btn.setIcon(QIcon(QPixmap(stgs['ico'])))
            if 'width' in stgs.keys():
                width=stgs['width']
                if 'height' in stgs.keys():
                    height=stgs['height']
                else:
                    height=width
                btn.setMinimumSize(width, height)
                btn.setMaximumSize(width, height)
            if 'shortcut' in stgs.keys():
                btn.setShortcut(stgs['shortcut'])
            if 'cmd' in stgs.keys():
                btn.clicked.connect(stgs['cmd'])
        return btn
    
    def Check_Edit(self):
        if os.path.exists(self.Edit_path.text()):
            self.Label_status.setText('Статус: файл существует.')
            self.Label_status.setStyleSheet("""#Label_status{
                                            color:#17730d;
                                        }""")
            self.Edit_path.setStyleSheet("""#Edit_path {
                                            color:#3c4f27;
                                            border:1px solid #006080;
                                            }
                                        #Edit_path:focus{
                                            color:#085409;
                                            border: 2px solid #085409;
                                        }""")
        else:
            self.Label_status.setText('Статус: такого файла нет.')
            self.Label_status.setStyleSheet("""#Label_status{
                                            color:#968806;
                                        }""")
            self.Edit_path.setStyleSheet("""#Edit_path{
                                            color:#959595;
                                            border:1px solid #000;
                                        }
                                        #Edit_path:focus{
                                            color:#000;
                                            border: 2px solid #006080;
                                        }""")
    
    def Choose_file(self):
        title='Выберите файл с картографическими данными'
        main_dir= os.path.dirname(os.path.abspath(__file__))
        format="Map file (*.txt)"   #"All Files (*);;Text Files (*.txt)"
        path = QFileDialog.getOpenFileName(self, title, main_dir, format)[0]
        path=path.replace('/','\\')
        self.Edit_path.setText(path)
        self.Load_file()
    
    def Load_file(self):
        path = str(self.Edit_path.text())
        path=path.replace('/','\\')
        self.Edit_path.setText(path)
        if os.path.exists(path)==False:
            path=path.split('\\')[-1]
            self.Label_status.setText('Статус: Файл '+str(path)+' не существует по указанному пути!')
            self.Label_status.setStyleSheet("""#Label_status{
                                            color:#968806;
                                        }""")
        else:
            data=[]
            with open(path, "r") as f:
                for line in f.readlines():
                    line=line.replace('\n', '')
                    #line=line.replace('\t', '')
                    #line=line.replace(',', ' ')
                    #line=line.replace('  ', ' ')
                    #line=line.replace('  ', ' ')
                    data.append(line.split(' '))
            data=self.Check_data(data)
            hm=data['len']
            vl=len(data['valid'])
            fl=len(data['failed'])
            if fl==0:
                self.Label_status.setText('Статус: Документ прочитан без ошибок.\nЧисло строк ('+str(hm)+').')
                self.Label_status.setStyleSheet("""#Label_status{
                                                color:#17730d;
                                            }""")
                self.GenTasks(data['valid'])
            else:
                if vl!=0:
                    self.Label_status.setText('Статус: Данные прочитаны частично!\nЧисло строк ('+str(hm)+'), прочитано ('+str(vl)+'), не читаемо ('+str(fl)+').')
                    self.Label_status.setStyleSheet("""#Label_status{
                                                    color:#968806;
                                                }""")
                    self.GenTasks(data['valid'])
                else:
                    self.Label_status.setText('Статус: Данные не прочитаны!\nЧисло строк ('+str(hm)+'), прочитано ('+str(vl)+'), не читаемо ('+str(fl)+').')
                    self.Label_status.setStyleSheet("""#Label_status{
                                                    color:#730d0d;
                                                }""")
    
    def Check_data(self, data):
        ans={}
        ans['len']=len(data)
        ans['valid']=[]
        ans['failed']=[]
        for line in data:
            line_val=True
            if self.Check_line(line):
                for el in line:
                    if not self.Check_elem(el):
                        line_val=False
                        break
            else:
                line_val=False
            if line_val==True:
                ans['valid'].append([float(i) for i in line])
            else:
                ans['failed'].append(line)
        return ans
    
    def Check_line(self, line):
        test=True
        if len(line)==0:
            test=False
        if test==True and len(line)%2==1:
            test=False
        return test
    
    def Check_elem(self, elem):
        test=True
        if elem=='' or elem =="":
            test=False
        if test==True:
            L=len(elem)
            for i in range(L):
                ch=elem[i]
                ch_i = ord(ch)
                """
                ASCII
                0-9 = 48-57
                - = 45
                . = 46
                rule ch!=47 and 45<=ch<=57
                """
                if test==True and (ch_i<45 or 57<ch_i or ch_i==47):
                    test=False
                    break
                """
                - = elem[0] -10 X 1-0 10- -
                """
                if test==True and ((ch_i==45 and i!=0) or (ch_i==45 and i==0 and L==1)):
                    test=False
                    break
                """
                . = elem[1:-1] 1.01 10.1 X .101 101.
                """
                if test==True and ch_i==46:
                    if i==0 or i==L-1:
                        test=False
                        break
        return test

    def GetPoints(self, data):
        type_f = len(data)
        data=[[data[i], data[i+1]] for i in range(0, type_f, 2)]
        if type_f==2:
            P=Point(pos_x=float(data[0][0]), pos_y=float(data[0][1]))
            P.Set_color(self.p_color)
            P.Set_size(self.p_size)
            return P
        elif type_f==4:
            L=Line()
            for line in data:
                L.Add(pos_x=float(line[0]), pos_y=float(line[1]),color=self.p_color,size=self.p_size)
                L.Set_color(self.l_color)
                L.Set_size(self.l_size)
            return L
        elif type_f>=6:
            P=Polygon()
            for line in data:
                P.Add(pos_x=float(line[0]), pos_y=float(line[1]),color=self.p_color,size=self.p_size)
                P.Set_color(self.p_brush)
                P.Set_line_color(self.l_color)
            P.CloseLine()
            return P
    
    def GenTasks(self, data):
        self.Render.clear()
        for line in data:
            points = self.GetPoints(line)
            self.Render.add_Obj(points)
        self.Render.changed=True
        self.Render.renderAll()
        

    
    def Save_file(self):
        print('Save file')
        
    
    
    def switch_btn(self, checked):
        link_btn = self.sender()
        name=link_btn.property('name')
        type=link_btn.property('type')
        print('switch_btn:',type,name)
        if type=='switch':
            if name=='grid':
                if checked==False:
                    self.Render.Axes_show()
                    self.Render.changed=True
                    self.Render.renderAll()
                else:
                    self.Render.Axes_show()
                print('axes_show:',self.Render.axes_show)
            if name=='move':
                if checked==False:
                    self.Canvas.movable=True
                else:
                    self.Canvas.movable=False
            if name=='rotate':
                if checked==False:
                    pass
                else:
                    pass
            if name=='select':
                if checked==False:
                    self.Canvas.f_select=True
                else:
                    self.Canvas.f_select=False
                self.Canvas.selectable()
        
        
    def toggle_btn(self, checked):
        link_btn = self.sender()
        name=link_btn.property('name')
        type=link_btn.property('type')
        print('toggle_btn:',type,name)
        if type=='toggle':
            if name=='point':
                if checked==False:
                    pass
                else:
                    pass
            if name=='line':
                if checked==False:
                    pass
                else:
                    pass
            if name=='polygon':
                if checked==False:
                    pass
                else:
                    pass
            if name=='rectangle':
                if checked==False:
                    pass
                else:
                    pass
            if name=='sphere':
                if checked==False:
                    pass
                else:
                    pass
            if name=='brush':
                if checked==False:
                    pass
                else:
                    pass
        
        
    def click_btn(self, checked):
        link_btn = self.sender()
        name=link_btn.property('name')
        type=link_btn.property('type')
        print('click_btn:',type,name)
        if type=='click':
            if name=='pen_size':
                if checked==False:
                    pass
                else:
                    pass
            if name=='color_select':
                if checked==False:
                    pass
                else:
                    pass
            if name=='copy':
                if checked==False:
                    pass
                else:
                    pass
            if name=='clear':
                self.Canvas.remove()
                
            if name=='zoom_in':
                self.Canvas.zoom_In()
                if checked==False:
                    pass
                else:
                    pass
            if name=='zoom_out':
                self.Canvas.zoom_Out()
                if checked==False:
                    pass
                else:
                    pass
            if name=='zoom_def':
                self.Canvas.zoom_default()
                #self.Render.centre_all()
                if checked==False:
                    pass
                else:
                    pass
            if name=='center':
                if checked==False:
                    pass
                else:
                    pass
            if name=='group':
                if checked==False:
                    pass
                else:
                    pass
    
    
    
    
    
    def btns_style_change(self, checked):
        link_btn = self.sender()
        name=link_btn.property('name')
        type=link_btn.property('type')
        # Switch Toggle btns
        if type=='toggle' and checked==False:
            for key in self.tab_btns[type].keys():
                if key!=name and self.tab_btns[type][key].isChecked()==False:
                    self.tab_btns[type][key].setChecked(True)
    






if __name__ == '__main__':
    
    app = QApplication([])
    app.setStyleSheet(STYLE_SHEET)
    
    myApp = MainWindow(title='Тестовая ГИС')
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
