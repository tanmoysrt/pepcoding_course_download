#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Need to install ffmpeg CLi in system
# !pip install wget
# !pip install pandas
# !pip install ffmpeg-python


# In[20]:


import subprocess,os,wget,time,ffmpeg,re
import pandas as pd
from ffmpeg import Error as FFmpegError


# In[21]:


def mux_video_audio(videofile,audiofile, outputfile, base_dir=os.getcwd()):
    try:
        codec = "copy"
        process = subprocess.Popen(f"ffmpeg -i {base_dir}/{videofile} -i {base_dir}/{audiofile} -c {codec} {base_dir}/output/{outputfile}",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out, err = process.communicate()
        errcode = process.returncode
#         print(out)
#         print(err)
#         print(errcode)
        print("---- Successfully Muxed ----")
        
    except Exception as e:
        raise Exception(f"Error in muxing {e}")

def download_bar(current, total, width=80):
    print("Downloading: %d%% [%.2f / %.2f] MB" % (current / total * 100, current/1024/1024, total/1024/1024),end="\r")
    
def parse_data_from_link(data = None):
    if data.empty:
        print("No data given")
        return
    
    title = data.title
    url = data.url
    url_split = str(data.url).split("/")
    before_id = url_split[4]
    after_id = url_split[6]
    
    if title == "-1":
        title = f"Video {before_id}-{after_id}"
        
    return title,before_id,after_id

def delete_file_if_tmpfile_exsists():
    filename = ["tmp.mp4","tmp.m4a"]
    base_dir = os.getcwd()
    for i in filename:
        try:
            if os.path.exists(base_dir+"/"+i):
                os.remove(base_dir+"/"+i)
        except :
            raise Exception("Can't delete tmp files . May have permission issue")
            


# In[22]:


def downloader():
    df = pd.read_csv("data.csv")
    df.title = df.title.fillna("-1")
    starting_point = int(input("Enter the row number to start download from that position : "))
    ending_point =  int(input("Enter the row number where we need to finish : "))
    starting_point-=1
    for i in range(df.shape[0]):
        if i < starting_point :
            continue
        if i >= ending_point:
            print("Programme Halted")
            break
        while True:
            try:
                parsed_data = parse_data_from_link(df.iloc[i])
                video_link = f"https://pepvids.sgp1.cdn.digitaloceanspaces.com/batches/{parsed_data[1]}/video/{parsed_data[2]}/camcs.mp4"
                audio_link = f"https://pepvids.sgp1.cdn.digitaloceanspaces.com/batches/{parsed_data[1]}/video/{parsed_data[2]}/audio.m4a"
                print(video_link)
                output_filename = f"{parsed_data[0]}"
                output_filename = "Video "+str(i+1)+" "+output_filename
                output_filename = re.sub(r"[^a-zA-Z0-9]+", ' ', output_filename)
                output_filename += ".mp4"
                print(f"Downloading {output_filename}")
                wget.download(video_link,bar=download_bar,out="tmp.mp4")
                wget.download(audio_link,bar=download_bar,out="tmp.m4a")
                mux_video_audio("tmp.mp4","tmp.m4a",output_filename.replace(" ", "-"))
                time.sleep(5)
                delete_file_if_tmpfile_exsists()
                break
            except Exception as e:
                delete_file_if_tmpfile_exsists()
                print("Error")
                print(f"Details : {e}")
                user_input = input("Do you want to skip this download [y/n] : ")
                if user_input == "y" or user_input == "Y":
                    break
                else :
                    print("We are skipping this")


# In[23]:


downloader()


# In[63]:


if __name__ == "__main__":
    downloader()

