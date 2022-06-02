# -*- coding: utf-8 -*-
"""
Created on Wed April 13 10:57:59 2022

@author: wwq
"""

import HotelInfo 
import DataAnal

import tkinter as tk
from tkinter import ttk

import tkinter.messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #matplotlib图入画布
import difflib #模糊匹配

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #成员变量
        self.HotelInfo = HotelInfo.ManaHotelInfo() #酒店信息
        self.sysInfo = HotelInfo.SysConfiguration() 
        self.hot = HotelInfo.Hotel("") #当前处理的酒店信息
        
        menubar = tk.Menu(self)
        self.lastrow = 0
        
        #定义“文件”菜单项及其子菜单
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file)
        file.add_command(label="读入数据",command=self.loadData )
        file.add_command(label="保存数据",command=self.saveData)
        file.add_separator()
        file.add_command(label="退出", command=self.quit)
        
        #定义“编辑”菜单项及其子菜单
        edit = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit)
        edit.add_command(label="新增记录", command=self.add)
        edit.add_command(label="删除记录", command=self.delete)
        edit.add_command(label="修改记录", command=self.mod)
        
        #定义数据分析菜单项及其子菜单
        anal = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="数据分析", menu=anal)
        anal.add_command(label="评分分析", command=self.score_anal)
        anal.add_command(label="房价分析", command=self.price_anal)
        
        #定义“帮助”菜单项及其子菜单
        help = tk.Menu(menubar, tearoff=0)
        help.add_command(label="About")
        menubar.add_cascade(label="帮助", menu=help)
        
        # 定义区域，把全局分为上中下三部分
        self.frame_top = tk.Frame(width=500, height=50)
        self.frame_center = tk.Frame(width=500, height=200)
        self.frame_bottom = tk.Frame(width=500, height=50)
        
        # 定义数据区域，查询
        self.lb_id = tk.Label(self.frame_top, text="酒店名：")
        self.nameStr = tk.StringVar().set('')
        self.ent_name = tk.Entry(self.frame_top, textvariable=self.nameStr)
        self.btn_query = tk.Button(self.frame_top, text="   查 询   ", command=self.query)            
        self.lb_id.grid(row=0, column=0, padx=25, pady=10)
        self.ent_name.grid(row=0, column=1, padx=5, pady=10)
        self.btn_query.grid(row=0, column=2, padx=40, pady=10)
        
        # 定义列表新数据区域
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=8, columns=self.sysInfo.infoCol)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=tk.VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)
        # 表格的标题    
        for col,coltxt in zip(self.sysInfo.infoCol,self.sysInfo.colname):
            self.tree.column(col, width=75, anchor="center")
            self.tree.heading(col, text=coltxt)
    

        # 调用方法获取表格内容插入及树基本属性设置
        self.tree["selectmode"] = "browse"
        #self.get_tree()
        self.tree.grid(row=0, column=0, sticky=tk.NSEW, ipadx=1)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)
        self.tree.bind('<ButtonRelease-1>', self.treeviewClick) #绑定单击事件 
        
        #新增，修改，删除按钮
        self.btn_add = tk.Button(self.frame_bottom, text="   新增   ", command=self.add)
        self.btn_mod = tk.Button(self.frame_bottom, text="   修改   ", command=self.mod)
        self.btn_delete = tk.Button(self.frame_bottom, text="   删除   ", command=self.delete)
        self.btn_add.grid(row=0, column=0, padx=35, pady=10)
        self.btn_mod.grid(row=0, column=1, padx=35, pady=10)
        self.btn_delete.grid(row=0, column=2, padx=35, pady=10)
        
        # 定义整体区域
        self.frame_top.grid(row=0, column=0, padx=60, pady=20)
        self.frame_center.grid(row=1, column=0, padx=60, ipady=1)
        self.frame_bottom.grid(row=2, column=0, padx=60)
        self.frame_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        # 窗体设置
        self.center_window(500, 370)
        self.title('酒店信息分析系统')
        self.config(menu=menubar)
        self.resizable(False, False)
        self.mainloop()
        
    #从文件中读取信息记录到系统中
    def loadData(self):
        #从系统配置中取出文件名
        txtName = self.sysInfo.hotFile
        res = self.HotelInfo.loadFile(txtName)
        if( res != 1 ):
            tk.messagebox.showerror(title='提示', message=res)
            return

        #显示在Treeview中        
        for hotel in self.HotelInfo.info:            
            infoShow = self.getTreeItem(hotel)
            self.tree.insert("", "end", values=infoShow) 
    
    #用系统的记录重写文件
    def saveData(self):
        #从系统配置中取出文件名
        txtName = self.sysInfo.hotFile
        res = self.HotelInfo.saveFile(txtName)
        if( res != 1 ):
            tk.messagebox.showerror(title='错误', message=res)
        else:
            tk.messagebox.showinfo(title='提示', message="已成功保存到文件！")       
    
    #将当前酒店信息生成为可添加到Treeview中的列表变量
    def getTreeItem(self, hot):
        infoShow = [hot.name] + hot.get_Info()
        return infoShow      
    
    #响应Treeview单击事件，将选中行信息显示到编辑区域
    def treeviewClick(self, event):
        #只处理选中的第一行数据，赋给当前处理的学生记录curStu
        for item in self.tree.selection():
            item_text = self.tree.item(item,"values")
            #显示当前记录    
            self.ent_name.delete(0,'end')
            self.ent_name.insert(0,item_text[0])
    
    #根据输入酒店名查询信息并显示弹窗1            
    def query(self):
        name = self.ent_name.get()
        
        names = []
        for item in self.HotelInfo.info:
            names.append(item.name)
        name = difflib.get_close_matches(name, names,3, cutoff=0.5)
        if name == []:
            tk.messagebox.showerror(title='错误', message="此酒店不存在")
        HotInfo = self.HotelInfo.queryHot(name[0])
        if( HotInfo !=-1) :
            win = Window_edit(self,HotInfo.name)
            win.UI(1)
        else:
            tk.messagebox.showerror(title='错误', message="此酒店不存在")
        return
    
    #新增
    def add(self):
        
        win = Window_edit(self,1)
        win.UI(2)
        #self.tree.selection()
        #child_id = self.tree.get_children()[-1]
        #self.tree.focus(child_id)
        #self.tree.selection_set(child_id)
        
        #self.tree.selection_set(self.tree.tag_has(self.HotelInfo.info[-1].name))
        return
    
    #修改
    def mod(self):
        name = self.ent_name.get()
        names = []
        for item in self.HotelInfo.info:
            names.append(item.name)
        name = difflib.get_close_matches(name, names,3, cutoff=0.5)
        
        if name == []:
            tk.messagebox.showerror(title='错误', message="此酒店不存在")

        else:
            HotInfo = self.HotelInfo.queryHot(name[0])
            if( HotInfo !=-1) : #酒店存在
                win = Window_edit(self,HotInfo.name)
                win.UI(3)
            else:  
                #酒店不存在
                tk.messagebox.showerror(title='错误', message="此酒店不存在")
        return
    
    #删除Treeview选中信息
    def delete(self):
        name = self.ent_name.get()
        if tk.messagebox.askyesno(title='提示', message='是否删除'+name+'信息？') :
            self.HotelInfo.delHotInfo(name)
            item = self.tree.selection()[0]
            self.tree.delete(item)
        return
    
    #评分分析
    def score_anal(self):
        Window_anal(self,1)
        return
    
    #房价分析
    def price_anal(self):
        Window_anal(self,2)
        return
    
    # 窗体居中
    def center_window(self, width, height):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        # 宽高及宽高的初始点坐标
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(size)

    def quit(self):
        self.destroy()
        
