import os
import shutil
import subprocess
import cv2

input_path = r"H:\Videos\New folder\frames"
output_path = r"H:\Videos\New folder\export"
input_folder = input_path

if os.path.exists(output_path):
    shutil.rmtree(output_path)
    os.makedirs(output_path)

def rename_replace(input_path, output_path, dataset_counter, frame_rate):
    filenames = os.listdir(input_path)
    sorted_filenames = sorted(filenames, key=lambda x: int(os.path.splitext(x)[0]))
    
    
    for filename in sorted_filenames:
        filepath = os.path.join(input_path, filename)
        basename = os.path.splitext(filename)[0]

        if os.path.isfile(filepath):
            if int(basename) % 150 == 0 and int(basename) > 500:
                dataset_counter += 1
                output_folder = os.path.join(output_path, f"dataset_{dataset_counter}")
                os.makedirs(output_folder, exist_ok=True)
                
                i = 0
                for i in range(3):
                    shutil.copy(os.path.join(input_path, str(int(basename) + i ) + ".jpg"), output_folder)
                    os.rename(os.path.join(output_folder, str(int(basename) + i ) + ".jpg"), os.path.join(output_folder, f"frame{i+1}.jpg"))
                    
                print("Copied file: ", int(basename))
    
    return(dataset_counter)
                
def export_frames_from_video(input_path, output_path):
    input_folder = r"H:\Videos\New folder"
    
    dataset_counter = 0
    video_files = [
        f for f in os.listdir(input_folder) if f.endswith(
            ('.mp4', '.avi', '.mkv', '.mov'))]
    
    video_files.sort()
    
    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)
        cap = cv2.VideoCapture(video_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        print ("Processing video", video_file)
        if not os.path.exists(input_path):
            os.makedirs(input_path)
        else:
            shutil.rmtree(input_path)
            os.makedirs(input_path)
        ffpmeg_command = f'ffmpeg -i {video_file} -vf "setpts=N/FR/TB,scale=-2:256:flags=lanczos,crop=ih*16/9:ih,mpdecimate" -q:v 0 -vsync 0 frames/%d.jpg -v quiet -stats'

        subprocess.call(ffpmeg_command)
        dataset_counter = rename_replace(input_path, output_path, dataset_counter, frame_rate)
        print("The Dataset counter ended at:", dataset_counter)
           
export_frames_from_video(input_path, output_path)
        
            
