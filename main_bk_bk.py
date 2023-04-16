'''


'''
from multiprocessing import Pool
import sys
from imageocr import imageocr
from Extract_audio import extract_audio
from Imghash import imghash
from Extract_frame import V2frame
from wav2text import wav2text
import os
import shutil
from Sentence_distance import sentence_distance
import time
import json
import cv2
audio_path = ''
frame_path = ''
datasave_path = './data'
video_path = './videos'
# 清空文件夹


def clear_dir(path):
    try:
        shutil.rmtree(path)
        os.mkdir(path)
    except Exception as e:
        print(e)

# 环境初始化


def enc_init():
    print('[enc_init] working')
    clear_dir(audio_path)
    clear_dir(frame_path)


def get_string_from_list(A):
    if type(A) == list:
        ret = ''
        for i in A:
            ret += get_string_from_list(i)
        return ret
    if type(A) == str:
        return A
    return ""


ocr_ret = []


def ocr_frame(frame):
    img_path = os.path.join(frame_path, str(frame)+'.jpg')
    now_ocr_result = imageocr.work(img_path)
    ocr_ret.append({'frame': frame, 'result': now_ocr_result})


def get_frame(x):
    return x['frame']


def OCR(path):
    imgH = imghash()

    # 返回结果
    ret = []

    # 当前帧
    now_frame = -15
    # 上一次执行ocr的帧
    last_frame = 0
    # 上一次的ocr结果拼接字符串
    last_ocr_result_string = "ocr at first"
    # 限
    k = 5
    # 历史最高k点
    kmax = 20
    # 匹配标识
    marchflag = False

    while True:
        now_frame += 15

        img_path = os.path.join(frame_path, str(now_frame)+'.jpg')

        if not os.path.exists(img_path):
            print('[OCR all] done', now_frame)
            break

        # 相似度高，无需ocr
        if not imgH.work(img_path, k):
            print("continue " + str(now_frame))
            continue

        print('[OCR working] ocr at frame', now_frame)

        # 进行ocr
        try:
            now_ocr_result = imageocr.work(img_path)
            now_ocr_result_string = get_string_from_list(now_ocr_result)
        except:
            now_ocr_result = None
            now_ocr_result_string = ''

        if now_ocr_result_string == '':
            now_ocr_result_string = 'there is no message'

        # 将识别结果添加
        ret.append({'frame': now_frame, 'result': now_ocr_result})

        print('[OCR done] ocr at frame', now_frame)

        print('[text similar start]')
        # 判断结果是否相同
        print(last_ocr_result_string)
        print(now_ocr_result_string)

        print('[text similar end]')

        # 当前版本第三方库含有bug
        # 已提交issue https://github.com/kiwirafe/xiangshi/issues/4
        dis = sentence_distance.work(
            last_ocr_result_string, now_ocr_result_string)
        sim = False
        print(dis)
        if dis < 3 or dis / max(len(last_ocr_result_string), len(now_ocr_result_string)) < 0.2:
            sim = True
        if sim > 0.4:

            marchflag = True
            # 按照规则修改k值
            if k < kmax:
                k = int(k * 1.5) + 1
            else:
                k += max(1, int(k*0.1))
            k = min(k, 20)
            last_frame = now_frame
            last_ocr_result_string = now_ocr_result_string
        else:
            if now_frame != 0:
                kmax = k
                k = max(int(k * 0.8), 4)
            # 是否进行回退操作
            if marchflag:
                now_frame = last_frame + 15
            else:
                last_frame = now_frame
                last_ocr_result_string = now_ocr_result_string
            marchflag = False
        print("end k:" + str(k) + '\n')
    ret.sort(key=get_frame)
    return ret


# 处理视频
def video_work(path, video_id):
    print('[video_work] working')
    enc_init()
    v2f = V2frame()
    w2t = wav2text()
    # 分离wav
    print('[extract audio]', path, audio_path)
    extract_audio(path, audio_path)
    # 分离帧
    print('[extract frame]', path, audio_path)
    v2f.work(path, frame_path)

    # 进行wav处理
    print('[wav2text] working')
    wav_result = w2t.work(audio_path+'/a.wav')
    print('[wav_result]', wav_result)

    # 进行ocr处理
    ocr_result = OCR(frame_path)
    print('ocr_result', ocr_result)

    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 保存结果
    return {"video_id": video_id, 'wav_result': wav_result, 'ocr_result': ocr_result, "fps": fps}


if __name__ == '__main__':
    name = sys.argv[1]
    if name == "":
        print("video name need")
        sys.exit(1)
    path = os.path.join(video_path, name)
    audio_path = './audio/' + name[:-4]
    try:
        os.mkdir(audio_path)
    except:
        pass
    frame_path = './frame/' + name[:-4]
    try:
        os.mkdir(frame_path)
    except:
        pass
    result = video_work(path, name[:-4])
    data_path = os.path.join(datasave_path, name[:-4]+'.json')
    with open(data_path, 'w') as f:
        f.write(json.dumps(result, ensure_ascii=False))
