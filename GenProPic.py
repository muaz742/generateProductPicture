import os
import cv2
from PIL import Image
import numpy as np

class GenProPic:
    def __init__(self):
        self.plots = []
        self.plansPerspective = []
    def addBgPic(self,backgruondPicturePath):
        self.pathBg = os.path.join(backgruondPicturePath)
        self.imgBg = Image.open(self.pathBg)
    def addPlot(self,plotInBackgroundPicture):
        points = plotInBackgroundPicture['points']
        topLeft = points['topLeft']
        topRight = points['topRight']
        bottomLeft = points['bottomLeft']
        bottomRight = points['bottomRight']
        points = [topLeft,topRight,bottomLeft,bottomRight]
        plot = np.float32(points)
        self.plots.append({
            'plot':plot,
            'size':plotInBackgroundPicture['realSize']
            })
        print('Added plot')
    def addPic(self,mockupPicturePath):
        self.pathPic = os.path.join(mockupPicturePath)
        self.imgPic = cv2.imread(self.pathPic, cv2.IMREAD_UNCHANGED)
    def setOutDir(self, outputDirectoryPath=None):
        if outputDirectoryPath is None:
            self.pathOutDir = os.path.dirname(self.pathBg)
            return
        self.pathOutDir = os.path.join(outputDirectoryPath)
    def generate(self):
        for plot in self.plots:
            if plot['size'][0] < plot['size'][1]:
                size = plot['size'][0]
            else:
                size = plot['size'][1]
            resizeImage = self._resizeImg(
                self.imgPic, 
                size
                )
            resizeImage = self._toImgPIL(resizeImage)
            generatedPlan = self._generate_plan(resizeImage,plot['size'])
            generatedPlan = self._toImgCv2(generatedPlan)
            h, w, c = generatedPlan.shape
            pltPlan = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
            pltPlot = plot['plot']
            plotConnect = cv2.getPerspectiveTransform(pltPlan, pltPlot)
            imgPerspective = cv2.warpPerspective(
                generatedPlan, 
                plotConnect,
                self.imgBg.size,
                borderMode=cv2.BORDER_CONSTANT, 
                borderValue=(255, 255, 255)
                )
            self.plansPerspective.append(imgPerspective)
        bg = self.imgBg
        for plan in self.plansPerspective:
            fore = self._toImgPIL(plan)
            bg.paste(fore, (0, 0), fore)
        return bg
    def save(self, outputFileName=None,outputDirectoryPath=None):
        if outputDirectoryPath is None:
            try:
                self.pathOutDir
            except:
                self.setOutDir()
        else:
            self.setOutDir(outputDirectoryPath)
        if outputFileName is None:
            outputFileName = 'bindedPicture'
        pathOutput = os.path.join(self.pathOutDir, outputFileName+'.png')
        picBinded = self.generate()
        print("Generated '{}.png'".format(outputFileName))
        picBinded = self._toImgCv2(picBinded)
        cv2.imwrite(pathOutput,picBinded)
        print("Saved '{}.png'".format(outputFileName))
    def _toImgCv2(self,pillowImage):
        img = np.array(pillowImage)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
        return img
    def _toImgPIL(self,openCvImage):
        img = cv2.cvtColor(openCvImage, cv2.COLOR_BGRA2RGBA)
        pillowImage = Image.fromarray(img)
        return pillowImage
    def _resizeImg(self,img, width = None, height = None, inter = cv2.INTER_AREA):
        dim = None
        (h, w) = img.shape[:2]
        if width is None and height is None:
            return img
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        resized = cv2.resize(img, dim, interpolation = inter)
        return resized
    def _generate_plan(self,img, size):
        img_w, img_h = img.size
        background = Image.new('RGBA', size, (0, 0, 0, 255))
        bg_w, bg_h = background.size
        offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
        background.paste(img, offset)
        return background