#!/bin/bash
# GitHub SSH setup for OpenClaw sessions

# Start ssh-agent hvis den ikke kjører
if [ -z "$SSH_AGENT_PID" ] || ! kill -0 "$SSH_AGENT_PID" 2>/dev/null; then
    eval "$(ssh-agent -s)" > /dev/null
fi

# Legg til GitHub-nøkkelen hvis den ikke allerede er lagt til
if ! ssh-add -l | grep -q "github_arvi"; then
    ssh-add ~/.ssh/github_arvi 2>/dev/null
fi
