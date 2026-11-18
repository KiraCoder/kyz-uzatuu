#!/bin/sh
# Blend 2 sub-frames per output frame (light motion blur), mux audio, encode for Reels.
cd "$(dirname "$0")"
ffmpeg -hide_banner -loglevel error -y -framerate 60 -i frames/s_%05d.png -i audio.wav \
  -filter_complex "[0:v]tmix=frames=2,select='eq(mod(n\,2)\,1)',setpts=N/(30*TB),format=yuv420p[v]" \
  -map "[v]" -map 1:a -r 30 -c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 44100 -ac 2 -t 10.0 -movflags +faststart kiwi-go-reel-03-tolko-dostavka.mp4
