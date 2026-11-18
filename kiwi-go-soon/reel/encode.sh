#!/bin/sh
# Blend 8 sub-frames per output frame (motion blur), mux audio, encode for Reels.
cd "$(dirname "$0")"
ffmpeg -hide_banner -loglevel error -y -framerate 240 -i sub/s_%05d.png -i audio.wav \
  -filter_complex "[0:v]tmix=frames=8,select='eq(mod(n\,8)\,7)',setpts=N/(30*TB),format=yuv420p[v]" \
  -map "[v]" -map 1:a -r 30 -c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 44100 -t 9.6 -movflags +faststart kiwi-go-reel.mp4
