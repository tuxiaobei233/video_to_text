# 导入所有必要的库
import cv2
import os

class V2frame:
    def work(self,V_paht,save_path):
        cam = cv2.VideoCapture(V_paht, cv2.CAP_FFMPEG)

        try :
      
        # 创建文件夹
            if not os.path.exists( save_path ):
                os.makedirs( save_path )
        except OSError:
            print ( 'Error: Creating directory of {save_path}' )

        currentframe = 0
  
        while ( True ):
            ret, frame = cam.read()
            if ret:
                name = save_path+'/'+ str(currentframe) + '.jpg'
                cv2.imwrite(name, frame)

                currentframe += 1
            else:
                break

        cam.release()

if __name__ == '__main__':
    a=V2frame()
    a.work('/home/tuxiaobei/video_to_text/videos/douyin_6559701594739313923.mp4','/home/tuxiaobei/video_to_text/frame')