class Window_edit(tk.Toplevel):
    def __init__(self,parent,name):
        super().__init__()
        
        self.parent = parent 
        self.name = name
        
    def UI(self,func):
        # 定义区域，把全局分为上下三部分
        self.frame_center = tk.Frame(self,width=300, height=200)
        self.frame_bottom = tk.Frame(self,width=300, height=50)
        
        # 定义界面设计：信息显示
        lb_name = tk.Label(self.frame_center, text="酒店名：")
        self.var_name = tk.StringVar()
        self.ent_name = tk.Entry(self.frame_center,textvariable=self.var_name)

        lb_name.grid(row=0, column=0, padx=15, pady=10,sticky=tk.W)
        self.ent_name.grid(row=0, column=1, padx=10, pady=10)
        
        lb_time = tk.Label(self.frame_center, text="装修时间：")
        self.var_time = tk.StringVar()
        self.cmb_time = ttk.Combobox(self.frame_center,textvariable=self.var_time, width=17) #装修时间：下拉列表
        time_list = []
        for i in range(22):
            time_list.append(2001+i)
        self.cmb_time['value'] = time_list
        lb_time.grid(row=1, column=0, padx=15, pady=10,sticky=tk.W)
        self.cmb_time.grid(row=1, column=1, padx=10, pady=10)
        
        lb_num = tk.Label(self.frame_center, text="房间数：")
        self.var_num = tk.StringVar()
        self.ent_num = tk.Entry(self.frame_center,textvariable=self.var_num)
        lb_num.grid(row=2, column=0, padx=15, pady=10,sticky=tk.W)
        self.ent_num.grid(row=2, column=1, padx=10, pady=10)
        
        lb_price = tk.Label(self.frame_center, text="平均房价：")
        self.var_price = tk.StringVar()
        self.ent_price = tk.Entry(self.frame_center,textvariable=self.var_price)
        lb_price.grid(row=3, column=0, padx=15, pady=10,sticky=tk.W)
        self.ent_price.grid(row=3, column=1, padx=10, pady=10)
        
        lb_score = tk.Label(self.frame_center, text="评分：")
        self.var_score = tk.StringVar()
        self.ent_score = tk.Entry(self.frame_center,textvariable=self.var_score)      
        lb_score.grid(row=4, column=0, padx=15, pady=10,sticky=tk.W)
        self.ent_score.grid(row=4, column=1, padx=10, pady=10)
        
          
        # 定义界面设计：按钮
        btn_save = tk.Button(self.frame_bottom,text = '保存',command = lambda :self.saveData(func))
        btn_save.grid(row=5, column=0,padx=25, pady=10)
        
        btn_reset = tk.Button(self.frame_bottom,text = '重置',command = self.reset)
        btn_reset.grid(row=5, column=1,padx=25, pady=10)
        
        btn_return = tk.Button(self.frame_bottom,text = '返回',command = self.back)
        btn_return.grid(row=5, column=2,padx=25, pady=10)

        #查询/修改
        if func==1:
            self.query()
            btn_save['state']='disabled'
            btn_reset['state']='disabled'
        elif func==3:
            self.inputInfo()
        
        # 定义整体区域
        self.frame_center.grid(row=0, column=0, padx=20, pady=20)
        self.frame_bottom.grid(row=1, column=0, padx=20)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
        
        # 窗体设置
        self.center_window(300, 300)
        self.title('酒店数据编辑窗口')
        self.resizable(False, False)
        self.mainloop()
    
    #查询/修改信息录入
    def inputInfo(self):
        name = self.name
        #name = self.parent.ent_name.get()
        HotInfo = self.parent.HotelInfo.queryHot(name)
        self.var_name.set(HotInfo.name)
        self.var_time.set(HotInfo.Info[0])
        self.var_num.set(HotInfo.Info[1])
        self.var_price.set(HotInfo.Info[2])
        self.var_score.set(HotInfo.Info[3])
        
    #只读状态
    def change_state(self):
        self.ent_name.configure(state='readonly')
        self.cmb_time.configure(state='disabled') #禁用
        self.ent_num.configure(state='readonly')
        self.ent_price.configure(state='readonly')
        self.ent_score.configure(state='readonly')
        
    #主窗口查询
    def query(self):
        self.inputInfo()
        self.change_state()
    
    
    #检查数据合法性
    def checkData(self):
        if (eval(self.ent_num.get()) % 1 == 0 
        and eval(self.ent_score.get()) >= 1 
        and eval(self.ent_score.get()) <= 5):
            return 0        
        tk.messagebox.showerror(title='错误', message="数据不合法，请修改")
        return -1
    
    #保存数据
    def saveData(self,func):
        if func ==1: #查询状态，无响应
            return
        #获取添加酒店信息
        name = self.ent_name.get()
        try:
            time = eval(self.cmb_time.get())
            num = eval(self.ent_num.get())
            price = float(self.ent_price.get())
            score = float(self.ent_score.get())
        except Exception as e:
            print(e)
        cd = self.checkData()
        
        if cd != -1:
            hot = self.parent.HotelInfo.queryHot(name)
            if( hot != -1) : #判断该酒店是否存在
                #存在，是否修改已有信息
                if tk.messagebox.askyesno(title='提示', message='是否修改该酒店信息？') :
                    hot.Info = [time,num,price,score]
                    self.parent.HotelInfo.updateHotInfo(hot) #更新酒店信息
                    infoUpdate = self.parent.getTreeItem(hot)
                    #更新Treeview中信息
                    item = self.parent.tree.selection()[0]
                    self.parent.tree.item( item, values=infoUpdate)
                    tk.messagebox.showinfo(title='提示', message="保存成功！")
                    Window_edit.destroy(self)
                    return 
                return  #否，不修改
            else:
                #不存在，添加
                hot = HotelInfo.Hotel(name)
                hot.Info = [time,num,round(price,1),round(score,1)]
                self.parent.HotelInfo.addHotInfo(hot)
                infoShow = self.parent.getTreeItem(hot)
                self.parent.tree.insert("", 0, values=infoShow) #在主界面treeview第一行插入显示
                tk.messagebox.showinfo(title='提示', message="保存成功！")
                #添加信息在原treeview高亮
                child_id = self.parent.tree.get_children()[0]
                self.parent.tree.focus(child_id)
                self.parent.tree.selection_set(child_id)
                #主界面输入框显示
                for item in self.parent.tree.selection():
                    item_text = self.parent.tree.item(item,"values")
                    #显示当前记录    
                    self.parent.ent_name.delete(0,'end')
                    self.parent.ent_name.insert(0,item_text[0])
                    
                Window_edit.destroy(self)
                return 
        return 
    
    
    #重置数据
    def reset(self):
        self.ent_name.delete(0, 'end')
        self.cmb_time.delete(0, 'end') #禁用
        self.ent_num.delete(0, 'end')
        self.ent_price.delete(0, 'end')
        self.ent_score.delete(0, 'end')
        return
    
    #返回
    def back(self):
        Window_edit.destroy(self)
        return
    
    # 窗体居中
    def center_window(self, width, height):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        # 宽高及宽高的初始点坐标
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(size)
        
    
class Window_anal(tk.Toplevel):
    def __init__(self,parent,func):
        super().__init__()
        
        self.parent = parent 
        
        self.HotAnal = DataAnal.ManaHotelAnalysis()
        
        # 定义区域，把全局分为上下两部分
        self.frame_top = tk.Frame(self,width=500, height=50)
        self.frame_bottom = tk.Frame(self,width=500, height=200)
        
        #题目
        self.var_type = tk.StringVar()
        self.ent_type = tk.Entry(self.frame_top,textvariable=self.var_type,justify='center',font = "Helvetica 12 bold")
        self.ent_type.grid(row = 0,column = 0,columnspan=4,padx=60,ipadx=100,sticky=tk.N)
        self.ent_type.configure(state='readonly')
        
        # 均值，方差
        #控件
        self.lb_avg = tk.Label(self.frame_top, text="均值：")
        self.var_avg = tk.StringVar()
        self.ent_avg = tk.Entry(self.frame_top,textvariable=self.var_avg,width=10)
        self.lb_var = tk.Label(self.frame_top, text="方差：")
        self.var_var = tk.StringVar()
        self.ent_var = tk.Entry(self.frame_top,textvariable=self.var_var,width=10)
        #位置
        self.lb_avg.grid(row=1, column=0, padx=10, pady=10,sticky=tk.N)
        self.ent_avg.grid(row=1, column=1, padx=10, pady=10,sticky=tk.W)
        self.lb_var.grid(row=1, column=2, padx=10, pady=10,sticky=tk.N)
        self.ent_var.grid(row=1, column=3, padx=10, pady=10,sticky=tk.W)
       
        #只读状态
        self.ent_avg.configure(state='readonly')
        self.ent_var.configure(state='readonly')
        
        #图像
        self.cv = tk.Canvas(self.frame_bottom,bg = 'white')

        self.loadData() #读入数据
        if func == 1:
            self.score_anal()
        else:
            self.price_anal()
        
        # 定义整体区域
        self.frame_top.grid(row=0, column=0, padx=60, pady=20)
        self.frame_bottom.grid(row=1, column=0, padx=60)
        self.frame_top.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)
        
        # 窗体设置
        self.center_window(600, 420)
        self.title('数据分析窗口')
        self.resizable(False, False)
        self.mainloop()
        
        
    #读入数据,原始文件数据
    def loadData(self):
        file = self.parent.sysInfo.hotFile
        self.HotAnal.readAnalysis(file)
    
    #评分分析
    def score_anal(self):
        score_mean,score_var,hist = self.HotAnal.scoreAnalysis()
        self.var_avg.set(round(score_mean,2))
        self.var_var.set(round(score_var,2))
        self.var_type.set('Histogram（酒店评分区分分布）')
        
        #把绘制的图形显示到tkinter窗口上
        self.cv=FigureCanvasTkAgg(hist,self.frame_bottom)
        self.cv.draw()  
        self.cv.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                            fill=tkinter.BOTH,  # 填充方式
                            expand=tkinter.YES)
        return
    
    #房价分析
    def price_anal(self):
        avgPrice_mean, avgPrice_var,box = self.HotAnal.avgPriceAnalysis()
        self.var_avg.set(round(avgPrice_mean,2))
        self.var_var.set(round(avgPrice_var,2))
        self.var_type.set('Box（酒店房价数据分布）')
        
        #把绘制的图形显示到tkinter窗口上
        self.cv=FigureCanvasTkAgg(box,self.frame_bottom)
        self.cv.draw()  
        self.cv.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                            fill=tkinter.BOTH,  # 填充方式
                            expand=tkinter.YES)
        return
    
    # 窗体居中
    def center_window(self, width, height):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        # 宽高及宽高的初始点坐标
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(size)
        
        
#定义主程序
def main():
    MainWindow()
    
if __name__ == '__main__': main()
