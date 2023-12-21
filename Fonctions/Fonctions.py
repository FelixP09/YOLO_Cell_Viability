import os
import pandas as pd
import PIL
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import seaborn as sb
from ultralytics import YOLO

# Image normalization
def AutoNormalize(img, q = [0.0005,0.9995]) :
    quantile = np.quantile(img,q)
    matrix_scaled = (img - quantile[0]) /(quantile[1]-quantile[0])
    matrix_scaled[matrix_scaled <0] = 0
    matrix_scaled[matrix_scaled >1] = 1
    return matrix_scaled


# image loading + Autonormaliztion + convert gray to RGB (needed)
def Img_processing(path) :
    img = io.imread(path)
    img = AutoNormalize(img)
    img = (img*255).astype("uint8")
    img = np.stack([img,img,img], axis = 2)
    return img

class Custom_results :
    def __init__(self,obj, linewidth = 4, fontsize = 20, colors = [(8,76,153),(153,0,76)]) :
        self.obj = obj
        self.linewidth = linewidth
        self.fontsize = fontsize
        self.colors = colors
        self.Cell_Data = None
        self.Img_plot = None
        self.Viability_Data = None
        return self.Run()
        
    def Data_processing(self) :
        data = pd.DataFrame()
        data["Pred_class_ID"] = self.obj.boxes.cls.tolist()
        data["Pred_class"] = np.where(data.Pred_class_ID == 0, "Alive","Dead")
        data["x"] = self.obj.boxes.xywh[:,0].tolist()
        data["y"] = self.obj.boxes.xywh[:,1].tolist()
        data["w"] = self.obj.boxes.xywh[:,2].tolist()
        data["h"] = self.obj.boxes.xywh[:,3].tolist()
        data["x0"] = data.apply(lambda x : x.x - x.w//2, axis = 1)
        data["x1"] = data.apply(lambda x : x.x + x.w//2, axis = 1)
        data["y0"] = data.apply(lambda x : x.y - x.h//2, axis = 1)
        data["y1"] = data.apply(lambda x : x.y + x.h//2, axis = 1)
        self.Cell_Data = data
        
    def Img_Plot(self) :
        IMG = Image.fromarray(self.obj.orig_img)
        IMGD = ImageDraw.Draw(IMG)
        c = None
        fnt = ImageFont.truetype(r"/usr/share/fonts/truetype/fonts-deva-extra/chandas1-2.ttf",size = self.fontsize)


        for index, row in self.Cell_Data.iterrows() :
            if row.Pred_class_ID == 0 :
                c = self.colors[0]
            elif row.Pred_class_ID == 1 :
                c = self.colors[1]
            IMGD.rectangle((((row.x0,row.y0), (row.x1,row.y1))),outline = c, width = self.linewidth)
            bbox = IMGD.textbbox((row.x0,row.y0),row.Pred_class, font = fnt, anchor = "lb")
            IMGD.rectangle((((bbox[0],bbox[1]), (bbox[2],bbox[3]))),outline = c, width = self.linewidth, fill = c)
            IMGD.text((row.x0,row.y0),row.Pred_class, font = fnt, fill = "white", anchor = "lb")
            
        self.Img_plot = IMG
        
    def Viability_Count(self) :
        Total = len(self.Cell_Data)
        Dead = self.Cell_Data.Pred_class_ID.sum()
        Alive = Total - Dead
        self.Viability_Data = { "Total" : Total,
                                "Dead" : Dead,
                                "Alive" : Alive,
                                "Death_ratio" : Dead / Total,
                                "Alive_ratio" : Alive / Total}
        
    def Viability_plot(self) :
        colors = [np.array(i)/255 for i in [[127,127,127],self.colors[0],self.colors[1]]]
        plt.figure(figsize=(7,7))
        plt.bar(["Total","Alive","Dead"],[self.Viability_Data["Total"],self.Viability_Data["Alive"],self.Viability_Data["Dead"]],
               color = colors)
        plt.title("Pred classes distribution")
        plt.ylabel("Cell Count")
        plt.show()
        
    def Run(self) :
        self.Data_processing()
        self.Img_Plot()
        self.Viability_Count()
    
