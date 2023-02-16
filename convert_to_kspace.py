import os
from pathlib import Path
import json
import io
# open convert_to_kspace.net file as dictionary but ommits the first line

class ConvertToKspace(object):
    """
    Convert raw data from Philips to kspace through gpi
    """
    NETWORK_FILE = "convert_to_kspace.net"

    @classmethod
    def _make_dict(cls, lines):
        output = io.StringIO()
        for line in lines:
            output.write(line)

        # load output as dictionary
        output.seek(0)
        data = json.load(output)
        return data
    
    @classmethod
    def _change_paths(cls, data, raw_file_path, kspace_file_path):
        # Make new file paths
        data["nodes"]["nodes"][1]["widget_settings"]["parms"][1]["kwargs"]["directory"] = str(Path(raw_file_path).parent)
        data["nodes"]["nodes"][1]["widget_settings"]["parms"][1]["kwargs"]["val"] = str(raw_file_path)

        data["nodes"]["nodes"][2]["widget_settings"]["parms"][0]["kwargs"]["directory"] = str(Path(kspace_file_path).parent)
        data["nodes"]["nodes"][2]["widget_settings"]["parms"][0]["kwargs"]["val"] = str(kspace_file_path)
        return data

    @classmethod
    def _write_network_file(cls, raw_file_path, kspace_file_path):
        with open("convert_to_kspace.net", "r") as f:
            lines = f.readlines()
            first_line = lines[0]
            lines = lines[1:]

        data = cls._make_dict(lines)
        data = cls._change_paths(data, raw_file_path, kspace_file_path)
        # Create new newtwork file with new paths
        with open("convert_to_kspace_mod.net", "w") as f:
            f.write(first_line)
            json.dump(data, f, indent=4)
    
    @classmethod
    def convert(cls, raw_file_path, kspace_file_path):
        cls._write_network_file(raw_file_path, kspace_file_path)
        Path(kspace_file_path).parent.mkdir(parents=True, exist_ok=True)
        os.system("gpi --nogui convert_to_kspace_mod.net")

if __name__ == "__main__":
    file_dir = "/your/kspace/file/dir"
    save_dir = Path("/where/you/want/to/save/kspace")

    files = list()
    # Walk over all .raw and .data files in directory and subdirectories
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith(".raw"):
                file_path = os.path.join(root, file)
                print('-'*30)
                print(file_path)
                print('-'*30)
                # fetch subdirs not including file_dir when file_dir have unknown length
                subdirs = Path(file_path).parts[len(Path(file_dir).parts):-1]  # Don't include file name
                kspace_file_path = save_dir.joinpath(*subdirs, Path(file_path).stem + ".npy")
                ConvertToKspace.convert(file_path, kspace_file_path)
