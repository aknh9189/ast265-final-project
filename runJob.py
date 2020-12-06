#!/usr/bin/python

import argparse, os, shutil, sys, yaml, multiprocessing, time

data_dir = './data'

parser = argparse.ArgumentParser(description="tmp")
parser.add_argument('-y', '--yamlfile', type=str, required=True)

args = parser.parse_args()

with open(args.yamlfile, 'r') as f:
    data = yaml.load(f)
print(data)

template_dir = data['system']['template_dir']

def create_job(job):
    job_id = job['id']
    variables = job['variables']
    shutil.copytree(template_dir, job_id)
    curdur = os.getcwd()
    os.chdir(job_id)
    f = open("asteroid.inp", 'r+')
    text = f.read()
    for v in variables:
        linestart = text.find(v)
        lineend = text.find("\n", linestart)
        line = text[linestart:lineend]
        parts = line.split(":")
        for i in range(len(variables[v])): # for each value to set 
            part = parts[i+1]
            spaces = part.split(" ")
            max_i = spaces.index(max(spaces, key=len))
            spaces[max_i] = variables[v][i]
            parts[i+1] = " ".join(spaces)
            
        newline = ":".join(parts)
        text = text.replace(line, newline)
    f.seek(0)
    f.write(text)
    f.close()
    os.chdir(curdur)

def run_job(job):
    curdur = os.getcwd()
    os.chdir(job['id'])
    os.system('./iSALE2D > /dev/null')
    os.chdir(curdur)
    os.chdir("ast265-final-data")
    os.system("./newresult -p ../{} -n {} > /dev/null".format(job['id'], job['id']))
    os.chdir(curdur)

def cleanup_job(job):
    shutil.rmtree(job['id'])

def complete_job(job):
    print("Starting job " + job['id'] + " at " + str(time.time()))
    create_job(job)
    run_job(job)
    cleanup_job(job)
    print("Completing job " + job['id'] + " at " + str(time.time()))


if __name__ == '__main__':
    p = multiprocessing.Pool(data['system']['jobs'])
    p.map(complete_job, data['jobs'])
