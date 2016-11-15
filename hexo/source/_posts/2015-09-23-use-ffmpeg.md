---
title: ffmpeg 视频转码
layout: post
published: true
categories: 
tags: [tools, ffmpeg, video]
---

see https://www.virag.si/2012/01/web-video-encoding-tutorial-with-ffmpeg-0-9/
see https://www.virag.si/2012/01/webm-web-video-encoding-tutorial-with-ffmpeg-0-9/

## Mac OSX安装

`brew install ffmpeg --with-libvpx --with`

## 生成 mp4

### 参数说明

* -i [input file] | this specifies the name of input file
* -codec:v libx264 | tells FFmpeg to encode video to H.264 using libx264 library
* -profile:v high | sets H.264 profile to “High” as per Step 2. Other valid options are baseline, main
* -preset slow | sets encoding preset for x264 – slower presets give more quality at same bitrate, but need more time to encode. “slow” is a good balance between encoding time and quality. Other valid options are: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo (never use this one)
* -b:v | sets video bitrate in bits/s
* -maxrate and -bufsize | forces libx264 to build video in a way, that it could be streamed over 500kbit/s line considering device buffer of 1000kbits. Very useful for web - setting this to bitrate and 2x bitrate gives good results.
* -vf scale | applies “scale” filter, which resizes video to desired resolution. “720:480” would resize video to 720x480, “-1” means “resize so the aspect ratio is same.” Usually you set only height of the video, so for 380p you set “scale=-1:380”, for 720p “scale=-1:720” etc.
* -threads 0 | tells libx264 to choose optimal number of threads to encode, which will make sure all your processor cores in the computer are used
* -codec:a libfdk_aac | tells FFmpeg to encode audio to AAC using libfdk-aac library
* -b:a | sets audio bitrate in bits/s
* -pass [1 2] | tells FFmpeg to process video in multiple passes and sets the current pass
* -an | disables audio, audio processing has no effect on first pass so it’s best to disable it to not waste CPU

Standard web video (480p at 500kbit/s)
```
ffmpeg -i input_file.avi -codec:v libx264 -profile: high -preset slow -b:v 500k -maxrate 500k -bufsize 1000k -vf scale=-1:480 -threads 0 -codec:a libfdk_aac -b:a 128k output_file.mp4
```

360p video for older mobile phones (360p at 250kbit/s in baseline profile)
```
ffmpeg -i inputfile.avi -codec:v libx264 -profile:v baseline -preset slow -b:v 250k -maxrate 250k -bufsize 500k -vf scale=-1:360 -threads 0 -codec:a libfdk_aac -b:a 96k output.mp4
```
480p video for iPads and tablets (480p at 400kbit/s in main profile):
```
ffmpeg -i inputfile.avi -codec:v libx264 -profile:v main -preset slow -b:v 400k -maxrate 400k -bufsize 800k -vf scale=-1:480 -threads 0 -codec:a libfdk_aac -b:a 128k output.mp4
```
High-quality SD video for archive/storage (PAL at 1Mbit/s in high profile):
```
ffmpeg -i inputfile.avi -codec:v libx264 -profile:v high -preset slower -b:v 1000k -vf scale=-1:576 -threads 0 -codec:a libfdk_aac -b:a 196k output.mp4
```

## 生成 webm

###  参数说明:
* -codec:v    Specifies the video encoder to be used, in our case that is libvpx VP8 library
* -quality good   Sets encoding speed for the VP8 encoder. This works in concert with cpu-used parameter. Available values are best, good and realtime. The official libvpx documentation strongly advises against using best quality parameter, because good with cpu-used 0 offers almost identical quality for half the encoding time.
* -cpu-used [0-5] Sets “speed” of encoding “ lower value uses more CPU for processing and produces better quality. Larger values trade quality for faster encoding, with 4 and 5 enabling “rate distortion optimization”, which significantly speeds-up encoding with price of big quality hit.
* -b:v [bitrate]  Sets desired output video bitrate
* -maxrate/-bufsize   Set upper limits for stream bitrate, maxrate specifying maximum bitrate and bufsize specifying device buffer size. Buffer size tells the encoder how much it can overshoot the maximum bitrate when required. Good default is twice the maxrate for approx. 2sec of buffer.
* -qmin 10 -qmax 42   This sets minimum and maximum quantization values. Since as of 0.9, FFmpeg sets those values wrong by default, adding these is required for a a decent video quality. Omitting these will produce blocky broken video.
* -threads [num]  Sets number of encoding threads to use. Set to the number of your CPU cores available.
* -vf scale=[width:height]    Rescales video to a chosen resolution. Value of “-1″ means “size to keep aspect ratio”, e.g. setting this to “-1:720″ will produce a 720p output with same aspect ratio as input.
* -codec:a libvorbis  Sets output audio encoder to libvorbis to produce vorbis output. This is required for a valid WebM file.
* -b:a [bitrate]  Sets bitrate for encoded audio.
* -an disables audio, audio processing has no effect on first pass so itís best to disable it to not waste CPU.
* -f webm tells FFmpeg the output file format (required only if it cannot be inferred from output file extension).
* -pass [1 2] tells FFmpeg to process video in multiple passes and sets the current pass.

Standardî web video (480p at 600kbit/s)

```
ffmpeg -i input_file.avi -codec:v libvpx -quality good -cpu-used 0 -b:v 600k -maxrate 600k -bufsize 1200k -qmin 10 -qmax 42 -vf scale=-1:480 -threads 4 -codec:a vorbis -b:a 128k output_file.webm
```

High-quality SD video for archive/storage (PAL at 1.2Mbit/s):

```
ffmpeg -i input_file.avi -codec:v libvpx -quality good -cpu-used 0 -b:v 1200k -maxrate 1200k -bufsize 2400k -qmin 10 -qmax 42 -vf scale=-1:480 -threads 4 -codec:a vorbis -b:a 128k output_file.webm
```
