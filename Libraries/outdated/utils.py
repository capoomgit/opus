import os

def add_paths():
    path_contents = os.environ["Path"].split(";")

    required = ["C:/Program Files/Side Effects Software/Houdini 19.0.657/bin"]
    # "C:/Program Files/Side Effects Software/Houdini 19.0.657/houdini/python3.7libs"
    # Create PYTHONPATH environment

    # os.environ["PYTHONPATH"] = "C:/Program Files/Side Effects Software/Houdini 19.0.657/houdini/python3.7libs"
    
    # if PYTHONPATH is not exist in the environment, create it
    if "PYTHONPATH" not in os.environ:
        os.system(r'setx PYTHONPATH "C:\Program Files\Side Effects Software\Houdini 19.0.657\houdini\python3.7libs"')
        print("PYTHONPATH created")
        return True
    else:
        return False
    # print(os.environ["PYTHONPATH"])
    # for x in required:
    #     if x not in path_contents:
    #         os.environ["Path"] += f";{x}"
    #         print(f"Required path variable added; {x}")
