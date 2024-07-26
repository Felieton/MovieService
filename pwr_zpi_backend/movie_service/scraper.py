from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lxml import etree
import requests
from translate import Translator

allowed_netlocs = [
    'www.filmweb.pl',
    'www.imdb.com'
]


def getPageSource(url):
    page = requests.get(url)
    return page.text


def getFilmInfoFilmweb(url):
    translator = Translator(to_lang="en", from_lang='pl')
    page_source = getPageSource(url)
    soup = BeautifulSoup(page_source, "html.parser")
    if soup is None:
        return 'Wrong url'
    title = soup.find("h1", "filmCoverSection__title")
    year = soup.find("span", "filmCoverSection__year")
    time = soup.find("span", "filmCoverSection__filmTime")
    plot = soup.find("div", "filmPosterSection__plot clamped")
    filmInfo = soup.find_all("div", "filmInfo__info")
    film_info_actors = soup.find("div",
                                 "page__container page__container--bottom page__container--paddingless page__navContent")

    genres = []
    countries = []
    actors = []
    characters = []

    for genre in filmInfo[2].find_all("a"):
        genres.append(translator.translate(genre.get_text()))

    for country in filmInfo[3].find_all("a"):
        countries.append(country.get_text())

    for actor in film_info_actors.find_all("h3", "personRole__person"):
        actors.append(actor.find("a").get_text())

    for character in film_info_actors.find_all("div", "personRole__role"):
        characters.append(character.get_text())

    return {
        "title": title.get_text(),
        "year": year.get_text(),
        "duration": time.get_text(),
        "genres": genres,
        "countries": countries,
        "actors": actors,
        "characters": characters,
        "plot": plot.get_text(),
    }


def getFilmInfoIMDB(url):
    page_source = getPageSource(url)
    soup = BeautifulSoup(page_source, "html.parser")
    if soup is None:
        return 'Wrong url'
    title = soup.find("h1", "TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG")
    og_title = soup.find("div", "OriginalTitle__OriginalTitleText-jz9bzr-0")
    film_details = soup.find("ul", "TitleBlockMetaData__MetaDataList-sc-12ein40-0")
    duration = film_details.find_all("li", "ipc-inline-list__item")[-1]
    film_details = film_details.find_all("span", "TitleBlockMetaData__ListItemText-sc-12ein40-2")
    genres_and_plot = soup.find("div", "GenresAndPlot__ContentParent-cum89p-8")
    genres = genres_and_plot.find("div", "GenresAndPlot__GenresChipList-cum89p-4")
    genres = genres.find_all("a", "GenresAndPlot__GenreChip-cum89p-3")

    countries = []
    plot = genres_and_plot.find("span", "GenresAndPlot__TextContainerBreakpointXS_TO_M-cum89p-0")
    film_info = soup.find("section",
                          "ipc-page-section ipc-page-section--base StyledComponents__CastSection-y9ygcu-0 fswvJC "
                          "celwidget")

    actors_and_characters = soup.find_all("div", "StyledComponents__CastItemSummary-y9ygcu-9 fBAofn")
    actors = []
    characters = []

    for ac in actors_and_characters:
        actors.append(ac.find("a").get_text())
        characters.append(ac.find("div", "title-cast-item__characters-list").get_text().split("as")[-1])

    return {
        "title": title.get_text(),
        "year": film_details[0].get_text(),
        "duration": duration.get_text(),
        "genres": [g.get_text() for g in genres],
        "countries": countries,
        "actors": actors,
        "characters": characters,
        "plot": plot.get_text(),
    }


def checkCorrectUrl(url):
    parsed = urlparse(url)
    return parsed.netloc in allowed_netlocs


def getBySearchFilmweb(title):
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("window-size=1200x600")

    chrome_path = which("chromedriver.exe")

    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_option)
    driver.maximize_window()

    driver.get('https://www.filmweb.pl')

    search = driver.find_element(by='xpath', value='//*[@id="inputSearch"]')
    driver.implicitly_wait(10)

    search.send_keys(title)

    driver.implicitly_wait(10)
    film = driver.find_element(by='xpath', value='/html/body/div[6]/div/div/div[1]/div[1]/div[3]/div[1]/div[1]/a')
    return film.get_attribute('href')


def getBySearchIMDB(title):
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("window-size=1200x600")

    chrome_path = which("chromedriver.exe")
    print(chrome_path)
    driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_option)
    driver.maximize_window()

    driver.get('https://www.imdb.com')

    search = driver.find_element(by='xpath', value='/html/body/div[2]/nav/div[2]/div[1]/form/div[2]/div/input')
    driver.implicitly_wait(10)

    search.send_keys(title)
    driver.implicitly_wait(10)

    film = driver.find_element(by='xpath',
                               value='/html/body/div[2]/nav/div[2]/div[1]/form/div[2]/div/div/div/ul/li[1]/a')
    return film.get_attribute('href')


def getFromPageSourceWithXPATH(page_source, xpath):
    if xpath is None:
        return None
    if xpath[-2:] == "ul":
        return getListFromPageSourceWithXPATH(page_source, xpath)
    soup = BeautifulSoup(page_source, "html.parser")
    dom = etree.HTML(str(soup))
    return dom.xpath(xpath)[0].text


def getFromPageSourceWithClass(page_source, tag, classname):
    soup = BeautifulSoup(page_source, "html.parser")
    dom = etree.HTML(str(soup))
    res = dom.findall(f".//{tag}[@class='{classname}']")
    for l in res:
        if l.text is None:
            print(l[0].text)
        else:
            print(l.text)


def getListFromPageSourceWithXPATH(page_source, xpath):
    soup = BeautifulSoup(page_source, "html.parser")
    dom = etree.HTML(str(soup))
    list = dom.xpath(xpath)[0].findall('./li')
    res = []
    for l in list:
        res.append(l[0].text)
    return res
