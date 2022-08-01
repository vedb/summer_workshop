# Bash commands
This page contains a bunch of bash commands that we will use during our introduction to the command line. We will tell you what to type during the lectures, but we have found that it's very nice to have a copy-able version of the commands ready at hand. 

# `ping` command
* Ping google (This is a simple test to determine whether the computer you're on can "see" the interent at all - google is very rarely down): 

`ping www.google.com`

* Check whether you can see a computer on this network
`ping bdss_node_party.acs.unr.edu`

* Check whether you can see a different computer
`ping bdss_node_00.acs.unr.edu`

* Check whether you can see the high-performance computing login node
`ping pronghorn.rc.unr.edu`

# `ssh` command

* connect to "party" node: 
`ssh bdss_student@bdss_node_party.acs.unr.edu`

* connect to your individual node:
`ssh bdss_student@bdss_node_<number>.acs.unr.edu`

* Note that `<number>` should be replaced with the number you for the node that you are assigned, e.g. `ssh bdss_student@bdss_node_25.acs.unr.edu` 

* disconnect from any node with <ctrl>-d (hold "control" button and press "d")



# `man` page / `less` command quick reference:

* `/` is find (type after the slash and press enter to search for an exact word or phrase)

* `n` is next instance (after searching for something)

* `<shift>-n` is previous instance (after searching for something)

* `q` is quit man 

