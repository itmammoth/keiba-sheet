import argparse
import os
import re
from typing import Dict, List

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from sheets_uploader import GoogleSheetsUploader

load_dotenv()


def get_race_data(race_id: str) -> tuple[Dict[str, str], List[str], List[List[str]]]:
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
    keibajo = race_data2.split(" ")[1]

    # レース情報を辞書として格納
    race_info = {
        "race_name": race_name,
        "race_data1": race_data1,
        "race_data2": race_data2,
    }

    # ヘッダー情報
    headers = [
        "枠番",
        "印",
        "馬番",
        "馬名",
        "性",
        "齢",
        "斤量",
        "騎手",
        "厩舎",
        "調教師",
        "仕上がり",
        "馬体重",
        "オッズ",
        "人気",
        "パドック",
        "メモ",
    ]

    SEX_AGE_RE = re.compile(r"^(?P<sex>[^\d]+)(?P<age>\d+)$")

    # 馬データを収集
    horses_data = []
    for horse_list in soup.select("table.ShutubaTable tr.HorseList"):
        waku = horse_list.select("td")[0].text.strip()
        number = horse_list.select("td")[1].text.strip()
        horse_name = horse_list.select("td")[3].text.strip()
        sex_and_age = horse_list.select("td")[4].text.strip()
        m = SEX_AGE_RE.fullmatch(sex_and_age)
        sex = m.group("sex")
        age = m.group("age")
        carrying_weight = horse_list.select("td")[5].text.strip()
        jockey = horse_list.select("td")[6].text.strip()
        trainer_info = horse_list.select("td")[7].text.strip()
        stable = trainer_info[:2]
        trainer = trainer_info[2:]
        horse_weight = horse_list.select("td")[8].text.strip()
        odds = horse_list.select("td")[9].text.strip()
        popularity = horse_list.select("td")[10].text.strip()

        horses_data.append(
            [
                waku,
                "",  # 印
                number,
                horse_name,
                sex,
                age,
                carrying_weight,
                jockey,
                stable_disp(stable, keibajo),
                trainer,
                "",  # 仕上がり
                horse_weight,
                odds,
                popularity,
                "",  # パドック
                "",  # メモ
            ]
        )

    return race_info, headers, horses_data


def print_csv(
    race_info: Dict[str, str], headers: List[str], horses_data: List[List[str]]
):
    """CSVフォーマットで出力"""
    print(f'"{race_info["race_name"]}"')
    print(f'"{race_info["race_data1"]}"')
    print(f'"{race_info["race_data2"]}"')
    print()

    print(",".join(headers))
    for horse_data in horses_data:
        print(",".join(horse_data))


def upload_to_sheets(
    race_info: Dict[str, str], headers: List[str], horses_data: List[List[str]]
):
    """Google Sheetsにアップロード"""
    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
    if not spreadsheet_id:
        print("エラー: GOOGLE_SHEETS_SPREADSHEET_IDが設定されていません")
        return

    try:
        uploader = GoogleSheetsUploader(spreadsheet_id)
        sheet_name = uploader.upload_race_data(race_info, headers, horses_data)
        print(f"データをGoogle Sheetsにアップロードしました: シート名 '{sheet_name}'")
    except Exception as e:
        print(f"Google Sheetsへのアップロードエラー: {e}")


def main():
    parser = argparse.ArgumentParser(description="netkeiba競馬データ取得ツール")
    parser.add_argument("race_id", help="レースID")
    parser.add_argument(
        "--upload", action="store_true", help="Google Sheetsにアップロード"
    )
    args = parser.parse_args()

    # データを取得
    race_info, headers, horses_data = get_race_data(args.race_id)

    if args.upload:
        upload_to_sheets(race_info, headers, horses_data)
    else:
        print_csv(race_info, headers, horses_data)


def stable_disp(stable: str, keibajo: str) -> str:
    if stable == "栗東" and (keibajo == "阪神" or keibajo == "京都"):
        return "栗東+"
    elif stable == "美浦" and (keibajo == "東京" or keibajo == "中山"):
        return "美浦+"
    else:
        return stable


def get_html(race_id: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(
            f"https://race.netkeiba.com/race/shutuba.html?race_id={race_id}&rf=shutuba_submenu",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(3 * 1000)
        page.screenshot(path="tmp/netkeiba.png")
        html = page.content()
        browser.close()
    return html


if __name__ == "__main__":
    main()
