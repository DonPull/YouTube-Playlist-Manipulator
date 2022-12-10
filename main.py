import pathlib
import time

from selenium import webdriver

from seleniumMandatoryMethods import execute_script


def initialize(chrome_data_dir_path="chrome-data", chromedriver_path="chromedriver.exe"):
    script_directory = pathlib.Path().absolute()
    user_data_dir = str(pathlib.Path(script_directory)) + f"\\{chrome_data_dir_path}"

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    return driver


def move_videos_from_one_playlist_to_another(driver, from_playlist_url, to_playlist_url, number_of_videos_to_move=10, videos_offset=0, sort_method="newest-addition"):
    driver.get(to_playlist_url)
    to_playlist_name = execute_script(driver, 'return document.querySelector(".metadata-wrapper.style-scope.ytd-playlist-header-renderer").querySelector("#text").innerText')

    # change of plans... the comment line below was the old plan but the new one is: the bot is just going to require you to change your Google profile language to us if you want to use it (because it's way simpler and way more reliable)
    # change the Google profile language (because this bot relies on YouTube english text labels to select some elements/information)  (also this is not the best sopt for this piece of code... probably going to move it in the future)

    driver.get(from_playlist_url)

    # click the "Sort" button, so we can sort the playlist the way the user desires
    execute_script(driver, 'document.querySelector("tp-yt-paper-button#label.dropdown-trigger.style-scope.yt-dropdown-menu").click()')
    sort_map = {"newest-addition": "Date added (newest)", "oldest-addition": "Date added (oldest)", "most-popular": "Most popular", "newest-publish": "Date published (newest)", "oldest-publish": "Date published (oldest)"}
    try:
        execute_script(driver, 'document.querySelector("tp-yt-paper-listbox#menu.dropdown-content.style-scope.yt-dropdown-menu").querySelectorAll(".item.style-scope.yt-dropdown-menu").forEach(e => { if(e.innerText === "' + sort_map[sort_method] + '"){e.click()}})')
    except:
        raise Exception(f"Sort method: '{sort_method}' is not supported. Please, use one of the supported sort methods: [{', '.join(sort_map.keys())}]")

    # this code here waits for YouTube to actually sort the videos in the playlist before proceeding
    while True:
        try:
            execute_script(driver, 'document.querySelector(".reloading.ytd-playlist-video-list-renderer").click()', time_before_execute_sec=1, number_of_sec_before_fail=2)
        except: break

    videos_end_index = number_of_videos_to_move + videos_offset
    number_of_videos_in_playlist = int(execute_script(driver, 'return document.querySelector("yt-formatted-string.byline-item.style-scope.ytd-playlist-byline-renderer").querySelector("span").innerText').replace(",", "").replace(".", ""))

    if number_of_videos_in_playlist < videos_end_index:
        print(f"Attempted to get videos {videos_offset + 1}-{videos_end_index} ({videos_end_index - videos_offset} total), however there are only {number_of_videos_in_playlist} videos in the playlist. Getting videos {videos_offset + 1}-{number_of_videos_in_playlist} ({number_of_videos_in_playlist - videos_offset} total) instead.")
        videos_end_index = number_of_videos_in_playlist

    print(f"to_playlist_name: {to_playlist_name}")
    print(f"number_of_videos_to_move: {number_of_videos_to_move}")
    print(f"videos_offset: {videos_offset}")
    print(f"start from video: {videos_offset} and stop at video: {videos_end_index}")
    print(f"given sort method: {sort_method}  corresponding yt sort method: {sort_map[sort_method]}")

    # scroll if needed to render more videos from the playlist in order to get their urls
    number_of_scrolls_needed = int((videos_end_index + 5) / 100) # adding 5 to 'videos_end_index' just in case we go out of bounds even tho it should not happen
    old_number_of_rendered_videos = 100
    for scrollIndex in range(number_of_scrolls_needed):
        print(f"Need to scroll {number_of_scrolls_needed} times. Current scroll: {scrollIndex}")
        execute_script(driver, 'window.scrollTo(0, document.querySelector("#page-manager > ytd-browse").scrollHeight)')

        # wait for the videos to render before scrolling again
        while True:
            #print(f"In the video rendering wait while. Old number of rendered videos: {old_number_of_rendered_videos}. Current number of rendered videos: " + str(execute_script(driver, 'return document.querySelectorAll("ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer").length')))
            current_number_of_rendered_videos = int(execute_script(driver, 'return document.querySelectorAll("ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer").length'))
            if current_number_of_rendered_videos != old_number_of_rendered_videos:
                old_number_of_rendered_videos = current_number_of_rendered_videos
                break
            time.sleep(5)

    youtube_videos = str(execute_script(driver, f'let videosArray = document.querySelectorAll("ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer"); let videoUrlsString = ""; let videos_offset = {videos_offset}; let videos_end_index = {videos_end_index}; for(let i = videos_offset; i < videos_end_index; i++)' + '{ videoUrlsString += videosArray[i].querySelector("#video-title").href + " " } return videoUrlsString;')).rstrip().split(" ") # this 'rstrip' just removes the one trailing white space on the right of the string... also the script string is separated in two, so I can use fstring for the first one without messing with the brackets of the second string
    #for i in range(videos_offset, videos_end_index, 1):
        # todo: the way I'm doing it here is not optimal... going to the playlist to transfer every video manually (which requires going through a couple of menus) is just not optimal... The better way to do this is to save in a list the urls of all videos in the playlist, so that we can add threads to the bot. Afterwards the bot is going to go to each video's url and it's going to move the video from one playlist to another based on the names of the playlists (all of this is going to happen inside of threads so hopefully it happens quickly)
        # click the current video menu btn
        #execute_script(driver, f'document.querySelectorAll("ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer")[{i}].querySelector("#menu").querySelector("button#button").click()')

    print("printing videos array: ")
    print(youtube_videos)
    print("now waiting 100000sec... (waiting because the logic below is still not done)")
    time.sleep(100000)


# TEST AREA
# print(int(300/100))
#
# sleep_time = 1000000
# print(f"done testing... now sleeping for {sleep_time}sec")
# time.sleep(sleep_time)
# TEST AREA

# user inputs (please give them a value that is true for your local system, otherwise the bot won't work)
chrome_data_dir_path = "chrome-data"
chromedriver_path = "chromedriver.exe"
# user inputs (please give them a value that is true for your local system, otherwise the bot won't work)

driver = initialize(chrome_data_dir_path, chromedriver_path)
move_videos_from_one_playlist_to_another(driver, "https://www.youtube.com/playlist?list=WL", "https://www.youtube.com/playlist?list=PLlLaeBxLO4Kk0dxeqM2pTTe7rlKsAYjUT", 5, 515, "oldest-addition")

# code I will probably need later ->
# get all currently rendered videos inside the playlist:
# document.querySelectorAll("ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer")
#
# scroll to the bottom of the currently rendered videos inside the playlist so that more videos render: (in order to know how many videos need to be rendered (so the bot knows when to stop scrolling) extract the number of videos in the playlist (yt gives us this info directly inside the playlist))
# let container = document.querySelector("#page-manager > ytd-browse:nth-child(3)"); window.scrollTo(0, container.scrollHeight)