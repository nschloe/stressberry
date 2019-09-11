#!/bin/bash

#Test name from CMD line args
NAME=$1

# Stress Test Config
STRESSBERRY=/home/pi/.local/bin/stressberry-run
OUTDIR=/share/

IDLE=300 # 5mins
DURATION=3600 # 1hour
WAIT=900 # 15mins
# Ambient Temperature Sensor
SENSOR=2302
SENSOR_PIN=16

# Convert to mins for file naming
let DURATION_MINS=$DURATION/60
let IDLE_MINS=$IDLE/60
let WAIT_MINS=$WAIT/60
# Replace spaces with underscore for file naming
FNAME=${NAME// /_}

# Loop the stress test to cover all scenarios
for cores in {1..4}
  do
    OUTFILE=$FNAME"-s"$DURATION_MINS"-i"$IDLE_MINS"-c"$cores".out"
    NOW=$(date +"%x %r")
    echo "$NOW : Name: \"$NAME\" : Idle: $IDLE Duration: $DURATION Cores: $cores Outfile: $OUTFILE"
    $STRESSBERRY -n "$NAME" -a $SENSOR $SENSOR_PIN -d $DURATION -i $IDLE -c $cores $OUTDIR$OUTFILE
    echo "Waiting betweeen tests for: $WAIT_MINS minutes..."
    sleep $WAIT
done
echo "Test Complete: "$(date +"%x %r")
