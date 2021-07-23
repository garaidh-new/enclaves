# Readme for the files in here #

## Switch.sh ##
Run this with 'enclave' or 'noenclave' to get it to build you a deployment in the enclave, or not. 

### Load balancer options ###
The script Switch.sh currently has a line that applies the file loadbalancer.yaml. Change that for Nodeport.yaml to expose the pods on the same port on each Node, instead of via an external load balancer. Then run 

    kubectl get svc -n foo

to get the port the node has exposed it on.
Actually that command will tell you wehere the pods are exposed, regardless of how they are exposed.

## Putting the enclave into ECR - push.sh ##

This automates the commands for putting an enclave into ECR.
This might not work, but try just running it, and don't give it any password, it might just run without it. I dont remember.
Alternatively, when prompted, put in the output of the aws cli command it requests *after* you have copied your temporary credentials into the shell from the portal. Ie, get temporary credntials from portal, paste into shell, run command, paste output into script's prompt, CTL-D to enter.

## How to update ##

Go to the path these files are in on the machine, and use

    git pull

to update from here.
Be aware you'll lose changes/screw it up if you make local changes then do the above.



