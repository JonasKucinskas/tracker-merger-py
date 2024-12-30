import qbittorrentapi
from simple_term_menu import TerminalMenu
from pathlib import Path
import requests
from dotenv import load_dotenv
import os
load_dotenv()


# Initialize qBittorrent client
def init_qb_client():

    conn_info = dict(
        host = os.getenv("QB_HOST"),
        port = os.getenv("QB_PORT"),
        username = os.getenv("QB_USERNAME"),
        password = os.getenv("QB_PASSWORD"),

    )

    qb = qbittorrentapi.Client(**conn_info)
    qb.auth_log_in()
    return qb

# Convert bytes to human-readable size
def to_readable_size(bytes):
    units = ['B', 'KB', 'MB', 'GB']
    for unit in units:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} {units[-1]}"

# Format search result dictionary to a string
def format_result(result):
    if 'MagnetUri' in result:
        magnet_uri = result['MagnetUri']
    else:
        magnet_uri = 'None'

    return (
        f"Seeders: {result['Seeders']}\n"
        f"Peers: {result['Peers']}\n"
        f"Size: {to_readable_size(result['Size'])}\n"
        f"Tracker: {result['Tracker']}\n"
        f"TrackerType: {result['TrackerType']}\n"
        f"CategoryDesc: {result['CategoryDesc']}\n"
        f"Guid: {result['Guid']}\n"
        f"Link: {result['Link']}\n"
        f"Magnet: {magnet_uri}\n"
    )

def get_preview(selected_item, results):
    for result in results:
        if result['Title'] == selected_item:
            return format_result(result)
    return "Preview unavailable."

def get_download_link(selected_item, results):
    for result in results:
        if result['Title'] == selected_item:
            if not result['Link']:
                print("Url for this torrent does not exist.")
            return result['Link']

def download(qb, link, path):

    if link.startswith('http'):
        response = requests.get(link)
        if response.status_code == 200:
            qb.torrents_add(torrent_files=response.content, save_path=path)
        else:
            print("Failed to fetch the torrent file.")
    else:
        qb.torrents_add(urls=link, save_path=path)

def select_from_menu(options, title="Select an option"):
    terminal_menu = TerminalMenu(options, title=title)
    return terminal_menu.show()

def has_file_extension(path):
    return bool(Path(path).suffix)

def save_torrent_file(filename, link=None, data=None):
    
    if link and not data:
        response = requests.get(link, stream=True)
        response.raise_for_status()  
        data = response.content

    if data:
        with open(f"torrentfiles/{filename}.torrent", "wb") as file:
                file.write(data)