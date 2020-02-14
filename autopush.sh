#!/bin/bash -e
# Doesn't necessarily add or rm everything it's supposed to. Use with care.
exe() { echo "\$ $@" ; "$@" ; } # prints the command being  run

if [ $# -eq 0 ]; then
    comment="autopush"
  else
    comment="$1"
fi

echo Autopushing all with comment "$comment"
exe git add -A
exe git commit -m "$comment"

while true
do
  # prompt user and get input
  read -p "Continue to Push?[Y/n]" answer

  # handle input 
  case $answer in
   [yY]* ) exe git push 
           break;;

   [nN]* ) exit;;

   * ) exe git push 
       break;;

  esac
done

echo Completed.
exit
