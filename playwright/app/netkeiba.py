import sys

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


def main(race_id: str):
    html = get_html(race_id)
    soup = BeautifulSoup(html, "html.parser")

    race_list_name_box = soup.select_one(".RaceList_NameBox")
    race_name = race_list_name_box.select_one(".RaceName").text.strip()
    race_data1 = (
        race_list_name_box.select_one(".RaceData01").text.strip().replace("\n", " ")
    )
    race_data2 = (
        race_list_name_box.select_one(".RaceData02").text.strip().replace("\n", " ")
    )
    print(race_name)
    print(race_data1)
    print(race_data2)

    for horse_list in soup.select("table.ShutubaTable tr.HorseList"):
        waku = horse_list.select("td")[0].text.strip()
        number = horse_list.select("td")[1].text.strip()
        horse_name = horse_list.select("td")[3].text.strip()
        age = horse_list.select("td")[4].text.strip()
        carrying_weight = horse_list.select("td")[5].text.strip()
        jockey = horse_list.select("td")[6].text.strip()
        trainer_info = horse_list.select("td")[7].text.strip()
        stable = trainer_info[:2]
        trainer = trainer_info[2:]
        horse_weight = horse_list.select("td")[8].text.strip()
        odds = horse_list.select("td")[9].text.strip()
        popularity = horse_list.select("td")[10].text.strip()

        print(
            ",".join(
                [
                    waku,
                    number,
                    horse_name,
                    age,
                    carrying_weight,
                    jockey,
                    stable,
                    trainer,
                    horse_weight,
                    odds,
                    popularity,
                ]
            )
        )


def get_html(race_id: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(
            f"https://race.netkeiba.com/race/shutuba.html?race_id={race_id}&rf=shutuba_submenu",
            wait_until="domcontentloaded",
        )
        page.screenshot(path="tmp/netkeiba.png")
        html = page.content()
        browser.close()
    return html


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python netkeiba.py <race_id>")
        sys.exit(1)
    race_id = sys.argv[1]
    main(race_id)
