#!/bin/sh
set -eu

exe="/home/henrique/Redes/TP2_Redes/udprip/src/router.py"

# Start a new tmux session
tmux new-session -d -s mysession3

# Run the hub router in the first pane
tmux send-keys -t mysession3 "python3 $exe --addr 127.0.1.10 --startup-commands hub.txt" C-m

# Loop to create and run spoke routers
for i in $(seq 1 5); do
    tmux split-pane -v -t mysession3
    tmux send-keys -t mysession3 "python3 $exe --addr 127.0.1.$i --startup-commands spoke.txt" C-m
    tmux select-layout -t mysession3 even-vertical
done

# Attach to the tmux session
tmux attach -t mysession3
