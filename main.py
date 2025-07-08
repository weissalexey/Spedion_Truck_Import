import requests
import pymssql
import os

LIST_PATCH = 'LIST_PATCH.txt'
SOAP_URL = "https://services.spedion.de/StammdatenWsExtern/2.1/StammdatenWsExtern.asmx"
HEADERS = {
    'charset': 'utf-8',
    'SOAPAction': '"http://ws.spedion.de/VehicleAdd"',
    'Content-Type': 'Text/XML',
    'Host': 'services.spedion.de',
    'Authorization': 'Basic <REPLACE_WITH_BASE64_AUTH>'
}

SQL_QUERY = """
SELECT b.LKW , a.LKWINr,a.Hersteller,a.Modell,a.FahrgNr,a.Handy,a.ModelShort, b.LKw, b.polKz 
FROM XXALKWZU AS a 
LEFT JOIN XXALKW AS b ON a.lKWinr = b.lKWinr 
WHERE CAST(b.ErstDat AS DATE) = CAST(GETDATE() AS DATE)
"""

def is_already_processed(lkw_id):
    if not os.path.exists(LIST_PATCH):
        return False
    with open(LIST_PATCH, 'r') as f:
        return lkw_id in f.read()

def mark_as_processed(lkw_id):
    with open(LIST_PATCH, 'a') as f:
        f.write(f"{lkw_id}\n")

def build_payload(row):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns:xsd="http://www.w3.org/2001/XMLSchema"
 xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <VehicleAdd xmlns="http://ws.spedion.de/">
      <vehicle>
        <Name>{row['LKw']}</Name>
        <NumberPlate>{row['polKz']}</NumberPlate>
        <VehicleState>Active</VehicleState>
        <HasAndroid>true</HasAndroid>
        <TankCapacity>0</TankCapacity>
        <InfoField>{row['ModelShort']}</InfoField>
        <TelephoneNumber>{row['Handy']}</TelephoneNumber>
        <VehicleIdentificationNumber>{row['FahrgNr']}</VehicleIdentificationNumber>
        <BranchLocation>Chr. Carstensen</BranchLocation>
      </vehicle>
    </VehicleAdd>
  </soap12:Body>
</soap12:Envelope>"""

def main():
    conn = pymssql.connect(server="srv-db1", user="gobabygo", password="comeback", database="WinSped")
    cursor = conn.cursor(as_dict=True)
    cursor.execute(SQL_QUERY)

    for row in cursor:
        lkw_id = str(row['LKW'])
        if is_already_processed(lkw_id):
            print(f"{lkw_id} already processed.")
            continue

        payload = build_payload(row)
        response = requests.post(SOAP_URL, headers=HEADERS, data=payload)
        print(f"Sent {lkw_id}, status: {response.status_code}")
        mark_as_processed(lkw_id)

    conn.close()

if __name__ == "__main__":
    main()
