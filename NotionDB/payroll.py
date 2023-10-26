import requests, json
import pandas as pd

def readDatabase(databaseId, headers):
    
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers=headers)

    data = res.json()
    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
    
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    col7 = []

    columns = ['이름', '시작일', '종료일', '인사구분', '본부', '파트', '연봉']

    if res.status_code == 200:
        for result in data['results']:
            try:
                properties = result['properties']
                col1.append(properties['이름']['title'][0]['text']['content'])
                col2.append(properties['시작일']['date']['start'])
                col3.append(properties['종료일']['date']['start'])
                col4.append(properties['인사구분']['select']['name'])
                col5.append(properties['본부']['select']['name'])
                col6.append(properties['파트']['select']['name'])
                col7.append(properties['연봉']['number'])

            except:
                continue
    else:
        print(res.status_code)

    df = pd.DataFrame(zip(col1, col2, col3, col4, col5, col6, col7), columns=columns)
    print(df)
    print(df[df["종료일"]=='2050-12-31'])

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

# Notion API Token
# Notion 에서 Token 업데이트
token = "xxx"

# Payroll DB
databaseId = "69188ca8282643e691d598d39364dfd1"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}

readDatabase(databaseId, headers)

# page_values = {
#     '이름': 'Doom',
#     '상태': 'Data Analyst'
# }

# createPage(databaseId, headers, page_values)

