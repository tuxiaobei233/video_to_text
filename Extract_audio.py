import moviepy.editor as mp


def extract_audio(videos_file_path, save_path):
    print(videos_file_path)
    my_clip = mp.VideoFileClip(videos_file_path)
    print(f'{save_path}/a.wav')
    my_clip.audio.write_audiofile(f'{save_path}/a.wav')


if __name__ == '__main__':
    extract_audio('douyin_6571001202379590925.mp4',
                  './audio/douyin_6571001202379590925')
