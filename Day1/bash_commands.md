# Bash commands
This page contains a bunch of bash commands that we will use during our introduction to the command line. We will tell you what to type during the lectures, but we have found that it's very nice to have a copy-able version of the commands ready at hand. 

# Morning
## `ping` command
* Ping google (This is a simple test to determine whether the computer you're on can "see" the interent at all - google is very rarely down): 
`ping www.google.com`

* Check whether you can see a computer on this network:
`ping bdss_node_party.acs.unr.edu`

* Check whether you can see a different computer:
`ping bdss_node_00.acs.unr.edu`

* Check whether you can see the high-performance computing login node:
`ping pronghorn.rc.unr.edu`

## `ssh` command

* connect to "party" node: 
`ssh bdss_student@bdss_node_party.acs.unr.edu`

* connect to your individual node:
`ssh bdss_student@bdss_node_<number>.acs.unr.edu`
    * Note that `<number>` should be replaced with the number you for the node that you are assigned, e.g. `ssh bdss_student@bdss_node_25.acs.unr.edu` 

* disconnect from any node with <ctrl>-d (hold "control" button and press "d")

# Afternoon
## File manipulation : viewing files (`cat`, `head`, `tail`, `less`, `man`)
(Done from your personal VM or laptop; you should have the example shell data in the home directory)
* Show the full contents of a file: 
`cat ~/shell-lesson-data/exercise-data/animal-counts/animals.csv`

* Show the first (n) lines of a file:
`head ~/shell-lesson-data/exercise-data/creatures/basilisk.dat`

* Show the last (n) lines of a file: 
`tail ~/shell-lesson-data/exercise-data/creatures/basilisk.dat`

* Show a scrollable version of a (long) text file:
`less ~/shell-lesson-data/exercise-data/writing/LittleWomen.txt` (see below for help with `less` command!)

## File maniupation: creating, copying, moving, deleting files and directories (`touch`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`)
(Done from your personal VM or laptop; you should have the example shell data in the home directory. Start in the home directory: `cd ~/`)

* Create a new empty file: 
`touch hello.txt` then `ls` to see new file, then `cat hello.txt` to see that it is empty (nothing is displayed with this call to `cat`)

* copy that file to a new name: 
`cp hello.txt backatyou.txt` then `ls` to see that it exists

* remove the newly copied file: 
`rm backatyou.txt` then `ls` to see that it is gone

* make a directory to put the empty file, called "empty_files":
`mkdir empty_files` then `ls` to see that it is there

* move the empty file into the directory:
`mv hello.txt empty_files/`

* remove the directory, since it is useless after all:
`rm empty_files/`
    * this will fail! You need to find an option in rm that will remove not only a directory but also (recursively) the files and folders inside it. 


## More copying on the same computer
* Copy a file from the example data to your home directory: `cp ~/shell-lesson-data/exercise-data/animal-counts/animals.csv ~/`

* Copy a file from the example data to your home directory and rename it as you copy it: `cp ~/shell-lesson-data/exercise-data/animal-counts/animals.csv ~/love_these_animals.csv`

* Copy a whole directory of files (this won't work without a bit of modification!)
`cp ~/shell-lesson-data/ ~/shell-lesson-data-bkup/`

## `scp` and `rsync` commands - copying files between computers
* Copy a file from your computer to the ~/uploads/ directory on bdss_node_party (communal) VM: 
`scp <file> bdss_student@bdss_node_party.acs.unr.edu:~/uploads/`

* Copy a file from the bdss_node_party VM to your personal machine: 
`scp bdss_student@bdss_node_party.acs.unr.edu:~/uploads/<jpeg image file> my_new_file.jpg`

* Copy a file from the bdss_node_party VM to your personal VM:
    * first, log in to your VM: `ssh bdss_student@bdss_node_<XX>.acs.unr.edu`
    * second, call: `rsync bdss_student@bdss_node_party.acs.unr.edu:~/uploads/<jpeg image file> ./my_new_file.jpg`
    * This copies the image file to whatever directory you are in. 

## Program installation with `sudo apt-get install`
(All done from your personal VM, e.g. bdss_node_25)
* Install the program "rename": 
`sudo apt-get install rename`

* Install the program "cowsay": 
`sudo apt-get install cowsay`

## Renaming files walk-through
These commands are meant to be called in sequence:

* Make a new directory called "data_copy" and cd into it: 
`mkdir ~/data_copy/`  then  `cd ~/data_copy/`

* copy many files at once from one of the example directories into that directory: 
`cp ~/shell-lesson-data/north-pacific-gyre/*txt ~/data_copy/`

* check on what input rename wants: 
`man rename`

* rename all files with "A.txt" at the end to have "_first.txt"
`rename s/A.txt/_first.txt/ *A.txt`

* try to rename the files ending in `B.txt` to replace `B` with `_second`!
# `man` page / `less` command quick reference:

* `/` is find (type after the slash and press enter to search for an exact word or phrase)

* `n` is next instance (after searching for something)

* `<shift>-n` is previous instance (after searching for something)

* `q` is quit man 

# Special characters & operators
* `~` refers to the home directory in *nix systems

* `..` or `../` refers to the directory above the current directory

* `.` or `./` refers to the current directory

* `*` wild card operator for ls, cp, mv, rm, and many more: fits *anything* matching the rest of the pattern, e.g. `ls *.txt` lists all files in a directory that end in ".txt". 

* `>>` send output to a file, e.g. `echo Hello world >> hello.txt` or `ls *txt >> text_files_in_dir.txt`
