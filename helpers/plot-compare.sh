#!/bin/bash

# Config
PLOT=/home/pi/.local/bin/stressberry-plot
TEMP_MIN=30
TEMP_MAX=90
D_TEMP_MIN=0
D_TEMP_MAX=70
DPI=300
LINE_WIDTH=0.2
FILE_FORMAT=.png


for f in *.files # contains list of files
  do
     echo "**Processing: $f"
     FILELIST=""
     while IFS= read line || [[ -n "$line" ]];
     do
        FILELIST="$FILELIST $line"
    done < "$f"
    MPLBACKEND=Agg $PLOT $FILELIST -d $DPI -t $D_TEMP_MIN $D_TEMP_MAX -o "${f%.files}-delta$FILE_FORMAT" --not-transparent --line-width $LINE_WIDTH --delta-t
    MPLBACKEND=Agg $PLOT $FILELIST -d $DPI -t $TEMP_MIN $TEMP_MAX -o "${f%.files}$FILE_FORMAT" --not-transparent --line-width $LINE_WIDTH
done

