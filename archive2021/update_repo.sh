# NOTE: this script will only work if ONLY new files are added; will break things if there are updates 
# to files that have been modified by a user.
# Put all local changes into temp store
git stash
# Get updates from repo
git fetch origin
# Pull and merge them into the current repo
git pull
# Put your changes back on top
git stash apply
