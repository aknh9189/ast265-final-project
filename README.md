# ast265-final-project

## Deps
Needs pyyaml 
`pip install pyyaml`

## Monitoring Runs
Need to change all instances of `Ice` to the name of the example directory you are running (ex `demo2D`). All running iSALE examples must be in this folder. 
`python monitor_runs.py`, or `./monitor_runs` if you've chmod +x'd the file 

## Running a job

### Setting up YAML file
Modify `job_desc.yaml` to specify the number of parallel jobs you want to run and the name of the "template" directory that will be copied and modified to perform your run.

Set the variables you want changed between runs in asteroid.inp in the YAML file.

The template directory (just one of the examples, ex `Planet2D` or `demo2D`) must be in this project's folder

### Result processing
You must include result copying code from other repo or modify the `run_job` function in `runJob.py`. You can also just remove the `cleanup_job` function in `runJob.py`. To use newresult in `ast265-final-data` (other repo), repo must be in this folder. 

Start a job with `python runJob.py -y job_desc.yaml`
