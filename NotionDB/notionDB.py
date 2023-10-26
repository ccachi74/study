'''
NotionDB 값 읽기
'''

import requests, json

def readDatabase(databaseId, headers):
    
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers=headers)
    print(res.status_code)

    data = res.json()
    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
    
    if res.status_code == 200:
        for result in data['results']:
            try:
                properties = result['properties']
                col1 = properties['이름']['title'][0]['text']['content']
                col2 = properties['상태']['rich_text'][0]['text']['content']
                print(f'이름: {col1}, 상태: {col2}')
            except:
                continue
        
def createPage(databaseId, headers, page_values):

    createdUrl = "https://api.notion.com/v1/pages"

    newPageData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": page_values['이름']
                        }
                    }
                ]
            },
            "상태": {
                "rich_text": [
                    {
                        "text": {
                            "content": page_values['상태']
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(newPageData)

    res = requests.post(createdUrl, headers=headers, data=data)

    print(res.status_code)

token = "secret_R12tFCcdgBrs7M03RdE0owy59499SODVL1PBwJZz7G1"

databaseId = "e74cb840b6cf4bf7897a48e68d4d05fb"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

readDatabase(databaseId, headers)

page_values = {
    '이름': 'Doom',
    '상태': 'Data Analyst'
}

createPage(databaseId, headers, page_values)

