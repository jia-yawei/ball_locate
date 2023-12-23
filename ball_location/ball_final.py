from PyQt5.QtWidgets import  QFrame,QTabWidget,QTableWidget,QVBoxLayout, QApplication, QMainWindow, QWidget, QGridLayout,QPushButton, QComboBox, QFileDialog, QLabel, QMessageBox, QLineEdit,QFormLayout 
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy import signal
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
import sys
import time
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QButtonGroup
from scipy.signal import find_peaks
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import os
#增加一个注释
def resource_path(relative_path):
    """ 获取资源路径 """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为 SimHei
plt.rcParams['axes.unicode_minus'] = False  # 设置支持负号

#创建主窗口类
class MainWindow(QMainWindow):
    """
    主窗口类，用于创建主窗口部件、布局、下拉框、按钮和图形区域，并实现按钮事件处理函数。
    """
    def __init__(self):
        super().__init__()  
        self.ax5 = None
        self.init_variables()
        # 设置窗口名称
        self.setWindowTitle("智能球定位分析系统V1.0")
        # 使用图标
        icon1_path = resource_path('ball_ico.ico')
        icon2_path = resource_path('open_file.png')
        # 设置图标
        self.setWindowIcon(QIcon(icon1_path))   
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        #设置主窗口背景
        self.central_widget.setStyleSheet("QWidget{background-color:rgb(220,220,220)};")  
        # 创建主窗口布局
        self.grid_layout = QGridLayout(self.central_widget)
        
        #创建三个标签
        self.box_label1 = QLabel('请选择加速度')
        self.box_label2 = QLabel('请选择角速度') 
        self.box_label3 = QLabel('请选择磁场强度') 

        #设置字体样式
        self.box_label1.setFont(QFont('黑体', 10, QFont.Bold))  
        self.box_label2.setFont(QFont('黑体', 10, QFont.Bold))  
        self.box_label3.setFont(QFont('黑体', 10, QFont.Bold))  

        # 创建下拉框
        self.combo_box_x1 = QComboBox()
        self.combo_box_x2 = QComboBox()
        self.combo_box_x3 = QComboBox()
        
        #创建三个垂直布局
        self.vbox_x1 = QVBoxLayout()
        self.vbox_x1.addStretch() 
        self.vbox_x1.addWidget(self.box_label1)
        self.vbox_x1.addWidget(self.combo_box_x1)
        self.vbox_x1.addStretch() 
        self.vbox_x1.setSpacing(4)
        self.vbox_x2 = QVBoxLayout() 
        self.vbox_x2.addStretch()    
        self.vbox_x2.addWidget(self.box_label2)  
        self.vbox_x2.addWidget(self.combo_box_x2)
        self.vbox_x2.addStretch() 
        self.vbox_x2.setSpacing(4)     
        self.vbox_x3 = QVBoxLayout()
        self.vbox_x3.addStretch()     
        self.vbox_x3.addWidget(self.box_label3)  
        self.vbox_x3.addWidget(self.combo_box_x3)
        self.vbox_x3.addStretch() 
        self.vbox_x3.setSpacing(4)     
        #设置下拉框的样式
        self.combo_box_x1.setStyleSheet("QComboBox{margin:3px};")   
        self.combo_box_x2.setStyleSheet("QComboBox{margin:3px};")   
        self.combo_box_x3.setStyleSheet("QComboBox{margin:3px};")  
        self.combo_box_x1.setFont(QFont('黑体', 12, QFont.Bold))    
        self.combo_box_x2.setFont(QFont('黑体', 12, QFont.Bold))    
        self.combo_box_x3.setFont(QFont('黑体', 12, QFont.Bold))       
        self.combo_box_x1.setFixedSize(150, 40) 
        self.combo_box_x2.setFixedSize(150, 40) 
        self.combo_box_x3.setFixedSize(150, 40) 

        # 创建按钮
        self.load_IMU_button = QPushButton('打开IMU文件')
        self.load_sound_button = QPushButton('打开声音文件')
        self.plot_IMU_button = QPushButton('绘制IMU波形')
        self.plot_sound_button = QPushButton('绘制声音波形')
        self.load_position_button = QPushButton('加载位置') 
        self.calculate_displacement_button = QPushButton('计算位移')
        self.set_reference_button = QPushButton('设为参考点')
        self.set_suspicious_button = QPushButton('设为可疑点')
        self.clear1_button = QPushButton('清空所有标记')  
        self.set_reference_button.setFixedSize(120, 30) 
        self.set_suspicious_button.setFixedSize(120, 30)
        self.clear1_button.setFixedSize(120, 30)

        #设置按钮的样式
        self.load_IMU_button.setFixedSize(200, 50)
        self.load_sound_button.setFixedSize(200, 50) 
        self.plot_IMU_button.setFixedHeight(50) 
        self.plot_sound_button.setFixedHeight(50)         
        self.load_position_button.setFixedHeight(50)    
        self.calculate_displacement_button.setFixedSize(200, 50)    
        self.set_reference_button.setFixedSize(200, 60) 
        self.set_suspicious_button.setFixedSize(200, 60)    
        self.clear1_button.setFixedSize(200,50)  
        self.load_IMU_button.setStyleSheet("QPushButton{margin:3px;font:10pt '黑体';color:white;background-color:rgb(87, 96, 111)};")
        self.load_sound_button.setStyleSheet("QPushButton{margin:3px;font:10pt '黑体';color:white;background-color:rgb(87, 96, 111)};")
        self.plot_IMU_button.setStyleSheet("QPushButton{margin:3px;font:10pt '黑体';color:black;background-color:rgb(223, 228, 234)};")    
        self.plot_sound_button.setStyleSheet("QPushButton{margin:3px;font:10pt '黑体';color:black;background-color:rgb(223, 228, 234)};")  
        self.load_position_button.setStyleSheet("QPushButton{background-color:rgb(135,206,235);font:15pt '宋体';}")
        self.calculate_displacement_button.setStyleSheet("QPushButton{background-color:rgb(205,133,63);font:15pt '宋体';}") 
        self.set_reference_button.setStyleSheet("QPushButton{background-color:rgb(100,149,237);color:white;font:15pt '宋体';}")   
        self.set_suspicious_button.setStyleSheet("QPushButton{background-color:rgb(47, 53, 66);color:white;font:15pt '宋体';}")  
        self.clear1_button.setStyleSheet("QPushButton{background-color:rgb(255,140,0);font:15pt '宋体';}")  
        self.calculate_displacement_button.setFixedHeight(60)
        #给按钮添加图标
        self.load_IMU_button.setIcon(QIcon(icon2_path))  
        self.load_sound_button.setIcon(QIcon(icon2_path))  
        #创建一个垂直布局
        self.v_layout3 = QVBoxLayout() 
        self.v_layout3.addWidget(self.set_reference_button) 
        self.v_layout3.addWidget(self.set_suspicious_button)   

        #创建标签
        self.label0 = QLabel('声音波形')
        self.label1 = QLabel('参考点：') 
        self.label2 = QLabel('可疑点：')  
        self.label3 = QLabel('相对位移：')
        #设置字体样式
        self.label0.setFont(QFont('黑体', 15, QFont.Bold))  
        self.label1.setFont(QFont('黑体', 15, QFont.Bold)) 
        self.label1.setStyleSheet("color:rgb(55, 66, 250);")  
        self.label2.setFont(QFont('黑体', 15, QFont.Bold))  
        self.label2.setStyleSheet("color:rgb(47, 53, 66);")   
        self.label3.setFont(QFont('黑体', 15, QFont.Bold))  
        self.label3.setStyleSheet("color:rgb(255, 0, 0);")    
        
        #创建文本框
        self.text1 = QLineEdit()    
        self.text2 = QLineEdit()    
        #设置文本框的样式
        self.text1.setFixedHeight(40)  
        self.text2.setFixedHeight(40)
        self.text1.setStyleSheet("QLineEdit{background-color:rgb(255, 255, 255);font:15pt '宋体';color:rgb(0, 0, 0);}")
        self.text2.setStyleSheet("QLineEdit{background-color:rgb(255, 255, 255);font:15pt '宋体';color:rgb(0, 0, 0);}") 
        #将文本框设置为只读
        self.text1.setReadOnly(True)    
        self.text2.setReadOnly(True)    

        #创建位移显示标签
        self.label4 = QLabel('') 
        self.label4.setFont(QFont('黑体', 15, QFont.Bold))
        self.label4.setFixedSize(100, 20) 
        self.line = QFrame()
        #设置水平线的样式加粗、颜色
        self.line.setFrameShape(QFrame.HLine)   
        self.line.setFrameShadow(QFrame.Sunken) 
        self.line.setStyleSheet("border:4px solid rgb(255, 0, 0);") 
        #创建一个垂直布局，将标签和水平线添加到布局中
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.label4)    
        self.v_layout.addWidget(self.line) 
         # 创建表单布局
        self.form1_layout = QFormLayout()  
        self.form1_layout.addRow(self.load_position_button)
        self.form1_layout.addRow(self.label1,self.text1) 
        self.form1_layout.addRow(self.label2,self.text2) 
        self.form1_layout.addRow(self.label3,self.v_layout) 

        #创建三个选择按钮
        self.radio_button1 = QRadioButton('角速度法定位')
        self.radio_button2 = QRadioButton('加速度半圈法定位')
        self.radio_button3 = QRadioButton('加速度比例法定位')    
        self.radio_button4 = QRadioButton('融合滤波法定位') 
        #设置按钮样式
        self.radio_button1.setStyleSheet("QRadioButton{font:12pt '宋体';color:rgb(0, 0, 0);}")  
        self.radio_button2.setStyleSheet("QRadioButton{font:12pt '宋体';color:rgb(0, 0, 0);}")  
        self.radio_button3.setStyleSheet("QRadioButton{font:12pt '宋体';color:rgb(0, 0, 0);}")
        self.radio_button4.setStyleSheet("QRadioButton{font:12pt '宋体';color:rgb(0, 0, 0);}")  
        #将三个按钮添加到一个按钮组中
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_button1, 1)  
        self.button_group.addButton(self.radio_button2, 2)  
        self.button_group.addButton(self.radio_button3, 3)  
        self.button_group.addButton(self.radio_button4, 4)  
        #设置按钮的宽度
        self.radio_button1.setFixedSize(250, 30)    
        self.radio_button2.setFixedSize(250, 30)    
        self.radio_button3.setFixedSize(250, 30)    
        self.radio_button4.setFixedSize(250, 30)    
        #设置按钮默认选中
        self.radio_button1.setChecked(True) 
        #创建垂直布局，将三个选择按钮添加到布局中
        self.v_layout2 = QVBoxLayout()
        self.v_layout2.addWidget(self.radio_button1)    
        self.v_layout2.addWidget(self.radio_button2)    
        self.v_layout2.addWidget(self.radio_button3)    
        self.v_layout2.addWidget(self.radio_button4)    

        #创建选项卡
        # 再添加一个选项卡部件命名为结果分析 
        self.tab_widget = QTabWidget()
        self.tab1 = QWidget()  
        self.tab2 = QWidget()
        self.tab3 = QWidget()      
        self.tab1_layout = QGridLayout(self.tab1)  
        self.tab2_layout = QGridLayout(self.tab2) 
        self.tab3_layout = QGridLayout(self.tab3)      
        self.tab_widget.addTab(self.tab1, "区间选择")
        self.tab_widget.addTab(self.tab2, "声音可视化分析")  
        self.tab_widget.addTab(self.tab3, "位移可视化分析")
          
        # 创建表格并添加到选项卡的布局中        
        self.tab1_table = QTableWidget()    
        self.tab1_layout.addWidget(self.tab1_table, 0, 0)     
        self.grid_layout.addWidget(self.tab_widget, 0, 3, 2, 2)   
        #设置在数据选项卡下有一个10行3列的表格
        self.tab1_table.setRowCount(10)
        self.tab1_table.setColumnCount(3)
        self.tab1_table.setHorizontalHeaderLabels(['参考点','可疑点','历经时间']) 
        #设置表格样式
        self.tab1_table.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:rgb(255, 255, 255);font:10pt '黑体';color:rgb(0, 0, 0);border:1px solid rgb(0, 0, 0);border-left:None;border-right:None;min-height:30px;min-width:100px;}")
        self.tab1_table.setFrameShape(QTableWidget.Box) 
        #加粗内部线框为2磅
        self.tab1_table.setStyleSheet("QTableWidget{border:1px solid rgb(0, 0, 0);}")     
        #设置表格布局，将10行3列的表格在数据选项卡中能够自适应
        self.tab1_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tab1_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  
        #在选项卡中增加四个新的绘图区域，放到可视化分析选项卡中
        # 创建图形区域
        self.figure5 = Figure() 
        self.canvas5 = FigureCanvas(self.figure5)     
        self.tab3_layout.addWidget(self.canvas5)
        self.figure6 = Figure() 
        self.canvas6 = FigureCanvas(self.figure6)   
        self.tab2_layout.addWidget(self.canvas6)      
        #设置绘图区域宽度
        self.canvas5.setFixedWidth(800)
        self.canvas6.setFixedWidth(800)   
        # 创建图形区域
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)
        self.figure4 = Figure()
        self.canvas4 = FigureCanvas(self.figure4)
        # 设置图形区域的大小
        self.canvas1.setFixedSize(800, 300)
        self.canvas2.setFixedSize(800, 300) 
        self.canvas3.setFixedSize(800, 300) 
        self.canvas4.setFixedSize(800, 300) 


    
        # 将按钮、下拉框、标签和图形区域添加到主布局中
        self.grid_layout.addLayout(self.vbox_x1, 0, 0)
        self.grid_layout.addWidget(self.canvas1, 0, 1) 
        self.grid_layout.addLayout(self.vbox_x2, 1, 0)
        self.grid_layout.addWidget(self.canvas2, 1, 1) 
        self.grid_layout.addLayout(self.vbox_x3, 2, 0)
        self.grid_layout.addWidget(self.canvas3, 2, 1)     
        self.grid_layout.addWidget(self.label0, 3, 0)
        self.grid_layout.addWidget(self.canvas4, 3, 1) 
        self.grid_layout.addWidget(self.clear1_button, 1, 2)    
        self.grid_layout.addWidget(self.load_IMU_button, 4, 0)
        self.grid_layout.addWidget(self.plot_IMU_button, 4, 1)
        self.grid_layout.addWidget(self.load_sound_button, 5, 0)
        self.grid_layout.addWidget(self.plot_sound_button, 5, 1)   
        self.grid_layout.addWidget(self.calculate_displacement_button, 4, 3)    
        #将表单布局添加到主窗口布局中
        self.grid_layout.addLayout(self.form1_layout, 2, 3, 1, 1)    
        #将存储参考点和可疑点按钮添加到主窗口布局中
        self.grid_layout.addLayout(self.v_layout3, 0, 2, 1, 1)   
        #将垂直布局添加到主窗口布局中
        self.grid_layout.addLayout(self.v_layout2, 3, 3, 1, 1)  
        
        # 绑定按钮事件
        self.load_IMU_button.clicked.connect(self.load_IMU_file)
        self.plot_IMU_button.clicked.connect(self.plot_IMU_data)
        self.load_sound_button.clicked.connect(self.load_sound_file)
        self.plot_sound_button.clicked.connect(self.plot_sound_data)
        self.set_reference_button.clicked.connect(self.on_click)    
        self.set_suspicious_button.clicked.connect(self.on_click)   
        self.clear1_button.clicked.connect(self.on_click)     
        self.load_position_button.clicked.connect(self.load_position) 
        self.calculate_displacement_button.clicked.connect(self.calculate_displacement)

        # 绑定鼠标悬停事件
        self.canvas1.mpl_connect('motion_notify_event', self.on_mouse_hover)
        self.canvas2.mpl_connect('motion_notify_event', self.on_mouse_hover)
        self.canvas3.mpl_connect('motion_notify_event', self.on_mouse_hover)
        self.canvas4.mpl_connect('motion_notify_event', self.on_mouse_hover)

        # 为图形区域添加鼠标单击事件处理函数
        self.canvas1.mpl_connect('button_press_event', self.on_mouse_click)
        self.canvas2.mpl_connect('button_press_event', self.on_mouse_click) 
        self.canvas3.mpl_connect('button_press_event', self.on_mouse_click) 
        self.canvas4.mpl_connect('button_press_event', self.on_mouse_click) 
    


    #定义刷新所有图形函数
    def refresh_all_canvases(self):
        self.canvas1.draw()
        self.canvas2.draw() 
        self.canvas3.draw() 
        self.canvas4.draw() 
    
    #定义计算位移的函数
    def calculate_displacement(self): 
        if self.ax5 is None:
            self.ax5 = self.figure5.add_subplot(111)  
        # 获取所有图例的文本
        legend_texts = [t.get_text() for t in self.ax5.legend_.texts] if self.ax5.legend_ else [] 
         #判断文本输入框中是否有数据，没有数据则提示，请填入参考点和可疑点
        if self.text1.text() == '' or self.text2.text() == '':
            QMessageBox.warning(self, "错误", "请填入参考点和可疑点")
            return  
        else :
            #获取文本输入框中的数据
            reference_point = float(self.text1.text())
            suspicious_point = float(self.text2.text())
            #获取第二个图像的时间戳 
            x2_time = self.IMU_data.iloc[:, 0]
        #判断三个选择按钮选择了哪一个，如果是第一个按钮，则计算角速度定位的位移
            if self.radio_button1.isChecked():
                #获取参考点和可疑点的数据
                #计算相对位移
                #这里参考点和可疑点是第二个图像的积分起点和终点，我需要将这个两个点之间对图像进行积分运算
                #获取第二个图像的数据
                x2_col = self.combo_box_x2.currentText()
                x2_data = self.IMU_data.loc[:, x2_col]  

                # 获取参考点和可疑点的索引值
                reference_index =  np.abs(x2_time - reference_point).argmin()
                suspicious_index = np.abs(x2_time - suspicious_point).argmin()  

                # 截取第二幅图像的数据和时间戳
                x2_data_sub = x2_data[reference_index:suspicious_index+1].reset_index(drop=True)
                x2_data_sub = np.deg2rad(x2_data_sub) * 0.05        
                x2_time_sub = x2_time[reference_index:suspicious_index+1] / 1000  # 将时间戳转换为秒 
                # 计算积分
                #x2_data_sub是速度，x2_time_sub是时间，对速度进行积分，将得到的一段一段位移累加并存在一个位移数组中   
                dis1 = np.zeros(len(x2_data_sub))   
                for i in range(0,len(x2_data_sub)-1):   
                    dis1[i+1]=dis1[i]+x2_data_sub[i]*(x2_time_sub[reference_index+i+1]-x2_time_sub[reference_index+i])  
                displacement = dis1[-1]     
                #将积分的值累加到数组中后，再将数组中的值进行积分运算  
                #integral = np.trapz(x2_data_sub, x2_time_sub)
                # 将结果显示在标签中,结果取绝对值，并保留两位小数
                self.label4.setText(str(round(abs(displacement),2)) + 'm') 
                #将速度和位移的图像绘制出来，显示在选项卡中的第一个图像区域中
                  
                # 如果图例中没有'角速度法'，则绘制图形
                if not '角速度法' in legend_texts:  
                    # 绘制图形  
                    self.ax5.plot(x2_time_sub, dis1, 'r-', label='角速度法')    
                    self.ax5.legend(loc='upper left')   
                    #刷新图形   
                    self.canvas5.draw()
                 
            elif self.radio_button2.isChecked():
                reference_index =  np.abs(x2_time - reference_point).argmin()
                suspicious_index = np.abs(x2_time - suspicious_point).argmin()  

                x1_col = self.combo_box_x1.currentText()
                x1_data1 = self.IMU_data.loc[:, x1_col]
                x1_data1_sub = x1_data1[reference_index:suspicious_index+1].reset_index(drop=True) 
                #x1_time_sub = self.IMU_data1.iloc[reference_index:suspicious_index+1, 0].values / 1000   
                peaks, _ = find_peaks(x1_data1_sub,height=0.5,distance=5)  # 找到所有峰值的索引
                troughs, _ = find_peaks(-x1_data1_sub,height=-0.5,distance=5)  # 找到所有谷值的索引
                #将参考点和标记点的索引以及峰值和谷值的索引合并
                all_index = np.concatenate((peaks, troughs, [0,len(x1_data1_sub) - 1]))   
                all_index = np.sort(all_index)   
                displacement = (len(all_index)-1) * 0.05*3.14
                self.label4.setText(str(round(abs(displacement),2)) + 'm')  
            elif self.radio_button3.isChecked():
                reference_index =  np.abs(x2_time - reference_point).argmin()
                suspicious_index = np.abs(x2_time - suspicious_point).argmin()  

                x1_col = self.combo_box_x1.currentText()
                x1_data2 = self.IMU_data.loc[:, x1_col]
                x1_data2_sub = x1_data2[reference_index:suspicious_index+1].reset_index(drop=True)
                x1_time2_sub = x2_time[reference_index:suspicious_index+1] / 1000
                x1_time2_sub = x1_time2_sub.reset_index(drop=True)  
                peaks, _ = find_peaks(x1_data2_sub,height=0.5,distance=8)  # 找到所有峰值的索引
                troughs, _ = find_peaks(-x1_data2_sub,height=-0.5,distance=8)  # 找到所有谷值的索引   
                #将参考点和标记点的索引以及峰值和谷值的索引合并
                all_index = np.concatenate((peaks, troughs, [0,len(x1_data2_sub) - 1]))  
                all_index = np.sort(all_index)  
                #计算相对位移   
                dis = np.zeros(len(x1_data2_sub))
                velocity = np.zeros(len(x1_data2_sub))  
                for i in range(0,len(all_index)-1):
                    y=abs(x1_data2_sub[all_index[i+1]]-x1_data2_sub[all_index[i]])

                    for j in range(all_index[i],all_index[i+1]):
                        
                        dy = abs(x1_data2_sub[j+1] - x1_data2_sub[j])
                        dis[j] = dy * 3.14 * 0.05 / y 
                        velocity[j] = dis[j] / (x1_time2_sub[j+1] - x1_time2_sub[j])       
                #将位移累加
                dis = np.cumsum(dis)      
                displacement = dis[-1]      
                self.label4.setText(str(round(abs(displacement),2)) + 'm') 
                #将位移的图像也绘制在选项卡中的第一个图像区域中
                # 绘制图形 
                if not '加速度比例法' in legend_texts:
                    self.ax5.plot(x1_time2_sub, dis, 'b-', label='加速度比例法')  
                    self.ax5.legend(loc='upper left')   
                    #刷新图形
                    self.canvas5.draw()    
                           
            elif self.radio_button4.isChecked():
                #对按钮1和按钮3中的位移进行卡尔曼融合滤波
                x2_col = self.combo_box_x2.currentText()
                x2_data = self.IMU_data.loc[:, x2_col]  

                # 获取参考点和可疑点的索引值
                reference_index =  np.abs(x2_time - reference_point).argmin()
                suspicious_index = np.abs(x2_time - suspicious_point).argmin()  

                x2_data_sub = x2_data[reference_index:suspicious_index+1].reset_index(drop=True)
                x2_data_sub = np.deg2rad(x2_data_sub) * 0.05        
                x2_time_sub = x2_time[reference_index:suspicious_index+1] / 1000  # 将时间戳转换为秒 
                # 计算积分
                #x2_data_sub是速度，x2_time_sub是时间，对速度进行积分，将得到的一段一段位移累加并存在一个位移数组中  
                dis1 = np.zeros(len(x2_data_sub))   
                for i in range(0,len(x2_data_sub)-1):   
                    dis1[i+1]=dis1[i]+x2_data_sub[i]*(x2_time_sub[reference_index+i+1]-x2_time_sub[reference_index+i])     
                #将积分的值累加到数组中后，再将数组中的值进行积分运算   
                
                x1_col = self.combo_box_x1.currentText()
                x1_data2 = self.IMU_data.loc[:, x1_col]
                x1_data2_sub = x1_data2[reference_index:suspicious_index+1].reset_index(drop=True)
                x1_time2_sub = x2_time[reference_index:suspicious_index+1] / 1000
                x1_time2_sub = x1_time2_sub.reset_index(drop=True)  
                peaks, _ = find_peaks(x1_data2_sub,height=0.5,distance=8)  # 找到所有峰值的索引
                troughs, _ = find_peaks(-x1_data2_sub,height=-0.5,distance=8)  # 找到所有谷值的索引   
                #将参考点和标记点的索引以及峰值和谷值的索引合并
                all_index = np.concatenate((peaks, troughs, [0,len(x1_data2_sub) - 1]))  
                all_index = np.sort(all_index)  
                #计算相对位移   
                dis = np.zeros(len(x1_data2_sub))  
                for i in range(0,len(all_index)-1):
                    y=abs(x1_data2_sub[all_index[i+1]]-x1_data2_sub[all_index[i]])

                    for j in range(all_index[i],all_index[i+1]):
                        
                        dy = abs(x1_data2_sub[j+1] - x1_data2_sub[j])
                        dis[j] = dy * 3.14 * 0.05 / y     
                #将位移累加
                dis = np.cumsum(dis) 
                #对位移进行卡尔曼滤波
                #dis1是角速度法定位的位移，dis是加速度法定位的位移
                x = np.zeros_like(dis1)
                P = np.zeros_like(dis)

                # 卡尔曼滤波器的噪声参数
                Q = 0.001
                R1 = 0.01
                R2 = 0.004

                # 对每个时间步进行卡尔曼滤波
                for i in range(len(dis1)):
                    # 预测
                    x_pred = x[i-1] if i > 0 else 0
                    P_pred = P[i-1] + Q if i > 0 else 1

                    # 更新步骤1：使用dis1的测量值
                    K1 = P_pred / (P_pred + R1)
                    x[i] = x_pred + K1 * (dis1[i] - x_pred)
                    P[i] = (1 - K1) * P_pred

                    # 更新步骤2：使用dis的测量值
                    K2 = P[i] / (P[i] + R2)
                    x[i] = x[i] + K2 * (dis[i] - x[i])
                    P[i] = (1 - K2) * P[i]
                displacement = x[-1]
                self.label4.setText(str(round(abs(displacement),2)) + 'm')      
                #将位移的图像也绘制在选项卡中的第一个图像区域中
                # 绘制图形
                if not '融合滤波法' in legend_texts:
                    self.ax5.plot(x1_time2_sub, x, 'g-', label='融合滤波法')  
                    self.ax5.legend(loc='upper left')   
                    #刷新图形
                    self.canvas5.draw() 

    # 定义鼠标单击事件处理函数，用于在图形上添加标记点
    def on_mouse_click(self, event):
        """
        鼠标单击事件处理函数，用于在图形上添加标记。
        """
        if event.button == 1:
            # 获取鼠标单击的坐标
            x, y = event.xdata, event.ydata
            
            #在当前位置绘制一个标记
            maker, = event.inaxes.plot(x, y, 'ro')  
            self.markers.append(maker) 
            #刷新图形
            event.canvas.draw() 
            self.marker_x = round(x,2) 
            for marker in self.markers:
        # 检查每个标记是否已经被添加为参考点或可疑点
                if '参考点' not in marker.get_label() and '可疑点' not in marker.get_label() and self.markers[-1] != marker:
            # 如果一个标记没有被添加为参考点或可疑点，那么将它从 self.markers 列表中移除，并从图表中删除这个标记
                    marker.remove()
                    self.markers.remove(marker)
                    #刷新所有图形
                    self.refresh_all_canvases()
            #如果单击右键则依次往前清除上一步的标记，但不清除曲线
        elif event.button == 3 and self.markers:
                marker = self.markers.pop()    
                marker.remove()
                event.canvas.draw() 
              

            
    #定义单击按钮的槽函数
    def on_click(self):
        #如果点击的是设为参考点按钮，则将当前标记的横坐标填入参考点那一列的第一行表格中
        if self.sender() == self.set_reference_button and self.markers:
            if '可疑点' in self.markers[-1].get_label():
                #弹出提示窗口   
                QMessageBox.warning(self, "错误", "这个点已经被添加为可疑点，不能再添加为参考点")
                return
            #将标记点的横坐标填入参考点那一列的第一行表格中
            else:
                self.tab1_table.setItem(self.reference_count,0,QTableWidgetItem(str(self.marker_x)))
                #将红色标记改为参考点1，后面如果再次添加为参考点，这个值依次加1
                reference_annotation = self.markers[-1].axes.annotate('参考点' + str(self.reference_count + 1), (self.marker_x, self.markers[-1].get_ydata()[0])) 
                self.reference_annotations.append(reference_annotation)
                self.markers[-1].set_label('参考点'+str(self.reference_count+1))   
                #self.markers[-1].axes.annotate('参考点'+str(self.reference_count+1), (self.marker_x, self.markers[-1].get_ydata()[0]))
                #刷新所有图形
                self.refresh_all_canvases()
                self.reference_count += 1
                if self.tab1_table.item(self.reference_count-1, 0) is not None and self.tab1_table.item(self.reference_count-1, 1) is not None:
                    # 获取第一列和第二列的值
                    value1 = float(self.tab1_table.item(self.reference_count-1, 0).text())
                    value2 = float(self.tab1_table.item(self.suspicious_count-1, 1).text())
                    # 计算它们的差
                    difference = round((value2 - value1)/1000,2)
                    # 将结果设置为第三列的值
                    self.tab1_table.setItem(self.reference_count-1, 2,  QTableWidgetItem(str(difference)+' s'))
                else:  
                    return  
        #如果点击的是设为可疑点按钮，则将当前标记的横坐标填入可疑点那一列的第一行表格中
        elif self.sender() == self.set_suspicious_button and self.markers:
            if '参考点' in self.markers[-1].get_label():
                QMessageBox.warning(self, "错误", "这个点已经被添加为参考点，不能再添加为可疑点")
                return
            else:
                self.tab1_table.setItem(self.suspicious_count,1,QTableWidgetItem(str(self.marker_x)))
                suspicious_annotation=self.markers[-1].axes.annotate('可疑点' + str(self.suspicious_count + 1), (self.marker_x, self.markers[-1].get_ydata()[0]))   
                self.suspicious_annotations.append(suspicious_annotation)   
                self.markers[-1].set_label('可疑点'+str(self.suspicious_count+1))   
                #self.markers[-1].axes.annotate('可疑点'+str(self.suspicious_count+1), (self.marker_x, self.markers[-1].get_ydata()[0]))
                #刷新所有图形
                self.refresh_all_canvases() 
                self.suspicious_count += 1  
                if self.tab1_table.item(self.suspicious_count-1, 0) is not None and self.tab1_table.item(self.suspicious_count-1, 1) is not None:
                    # 获取第一列和第二列的值
                    value1 = float(self.tab1_table.item(self.reference_count-1, 0).text())
                    value2 = float(self.tab1_table.item(self.suspicious_count-1, 1).text())
                    # 计算它们的差
                    difference = round((value2 - value1)/1000,2)
                    # 将结果设置为第三列的值
                    self.tab1_table.setItem(self.suspicious_count-1, 2,  QTableWidgetItem(str(difference)+' s')) 
                else:
                    return
        #如果点击的是清空按钮，则将所有标记点的信息清空
        elif self.sender() == self.clear1_button and self.markers:
            #清空表格内全部内容
            self.tab1_table.clearContents() 
            #清空所有标记点
            markers_copy = self.markers.copy()  
            for marker in markers_copy: 
                marker.remove()
                self.markers = []   
            for reference_annotation in self.reference_annotations: 
                reference_annotation.remove()
                self.reference_annotations = [] 
            for suspicious_annotation in self.suspicious_annotations:       
                suspicious_annotation.remove()
                self.suspicious_annotations = []
            #刷新所有图形
            self.refresh_all_canvases()
            self.reference_count = 0    
            self.suspicious_count = 0   
            #清空文本框和标签
            self.text1.setText('')  
            self.text2.setText('')  
            self.label4.setText('') 
        else:
            pass    

    def on_mouse_hover(self, event):
            """
            鼠标悬停事件处理函数，用于显示当前坐标。
            """
            if event.inaxes:
                x, y = event.xdata, event.ydata
                self.statusBar().showMessage(f'x={x:.2f}, y={y:.2f}')
                #event.canvas.draw_idle()          
    def load_IMU_file(self):
            """
            加载IMU文件，读取CSV文件数据，并将数据列名添加到下拉框中。
            """
            # 打开文件选择对话框
            file_IMU_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'CSV Files (*.csv)')

            # 如果用户选择了文件
            if file_IMU_path:
                # 读取文件
                self.IMU_data = pd.read_csv(file_IMU_path)

                # 清空下拉框
                self.combo_box_x1.clear()
                self.combo_box_x2.clear()
                self.combo_box_x3.clear()

                # 添加下拉框选项,将部分列名添加到下拉框中
                #设置第一个下拉框的三项分别为文件中的2，3，4列
                self.combo_box_x1.addItems(self.IMU_data.columns[1:4])
                #设置第二个下拉框的三项分别为文件中的5，6，7列  
                self.combo_box_x2.addItems(self.IMU_data.columns[4:7])  
                #设置第三个下拉框的三项分别为文件中的8，9，10列 
                self.combo_box_x3.addItems(self.IMU_data.columns[7:10]) 
    def load_sound_file(self):
            """
            加载声音文件，读取CSV文件数据，并将数据列名添加到下拉框中。
            """
            # 打开文件选择对话框
            file_sound_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'CSV Files (*.csv)')

        # 如果用户选择了文件
            if file_sound_path:
            # 读取文件
                self.sound_data = pd.read_csv(file_sound_path, header=None, index_col=None)
    
    def plot_IMU_data(self):
        """
        绘制图形，根据下拉框选择的列名，获取对应的列数据，并绘制图形。
        """
        # 获取选择的列名
        x1_col = self.combo_box_x1.currentText()
        x2_col = self.combo_box_x2.currentText()
        x3_col = self.combo_box_x3.currentText()

        # 获取选择的列数据
        if not hasattr(self, 'IMU_data')or self.IMU_data is None:
            QMessageBox.warning(self, "错误", "请正确加载IMU文件")
            return
        x1_data = self.IMU_data.loc[:, x1_col]
        x2_data = self.IMU_data.loc[:, x2_col]
        x3_data = self.IMU_data.loc[:, x3_col]

        # 绘制图形
        self.figure1.clear()
        self.figure2.clear()
        self.figure3.clear()

        ax1 = self.figure1.add_subplot(111)
        ax1.plot(self.IMU_data.iloc[:, 0], x1_data)
        self.figure1.tight_layout()

        ax2 = self.figure2.add_subplot(111)
        ax2.plot(self.IMU_data.iloc[:, 0], x2_data)
        self.figure2.tight_layout() 

        ax3 = self.figure3.add_subplot(111)
        ax3.plot(self.IMU_data.iloc[:, 0], x3_data)
        self.figure3.tight_layout() 

        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()

    def plot_sound_data(self):
        # 获取声音数据并将数据转成一维数组
        if not hasattr(self, 'sound_data')or self.sound_data is None:
            QMessageBox.warning(self, "错误", "请正确加载声音文件")
            return
        
        sound_dt = self.sound_data.iloc[0:, 2:]  # 取出声音数据
        sound_dt_array = pd.to_numeric(sound_dt.values.ravel(), errors='coerce')  # 转化成一维数组并转换为数字

        # 定义无效值列表
        invalid_values = [-32768, '其他无效值']

         # 将一维数组中的无效值替换为nan
        for invalid_value in invalid_values:
            sound_dt_array = np.where(sound_dt_array == invalid_value, np.nan, sound_dt_array)
        # 将nan替换为前后两个值的平均值
        sound_dt_array = pd.Series(sound_dt_array).interpolate().values
         
        #取出时间戳并在声音时间戳数组最后增加一个元素

        sound_time = self.sound_data.iloc[1:, 0].values
        end_sound_data = sound_time[-1] + (sound_time[-1] - sound_time[-2])
        sound_time=np.append(sound_time,end_sound_data) 
        sound_time=np.array(sound_time) 
        
        #在声音时间戳之间增加元素，保证和转化后的声音数据数组长度一致
        #插入元素数量
        num_sound_inserts = 510
       
        #创建一个空列表保存扩充后的时间戳
        sound_time_inserts = []
         
        #插入元素
        for i in range(len(sound_time)-1):
            sound_time_inserts.extend(np.linspace(sound_time[i],sound_time[i+1],num_sound_inserts+2,endpoint=False))   
        
        #sound_time_inserts.append(sound_time_inserts[-1])
        sound_time_inserts=np.array(sound_time_inserts) 
        


        #截取声音时间戳和声音数据数组的长度，保证两者长度一致
        
        min_length = min(len(sound_time_inserts), len(sound_dt_array))
        sound_time_inserts = sound_time_inserts[:min_length]
        sound_dt_array = sound_dt_array[:min_length]
        
        #绘制图形
        self.figure4.clear()
        ax4 = self.figure4.add_subplot(111)
        ax4.plot(sound_time_inserts,sound_dt_array) 
        self.figure4.tight_layout()    
        
        # 添加导航工具栏
        toolbar = NavigationToolbar(self.canvas4, self)
        self.grid_layout.addWidget(toolbar, 6, 1)
        self.canvas4.draw()

        #清除图形
        self.figure6.clear()   
        
        # 绘制图形
        ax6 = self.figure6.add_subplot(111)
        # 清理声音信号
        sound_dt_array = sound_dt_array[~np.isnan(sound_dt_array)]
        # 计算声音信号的频谱
        frequencies, _, Sxx = signal.spectrogram(sound_dt_array, fs=5200)
        # 重采样sound_time_inserts
        sound_time_inserts_resampled = np.linspace(sound_time_inserts.min(), sound_time_inserts.max(), Sxx.shape[1]) 
        epsilon = 1e-10  # 一个非零的小数
        Sxx = np.where(Sxx == 0, epsilon, Sxx)  # 将Sxx中的零值替换为epsilon    
        # 绘制时频图
        ax6.pcolormesh(sound_time_inserts_resampled, frequencies, 10 * np.log10(Sxx), shading='gouraud')

        # 刷新图形
        self.canvas6.draw()

    
    #定义一个加载位置的函数
    def load_position(self):
            
            #判断表格中是否有数据
            if self.tab1_table.item(0,0) is None and self.tab1_table.item(0,1) is None:
                QMessageBox.warning(self, "错误", "请先添加标记点和可疑点 ")
                return     
            else:
                selected_items = self.tab1_table.selectedItems()
                #判断是否选中表格中的数据
                if not selected_items:
                    #弹出提示窗口
                    QMessageBox.information(self, "提示", "请先选中表格中的数据")

                    return   
                else:
                    column_index = self.tab1_table.column(selected_items[0])
                    if column_index == 0:
                        self.text1.setText(selected_items[0].text())
                    elif column_index == 1:
                        self.text2.setText(selected_items[0].text())       
    def init_variables(self):
    # 初始化数据
        self.IMU_data = None
        self.sound_data = None
        self.markers = []
        self.marker_x = None
        self.reference_count = 0 
        self.suspicious_count = 0 
        self.reference_annotations = [] 
        self.suspicious_annotations = []       

if __name__ == '__main__':
    # 使用背景图片
    background_path = resource_path('launch_imag.png')
    app = QApplication(sys.argv)
    # 创建一个启动窗口
    splash = QSplashScreen(QPixmap(background_path)) 
    splash.show()      
    app.processEvents()
    time.sleep(1)
    window = MainWindow()
    # 初始化变量
    window.init_variables()   
    window.show()
    # 关闭启动窗口
    splash.finish(window)
    sys.exit(app.exec())
