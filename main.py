
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import fitz
import re


summarization = pipeline("summarization",model="facebook/bart-large-cnn")

def checkmodel(model):
    if model=='bart':
        return "facebook/bart-large-cnn"
    elif model=='pegasus':
        return "google/pegasus-large"
    else:
        return "facebook/bart-large-cnn"

def generate_summary(source_type, Text,model):
    #summarization = pipeline("summarization",model=checkmodel(model))
    if source_type=='youtube':
        print("extracting youtube caption\n")
        youtubecaption(Text)
        with open('temp/subtitles.txt','r', encoding="utf-8") as f:
            Text = f.read()
        print("done")
    elif source_type=='pdf':
        with open('temp/pdftext.txt','r' , encoding="utf-8") as f:
            Text = f.read()
        print("done")
    print("Processing")
    summary = ""
    chunk = chunks(Text)
    print(chunk[1])
    for i in range (0,len(chunk[0])):
         #out = summarization(chunk[0][i], min_length = (chunk[1][i]//10), max_length=((chunk[1][i]*4)//10))[0]
         out = summarization(chunk[0][i] , min_length = (chunk[1][i]//15), truncation=True)[0]
         summary += out['summary_text']+"<br /><br />"
         print(out['summary_text'])
    return summary

def youtubecaption(url):
    # Extract video ID from various YouTube URL formats
    # Patterns: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID, etc.
    video_id = None
    
    # Pattern 1: watch?v=VIDEO_ID (standard and mobile)
    match = re.search(r'(?:youtube\.com\/watch\?v=|youtube\.com\/watch\?.*&v=)([^&\s]+)', url)
    if match:
        video_id = match.group(1)
    
    # Pattern 2: youtu.be/VIDEO_ID (shortened URLs)
    if not video_id:
        match = re.search(r'youtu\.be\/([^?\s]+)', url)
        if match:
            video_id = match.group(1)
    
    # Pattern 3: youtube.com/embed/VIDEO_ID
    if not video_id:
        match = re.search(r'youtube\.com\/embed\/([^?\s]+)', url)
        if match:
            video_id = match.group(1)
    
    # Pattern 4: youtube.com/v/VIDEO_ID
    if not video_id:
        match = re.search(r'youtube\.com\/v\/([^?\s]+)', url)
        if match:
            video_id = match.group(1)
    
    if not video_id:
        raise Exception(f"Could not extract video ID from URL: {url}")
    
    # Clean video ID (remove any trailing parameters)
    video_id = video_id.split('&')[0].split('?')[0]
    id = video_id

    #extracting and translating transcripts
    try:
        try:
            srt = YouTubeTranscriptApi.get_transcript(id,languages=['en','en-IN'])
        except:
            transcript_list = YouTubeTranscriptApi.list_transcripts(id)
            for transcript in transcript_list:
                if(transcript.is_translatable):
                    srt = (transcript.translate('en').fetch())
                    break
                else:
                    raise Exception("Sorry, Can Not Find a sutaible Transcript or Translation in English.")
    except Exception as e:
        raise Exception("Warning: Not Able to find any Transcript OR not able to translate it, Please only upload a video with transcript.")
    with open("temp/subtitles.txt", "w", encoding="utf-8") as f1:
            for i in srt:
                if(i['text']!="" and i['text']!="\n"):
                    f1.write("{} ".format(i['text']))
        

def chunks(s):
    lword = [[], []]
    l , u = 0 , 1
    while((len(s)-l)>20):
        word = 0
        while(word<1200 and u<len(s)):
            if(s[u]==' '):
                word+=1
            u+=1
        lword[0].append(s[l:u])
        lword[1].append(word)
        l = u
    return lword


def extractpdftext(file,ps,pe):
    whole_text = ""
    # with open('temp/pdftext.txt','w' , encoding="utf-8") as f:
    doc = fitz.open(file)
    if pe > doc.page_count:
        pe = doc.page_count
    for i in range(ps-1,pe):
        page = doc.load_page(i)
        data = page.get_text("text")
        whole_text += data + "\n"
        # f.write(data)
        # f.write('\n')
    print("done")
    return whole_text