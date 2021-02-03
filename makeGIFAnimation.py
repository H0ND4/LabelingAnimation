from PIL import Image
import glob

# フォルダ
files = sorted(glob.glob('./anim/*.png'))  

images = list(map(lambda file : Image.open(file) , files))
images[0].save('image.gif' , save_all = True , append_images = images[1:] , duration = 30 , loop = 0)