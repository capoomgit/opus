# NAMES
HDA_NAME = r"{hda}_{pid}_{wid}"
MERGE_NAME = r"merged_{pid}_{wid}"

# FOLDERS
HDA_ROOT_FOLDER = r"P:/pipeline/standalone_dev/saved/{pid}/hdas/"
MERGE_ROOT_FOLDER = r"P:/pipeline/standalone_dev/saved/{pid}/end/"
ERROR_ROOT_FOLDER = r"P:/pipeline/standalone_dev/saved/{pid}/errors/"
PROJECT_FOLDER = r"{hda}_{pid}/"
OUT_FOLDER = r"Out_{out}/"

# TODO check if string contains the needed kwarg first
def conv(path : str, **kwargs):
    new_path = path

    new_path = new_path.replace(r"{wid}", str(kwargs["wid"]))
    new_path = new_path.replace(r"{pid}", str(kwargs["pid"]))
    new_path = new_path.replace(r"{hda}", str(kwargs["hda"]))
    new_path = new_path.replace(r"{out}", str(kwargs["out"]))
    return new_path
    
