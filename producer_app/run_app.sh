#!/bin/bash
if [ ! -p ${IPC_PATH} ]; then
    echo "creating fifo stream ${IPC_PATH}"
    mkfifo ${IPC_PATH}
fi
# run python with unbuffered stdout to stream it out
python -u producer.py > ${IPC_PATH}