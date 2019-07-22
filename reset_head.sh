#!/bin/bash
echo Setting repo to latest master
git fetch origin
git pull
git reset --hard HEAD
echo Completed
