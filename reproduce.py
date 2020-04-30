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
        "notebook", help="path to notebook"
    )
    args = parser.parse_args()

    if args.notebook is not None and args.notebook[-6:] != '.ipynb':
        print("Make sure you have provided a notebook file (.ipynb) as input file")
        return
    # remove .ipynb extension from the name
    NOTEBOOK_NAME = args.notebook[:-6]
    #NOTEBOOK_NAME = f"notebooks/LifeCycleModelExample-Problems-And-Solutions"

    DOCKER_IMAGE = f"econark/econ-ark-notebook"
    TIMEOUT = args.timeout if args.timeout is not None else 600

    pwd = subprocess.run(["pwd"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mount = str(pwd.stdout)[2:-3] + ":/home/jovyan/work"
    # mount the present directory and start up a container
    print('Fetching the docker copy for reproducing results, this may take some time if running the reproduce.py command for the first time')
    container_id = subprocess.run(
        ["docker", "run", "-v", mount, "-d", DOCKER_IMAGE], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    container_id = container_id.stdout.decode("utf-8")[:-1]
    print('A docker container is created to execute the notebook')
    PATH_TO_NOTEBOOK = f"/home/jovyan/work/"

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

    subprocess.run([f"docker stop {container_id}"], shell=True)


reproduce_quark()
