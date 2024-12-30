import bencodepy as bcp
from utils import to_readable_size

def parse_torrent(torrent_file_path: str) -> list[dict]:
   
    with open(torrent_file_path, "rb") as f:
        torrent_data = bcp.Bencode(encoding="utf-8", encoding_fallback="value").decode(f.read())

    file_data_list = []
    if "info" in torrent_data and "files" in torrent_data["info"]:
        files_len = len(torrent_data["info"]["files"])
        for file_info in torrent_data["info"]["files"]:
            length = file_info["length"]
            path = "/".join(file_info["path"])
            if files_len > 1:
                path = torrent_data["info"]["name"] + "/" + path

            file_data_list.append({"path": path, "length": length})

    return file_data_list

def build_path_tree(file_data_list: list[dict]) -> dict:
    
    def _recurse(dic, path_parts, length):
        if not path_parts:
            return
        if len(path_parts) == 1:
            dic[path_parts[0]] = length
            return
        key, *new_path_parts = path_parts
        if key not in dic:
            dic[key] = {}
        _recurse(dic[key], new_path_parts, length)

    path_dict = {}
    for file_info in file_data_list:
        path_parts = file_info["path"].split("/")
        file_length = file_info["length"]
        _recurse(path_dict, path_parts, to_readable_size(file_length))

    return path_dict