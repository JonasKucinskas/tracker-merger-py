from simple_term_menu import TerminalMenu
import utils
from jackett import search, getTrackers
import torrent_parser  
import json

def main():
    qb = utils.init_qb_client()
    
    #get torrents
    torrents = qb.torrents_info(sort='added_on')[::-1]
    torrent_options = []
    for torrent in torrents:
        torrent_options.append(torrent['name'])

    selected_torrent_index = utils.select_from_menu(torrent_options, title="Select a torrent")
    selected_torrent_name = torrent_options[selected_torrent_index]

    for torrent in torrents:
        if selected_torrent_name == torrent['name']:
            selected_torrent = torrent
            continue
        

    #select trackers
    trackers = getTrackers()
    tracker_options = ['All']
    for tracker in trackers:
        tracker_options.append(tracker['Name'])

    selected_tracker_index = utils.select_from_menu(tracker_options, title="Select a tracker")
    if selected_tracker_index == 0:
        selected_tracker_id = 'All'
    else:
        selected_tracker_id = trackers[selected_tracker_index - 1]['ID']

    print("Searching using Jackett...")
    global results
    results = search(selected_torrent_name, selected_tracker_id)
    if not results:
        print("No results found.")
        return

    #show searched torrents
    global result_titles
    result_titles = []
    for result in results:
        result_titles.append(result['Title'])

    def preview_command(selected_item):
        return utils.get_preview(selected_item, results)
    
    terminal_menu = TerminalMenu(
        result_titles,
        title = f"Original torrent: {selected_torrent['name']} {utils.to_readable_size(selected_torrent['size'])}",
        preview_command = preview_command,
        preview_size = 0.75,
    )
    selected_result_index = terminal_menu.show()

    #pasirenka norima siusti torrenta
    #issaugoti jo torrent faila
    #parodyti jo struktura
    #pasirenka ar kur nori saugoti
    #gali grizti atgal ir is naujo pasirinkti torrenta.


    new_torrent_name = result_titles[selected_result_index]
    #get either magnet url or file
    link = utils.get_download_link(new_torrent_name, results)
    
    if not link:
        return
    
    utils.save_torrent_file(new_torrent_name, link=link)
    utils.save_torrent_file(f"{selected_torrent['name']}-original", data=qb.torrents_export(selected_torrent['hash']))
    
    print("Original torrent structure:")
    file_data_list = torrent_parser.parse_torrent(f"torrentfiles/{selected_torrent['name']}-original.torrent")
    result = torrent_parser.build_path_tree(file_data_list)
    print(json.dumps(result, indent=2))

    print("New torrent structure:")
    file_data_list = torrent_parser.parse_torrent
    file_data_list = torrent_parser.parse_torrent(f"torrentfiles/{new_torrent_name}.torrent")
    result = torrent_parser.build_path_tree(file_data_list)
    print(json.dumps(result, indent=2))

    #select path
    dirs = [selected_torrent['content_path'], selected_torrent['save_path']]

    selected_dir_index = utils.select_from_menu(dirs, title="Save where?")
    selected_dir_name = dirs[selected_dir_index]

    #utils.download(qb, link, selected_dir_name)
    qb.auth_log_out()


if __name__ == "__main__":
    main()
