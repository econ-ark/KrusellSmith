# Run a Jupyter notebook in a Docker container in order to test it
import argparse
import subprocess


def reproduce_quark():
    # Take the file as an argument
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--timeout", help="indvidual cell timeout limit, default 600s"
    )
    parser.add_argument(
        "--notebook", help="path to notebook"
    )
    parser.add_argument(
        "--script", help="path to a python script"
    )

    args = parser.parse_args()

    if args.notebook is None and args.script is None:
        print('Please provide either a notebook or a script as input file')
        return
    else:
        # make this more beautiful
        if args.notebook is not None and args.notebook[-6:] == '.ipynb':
            pass
        elif args.script is not None and args.script[-3:] == '.py':
            pass
        else:
            print("Make sure you have provided a notebook file (.ipynb) or a python script (.py) as input file")
            return


    # remove extension from the name
    NOTEBOOK_NAME = args.notebook[:-6] if args.notebook is not None else None
    SCRIPT_NAME = args.script[:-3] if args.script is not None else None
    #NOTEBOOK_NAME = f"notebooks/LifeCycleModelExample-Problems-And-Solutions"

    DOCKER_IMAGE = f"econark/econ-ark-notebook"
    TIMEOUT = args.timeout if args.timeout is not None else 600

    pwd = subprocess.run(["pwd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # make sure mount is in home directory, i.e go up Code/Python
    mount = str(pwd.stdout)[2:-15] + ":/home/jovyan/work"
    print(mount )
    # mount the present directory and start up a container
    print('Fetching the docker copy for reproducing results, this may take some time if running the reproduce.py command for the first time')
    container_id = subprocess.run(
        ["docker", "run", "-v", mount, "-d", DOCKER_IMAGE], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    container_id = container_id.stdout.decode("utf-8")[:-1]
    print('A docker container is created to execute the notebook')

    # go into Code/Python to find the notebook/script
    PATH_TO_NOTEBOOK = f"/home/jovyan/work/Code/Python/"

    if NOTEBOOK_NAME is not None:
        # copy the notebook file to reproduce notebook
        subprocess.run(
            [
                f"docker exec -it  {container_id} bash -c 'cp {PATH_TO_NOTEBOOK}{NOTEBOOK_NAME}.ipynb {PATH_TO_NOTEBOOK}{NOTEBOOK_NAME}-reproduce.ipynb'"
            ],
            shell=True,
        )

        # execute the reproduce notebook
        subprocess.run(
            [
                f"docker exec -it  {container_id} bash -c 'jupyter nbconvert --ExecutePreprocessor.timeout={TIMEOUT} --to notebook --inplace --execute {PATH_TO_NOTEBOOK}{NOTEBOOK_NAME}-reproduce.ipynb'"
            ],
            shell=True,
        )
    else:
        # execute the script
        subprocess.run(
            [
                f"docker exec -it  {container_id} bash -c 'ipython {PATH_TO_NOTEBOOK}{SCRIPT_NAME}.py'"
            ],
            shell=True,
        )


    subprocess.run([f"docker stop {container_id}"], shell=True)


reproduce_quark()
