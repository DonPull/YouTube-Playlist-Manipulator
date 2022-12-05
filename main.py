import pathlib
import time

from selenium import webdriver

from seleniumMandatoryMethods import execute_script


def initialize(chrome_data_dir_path="chrome-data", chromedriver_path="chromedriver.exe"):
    script_directory = pathlib.Path().absolute()
    user_data_dir = str(pathlib.Path(script_directory)) + f"\\{chrome_data_dir_path}"

    options = webdriver.ChromeOptions()
    print(user_data_dir)
    options.add_argument(f"--user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

    return driver


def move_videos_from_one_playlist_to_another(driver, from_playlist_url, to_playlist_url, number_of_videos_to_move=10):
    driver.get(to_playlist_url)
    to_playlist_name = execute_script(driver, 'return document.querySelector(".metadata-wrapper.style-scope.ytd-playlist-header-renderer").querySelector("#text").innerText')
    driver.get(from_playlist_url)

    for i in range(number_of_videos_to_move):
        # todo: the way I'm doing it here is not optimal... going to the playlist to transfer every video manually (which requires going through a couple of menus) is just not optimal... The better way to do this is to save in a list the urls of all videos in the playlist, so that we can add threads to the bot. Afterwards the bot is going to go to each video's url and it's going to move the video from one playlist to another based on the names of the playlists (all of this is going to happen inside of threads so hopefully it happens quickly)
        # click the current video menu btn
        execute_script(driver, f'document.querySelectorAll("ytd-playlist-video-renderer.style-scope.ytd-playlist-video-list-renderer")[{i}].querySelector("#menu").querySelector("button#button").click()')


# user inputs (please give them a value that is true for your local system, otherwise the bot won't work)
chrome_data_dir_path = "chrome-data"
chromedriver_path = "chromedriver.exe"
# user inputs (please give them a value that is true for your local system, otherwise the bot won't work)

driver = initialize(chrome_data_dir_path, chromedriver_path)
move_videos_from_one_playlist_to_another(driver, "https://www.youtube.com/playlist?list=WL", "https://www.youtube.com/playlist?list=PLlLaeBxLO4Kk0dxeqM2pTTe7rlKsAYjUT")