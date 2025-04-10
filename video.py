from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips, ColorClip
from moviepy.video.fx import fadein, fadeout
from PIL import Image, ImageOps
import io
import os
import numpy as np
import math
import shutil

video_name = './output_video.mp4'
supported_formats_images = [".jpeg", ".jpg", ".png", ".webp"]

def createVideo(imgFolderName, audioFolderName, userId, timePerImage = 3, resolution = "360p", quality = "low", tranistion = None):
    final_video_path = f'./static/output/user{userId}/'
    if not os.path.exists(final_video_path):
        os.makedirs(final_video_path)
    if not os.path.exists(imgFolderName):
        os.makedirs(imgFolderName)
    if not os.path.exists(audioFolderName):
        os.makedirs(audioFolderName)
    
    images = [img for img in os.listdir(imgFolderName) if any(img.endswith(format) for format in supported_formats_images)]
    images_with_times = [(img, os.path.getmtime(os.path.join(imgFolderName, img))) for img in images]
    sorted_images = sorted(images_with_times, key=lambda x: x[1])
    images = [filename for filename, _ in sorted_images]

    audios = [audio for audio in os.listdir(audioFolderName) if (audio.endswith(('.mp3', '.wav', '.aac', '.mpga')))]
    audios_with_times = [(audio, os.path.getmtime(os.path.join(audioFolderName, audio))) for audio in audios]
    sorted_audios = sorted(audios_with_times, key=lambda x: x[1])
    audios = [filename for filename, _ in sorted_audios]
    clips = []
    
    if resolution == "360p":
        width, height = 640, 360
    elif resolution == "720p":
        width, height = 1280, 720
    elif resolution == "1080p":
        width, height = 1920, 1080
    elif resolution == "4k":
        width, height = 3840, 2160
    else:
        width, height = 640, 360   
        
    if quality == 'low':
        setQuality = 33
    elif quality == 'medium':
        setQuality = 67
    elif quality == 'high':
        setQuality = 100
    else:
        setQuality = 33
    
    black_screen = ColorClip(size=(width, height), color=(0, 0, 0), duration=0.5)
    
    for image in images:
        img_path = os.path.join(imgFolderName, image)

        img = Image.open(img_path)
        img = img.convert('RGB')
        img = ImageOps.pad(img, (width, height), color="black")
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG', quality = setQuality)
        img = Image.open(img_io)
        img_array = np.array(img)
        clip = ImageSequenceClip([img_array], fps=1)
        clip = clip.set_duration(timePerImage)
        if(tranistion == "fadeIn"):
            clips.append(black_screen)
            clip = clip.fadein(1).fadeout(0)
            clips.append(clip)
        elif(tranistion == "crossFadeIn"): 
            clips.append(black_screen)  
            clip = clip.crossfadein(1).crossfadeout(0)
            clips.append(clip)
        elif(tranistion == "fadeOut"):
            clip = clip.fadein(0).fadeout(1)
            clips.append(clip)
            clips.append(black_screen)
        elif(tranistion == "crossFadeOut"):
            clip = clip.crossfadein(0).crossfadeout(1)
            clips.append(clip)
            clips.append(black_screen)
        elif(tranistion == "fadeInOut"):
            clips.append(black_screen)
            clip = clip.fadein(1).fadeout(1)
            clips.append(clip)
            clips.append(black_screen)
        elif(tranistion == "crossFadeInOut"):  
            clips.append(black_screen)  
            clip = clip.crossfadein(1).crossfadeout(1)
            clips.append(clip)
            clips.append(black_screen)
        else:
            clips.append(clip)
        
    final_clip = black_screen
        
    for clip in clips:
        final_clip = concatenate_videoclips([final_clip, clip])

    audio_clips = []
    mainAudio = ''
    for audio in audios:
        audioReq = os.path.join(audioFolderName, os.path.splitext(audio)[0] + os.path.splitext(audio)[1]) 
        audio_clip = AudioFileClip(audioReq)
        audio_clips.append(audio_clip)
        if mainAudio == '':
            mainAudio = audio_clip
        else:
            mainAudioList = [mainAudio] + [audio_clip]
            mainAudio = concatenate_audioclips(mainAudioList)
        
    if mainAudio != '':
        audio_clip = mainAudio
        audio_duration = audio_clip.duration
        video_duration = final_clip.duration
        repetitions = max(math.ceil(float(video_duration) / float(audio_duration)) + 1, 1)
        audio_clips = [audio_clip] * repetitions
        concatenated_audio_clip = concatenate_audioclips(audio_clips)
        concatenated_audio_clip = concatenated_audio_clip.set_duration(video_duration)
        final_clip = final_clip.set_audio(concatenated_audio_clip)

    final_clip.write_videofile(video_name, fps = 1)
    shutil.move(video_name, final_video_path + 'output_video.mp4')

    for audio in audio_clips:
        audio.close()
    return

if __name__ == "__main__":
    createVideo("./static/Images", "./SelectedAudio", 1, timePerImage= 3, tranistion = "fadeIn")
