'''


'''
from imageocr import imageocr
from Extract_audio import extract_audio
from Imghash import imghash
from Extract_frame import V2frame
from wav2text import wav2text
import os
import shutil
import xiangshi as xs
import time
import json

audio_path='./audio'
frame_path='./frame'

#清空文件夹
def clear_dir(path):
    try:
        shutil.rmtree(path)  
        os.mkdir(path)
    except Exception as e:
        print(e)  

#环境初始化
def enc_init():
    print('[enc_init] working')
    clear_dir(audio_path)
    clear_dir(frame_path)

def get_string_from_list(A):
    if type(A) == list:
        ret=''
        for i in A:
            ret+=get_string_from_list(i)
        return ret
    if type(A) == str:
        return A
    return ""

def OCR(path):
    imgH=imghash()

    #返回结果
    ret=[]

    #当前帧
    now_frame=-1
    #上一次执行ocr的帧
    last_frame=-1
    #上一次执行ocr的帧的hash
    last_hash=None
    #上一次的ocr结果拼接字符串
    last_ocr_result_string="ocr at first"
    #限
    k=4
    #历史最高k点
    kmax=0xffffffff
    #匹配标识
    marchflag=False
    
    while True:
        now_frame+=1

        img_path=os.path.join(frame_path,str(now_frame)+'.jpg')

        if not os.path.exists(img_path):
            print('[OCR all] done',now_frame)
            break

        now_hash = imgH.work(img_path)

        #相似度高，无需ocr
        if now_frame!=0:
            print('[hash k]',now_hash-last_hash,k)
            if abs(now_hash-last_hash) < k:
                continue
            
        print('[OCR working] ocr at frame',now_frame)
        
        #进行ocr
        try:
            now_ocr_result=imageocr.work(img_path)
            now_ocr_result_string=get_string_from_list(now_ocr_result)
        except:
            now_ocr_result=None
            now_ocr_result_string=''

        if now_ocr_result_string=='':
            now_ocr_result_string='there is no message'

        #将识别结果添加
        ret.append( {'frame':now_frame ,'result':now_ocr_result} )

        print('[OCR done] ocr at frame',now_frame)

        print('[text similar start]')
        #判断结果是否相同
        print(last_ocr_result_string)
        print(now_ocr_result_string)
        print(xs.minhash([last_ocr_result_string, now_ocr_result_string]))
        print('[text similar end]')

        similaty=0
        #当前版本第三方库含有bug 
        #已提交issue https://github.com/kiwirafe/xiangshi/issues/4
        try:
            similaty=xs.minhash([last_ocr_result_string, now_ocr_result_string])
        except:
            similaty=1

        if similaty >0.4:
            marchflag=True
            #按照规则修改k值
            if k < kmax:
                k*=2
            else:
                k+=max(1,int(k*0.1))
            last_hash=now_hash
            last_frame=now_frame
            last_ocr_result_string=now_ocr_result_string
        else:
            if now_frame!=0:
                kmax=max(int(k/2),1)
                k=kmax
            #是否进行回退操作
            if marchflag:
                now_frame=int((now_frame+last_frame+1)/2)
            else:
                last_hash=now_hash
                last_frame=now_frame
                last_ocr_result_string=now_ocr_result_string
            marchflag=False


    return ret


#处理视频
def video_work(path):
    print('[video_work] working')
    v2f=V2frame()
    w2t=wav2text()
    #环境重置
    enc_init()
    #分离wav
    print('[extract audio]',path,audio_path)
    extract_audio(path,audio_path)
    #分离帧
    print('[extract frame]',path,audio_path)
    v2f.work(path,frame_path)

    #进行wav处理
    print('[wav2text] working')
    wav_result=w2t.work(audio_path+'/a.wav')
    print('[wav_result]',wav_result)

    #进行ocr处理
    ocr_result=OCR(frame_path)
    print('ocr_result',ocr_result)

    #保存结果
    return {'wav_result':wav_result,'ocr_result':ocr_result}


    

#保存
def work(video_path,save_path):
    print('video path:',video_path)
    files = os.listdir(video_path)
    for file in files:
        if file.endswith('.mp4'):
            path=os.path.join(video_path,file)
            result=video_work(path)
            print('[work done]',result)
            data_path=os.path.join(save_path,file+'.json')
            with open(data_path,'w') as f:
                f.write(json.dumps(result, ensure_ascii=False))
        else:
            print(file,'is not MP4')


if __name__ == '__main__':
    video_path='./videos'
    datasave_path='./data'
    work(video_path,datasave_path)
