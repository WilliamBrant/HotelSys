# -*- coding: utf-8 -*-
"""
Created on Wed April 13 10:57:59 2022

@author: wwq
"""

import pandas as pd
#from fuzzywuzzy import fuzz
#from fuzzywuzzy import process
#数据类，系统配置信息
class SysConfiguration:
    def __init__(self):
        self.infoCol = ("name", "Time","RoomNum","AvgPrice","score")
        self.colname = ["酒店名","装修时间","房间数","平均房价","评分"]
        self.hotFile = "HotelInfo.csv"
        
        
#数据类，酒店信息
class Hotel:
    def __init__(self, name):
        self.name = name
        self.Info = [] 
        
    def get_name(self):
        return self.name
    
    def get_Info(self):
        return self.Info
    
#业务逻辑类，维护酒店信息，增、删、改、查 
class ManaHotelInfo:
    def __init__(self):
        self.info = []
      
    #从文件中读取酒店历史信息
    def loadFile(self, txtName): 
        self.info = []
        
        try:
            infile = pd.read_csv(txtName,sep=',',header='infer') #读取文件
        except Exception as e:
            return e
        
        for name in infile.iloc[:,0]:
            if self.queryID( name ) == -1 :   #查询酒店是否已存在
                hot = Hotel(name)
                Info = infile[infile.iloc[:,0]==name].iloc[:,1:].values.tolist()[0] 
                Info[0],Info[1] = int(Info[0]),int(Info[1])
                hot.Info = Info
                self.info.append( hot )
            else:
                print("相同酒店{}记录，删除！",name)
          
        print("Load file successfully!\n")     
        return 1

    #将酒店信息写入文件
    def saveFile( self, txtName):        
        frame2 = pd.DataFrame(columns=['酒店名','装修时间','房间数','平均房价','评分'])
        for item in self.info:
            new = pd.DataFrame([[item.name,item.Info[0],item.Info[1],item.Info[2],item.Info[3]]],
                               columns=['酒店名','装修时间','房间数','平均房价','评分'])
            frame2=frame2.append(new)
        frame2.to_csv(txtName,index=False,encoding="utf_8_sig")
        print("Save file successfully!\n")
        return 1


    #查询酒店是否已存在
    def queryID(self, name):
        names = []
        for item in self.info:
            names.append(item.name)
    
        if name in names:
            return names.index(name)
        else:
            return -1


    #查询酒店并返回信息
    def queryHot(self, name):
    
        if self.info == []:
            print("酒店信息不存在，请读取/录入酒店信息！\n")
            return -1
        
        idx = self.queryID(name)
        if idx != -1:
            return self.info[idx]
        else:
            print("酒店{}不存在！".format(name) )
            return -1

    #添加酒店信息
    def addHotInfo(self, hotInfo):
        idx = self.queryID(hotInfo.name)
        if idx != -1:  
            print("酒店{}已存在，不能添加！", hotInfo.name)
            return -1
        else:       #酒店不存在，可添加
            self.info.append( hotInfo )
            return 0       
    
    #修改酒店信息
    def updateHotInfo(self, hotInfo):
        idx = self.queryID(hotInfo.name)
        if idx != -1:   #酒店存在，记录可修改
            self.info[idx] = hotInfo
            return 0
        else:
            print("酒店{}不存在，不能修改！", hotInfo.name)
            return -1
     
    #删除酒店信息
    def delHotInfo(self, name):
        idx = self.queryID(name)
        if idx != -1: #酒店存在，可删除
            del self.info[idx]
            return 0
        else :
            print("酒店{}不存在，不能删除！",name)
            
            
#####定义主程序界面用户交互窗口类#########

class MainWindow:
    def __init__(self):
        self.manaHot = ManaHotelInfo()

    #菜单选择
    def selectCommand(self):
        print("******************************************")
        print("  1. 从文件中读取酒店历史信息")
        print("  2. 查询酒店信息")
        print("  3. 录入酒店信息")
        print("  4. 打印所有酒店信息")
        print("  5. 保存所有酒店信息至文件")
        print("  6. 退出")
        print("******************************************")
        return input("请输入选择的功能编号：\n")
    
    #添加新酒店/或修改酒店记录            
    def addHotInfo(self):
                
        addName = input("请输入添加酒店名：\n")
        if addName == "" :
            print("输入酒店名为空！")
            return -1
        
        mana = self.manaHot  #获得酒店信息对象

        #录入酒店信息
        str = input("请依次输入酒店的装修时间,房间数,平均房价,评分: \n") 
        while str != "" :            
            strs = str.split(",")
            nums = [ eval(x) for x in strs ]
            time, score = nums[0],nums[-1]          
            if(time>=2001 and time<=2022 and score>=1 and score<=5 ) :
                nums[-1] = round(nums[-1],1) #保留1位小数
                hot = Hotel(addName)
                hot.Info=nums
                str = ""
            else:
                print("输入数据不合法，请重新输入!")
                str = input("请依次输入酒店的装修时间,房间数,平均房价,评分: ")
        
        #添加/修改 酒店信息到数据记录中
        if ( mana.addHotInfo(hot) == -1 ): #酒店已存在，则选择是否修改           
            ch = input("该酒店已存在，是否修改: Y or N?）")
            if ch == 'Y':
                mana.updateHotInfo(hot)
    
    
    #显示某酒店信息
    def showHotInfo(self,HotInfo):
        
        print("-----------------------")
        print("酒店：{}".format(HotInfo.name) )
        cur = HotInfo.Info
        print('装修时间:{}年,房间数:{},平均房价:{},评分:{}'.format(cur[0],cur[1],cur[2],cur[3]))
        print("-----------------------")
              
    #显示所有酒店信息
    def  showAllInfo(self):       
        info = self.manaHot.info
        if info == []:
            print("酒店信息不存在，请读取/录入酒店信息！\n")
            return -1
        
        print("酒店信息：")
        for item in info:
            self.showHotInfo(item)
     
    def loadData(self, txtName):
        res = self.manaHot.loadFile(txtName)
        if( res != 1 ):
            print( res )
               
    def saveData(self, txtName):
        res = self.manaHot.saveFile(txtName)
        if( res != 1 ):
            print( res )
    
    def queryHot(self):
        qname = input("请输入查询酒店名称：\n")
        mana = self.manaHot
        HotInfo = mana.queryHot(qname)
        if( HotInfo !=-1) :
            self.showHotInfo(HotInfo)
       
#主程序
def main():
    
    #初始化
    mWin = MainWindow()

    #显示菜单，按照选择执行操作
    while True:
        ch = mWin.selectCommand()
        if ch == '1': #从文件读出已有酒店信息
            mWin.loadData("HotelInfo.csv")
            mWin.showAllInfo()

        elif ch == '2': #查询已有酒店信息
            mWin.queryHot()      

        elif ch == '3': #添加酒店
            mWin.addHotInfo()

        elif ch == '4': #显示所有酒店信息
            mWin.showAllInfo()

        elif ch == '5': #保存酒店信息到文件
            mWin.saveData("HotelInfo.csv")
            
        else:
            break

if __name__ == '__main__': main()