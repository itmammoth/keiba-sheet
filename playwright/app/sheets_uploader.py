from typing import Dict, List

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class GoogleSheetsUploader:
    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        self.service = self._get_service()

    def _get_service(self):
        # サービスアカウント認証を使用
        creds = Credentials.from_service_account_file(
            "keiba-sheet-py-key.json", scopes=SCOPES
        )
        return build("sheets", "v4", credentials=creds)

    def create_sheet(self, sheet_name: str) -> str:
        """新しいシートを作成し、実際に作成されたシート名を返す"""
        # 既存のシート名をチェック
        spreadsheet = (
            self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        )
        existing_sheets = [
            sheet["properties"]["title"] for sheet in spreadsheet["sheets"]
        ]

        # 重複を避けるためにシート名を調整
        final_sheet_name = sheet_name
        counter = 1
        while final_sheet_name in existing_sheets:
            final_sheet_name = f"{sheet_name}_{counter}"
            counter += 1

        # 新しいシートを作成
        request = {
            "requests": [{"addSheet": {"properties": {"title": final_sheet_name, "index": 0}}}]
        }

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id, body=request
        ).execute()

        return final_sheet_name

    def upload_data(self, sheet_name: str, data: List[List[str]]) -> None:
        """データをシートにアップロード"""
        # データの最大列数を計算
        max_cols = max(len(row) for row in data) if data else 1
        end_column = chr(ord("A") + max_cols - 1)
        range_name = f"{sheet_name}!A1:{end_column}{len(data)}"

        # データをアップロード
        body = {"values": data}

        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        ).execute()

    def upload_race_data(
        self, race_info: Dict[str, str], headers: List[str], race_data: List[List[str]]
    ) -> str:
        """競馬データを新しいシートにアップロード"""
        # 今日の日付を使用してシート名を作成
        from datetime import datetime
        today = datetime.now().strftime("%Y%m%d")
        sheet_name = f"{today}_{race_info['race_name']}"

        actual_sheet_name = self.create_sheet(sheet_name)

        # アップロード用のデータを構築
        upload_data = []

        # レース情報を最初の3行に追加
        upload_data.append([race_info["race_name"]])
        upload_data.append([race_info["race_data1"]])
        upload_data.append([race_info["race_data2"]])
        upload_data.append([])  # 空行

        # ヘッダーを追加
        upload_data.append(headers)

        # レースデータを追加
        upload_data.extend(race_data)

        # データをアップロード
        self.upload_data(actual_sheet_name, upload_data)

        return actual_sheet_name
