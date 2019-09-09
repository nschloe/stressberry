#!/bin/bash

# Config
PLOT=/home/pi/.local/bin/stressberry-plot
TEMP_MIN=30
TEMP_MAX=90
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
    MPLBACKEND=Agg $PLOT $FILELIST -d $DPI -t $TEMP_MIN $TEMP_MAX -o "${f%.out}$FILE_FORMAT" --not-transparent --line-width 0.2
done
