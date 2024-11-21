# How is this lab tested?

Last tested: September 2024

We use automation to verify the completeness of this lab. It works as follows

1. A script is run that extracts all the commands you have to run from the documents you work from, in the order that you have to run them right up to and including the [smoke test](./16-smoke-test.md) step.
1. The extracted commands are chained together into script files which are then executed against the running virtual machines and the correct operation of the smoke test at the end is validated.

The key thing about this is that the commands to run are extracted directly from the documentation for this lab. meaning that the test is doing each step that you are supposed to do in the order that you should be doing them, thus it validates the correctness of the lab documentation.

So, if you have got all 5 virtual machines running and you can log into all 5 individually from your laptop command prompt using `vagrant ssh`, and also to each of the other 4 VMs by using `ssh` from the command prompt on `controlplane01` (after having completed the `ssh-keygen` and associated steps at the beginning), then any failure for the cluster to come up is 99.9% you made a mistake somewhere and 0.1% a bug in this lab!

The only time when this may *not* be the case is if we have not tested it for some months and something has changed e.g. in a newer version of Kubernetes, etcd or other components that this lab does not yet cater for. In that case we would make a bug fix and verify it works using the above methods.

When you do call for help, the first thing we would do is to run this test again to check your issue isn't down to the 0.1% mentioned above. If it does not, then we're going to tell you that you made a mistake and need to redo the lab!

Issues with getting the virtual machines started in the first place are *not* covered by the above tests so please continue to ask about that.

[Back to start](../README.md)