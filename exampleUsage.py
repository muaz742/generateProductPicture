from GenProPic import GenProPic

photoPc = GenProPic()
photoPc.addBgPic("imgComposition.png") # Add background picture path.
photoPc.addPlot({ 
    'realSize': (2178, 3630),       # Size of transparent area in the picture. (for real ratio)
    'points':{
        'topLeft': [1770, 898],     # Top left point.
        'topRight': [3450,400],     # Top right point.
        'bottomLeft': [2725, 3959], # Bottom left point.
        'bottomRight': [4500,3360]  # Bottom right point.
    }
})
#photoPc.setOutDir("")              # Set output directory. (if you want)
photoPc.addPic("imgMozilla_LFW-1.png") # Add picture path.
photoPc.save("imgBindedPictureName")   # Save picture.