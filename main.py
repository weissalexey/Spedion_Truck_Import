import requests
import pymssql
import json

with open("//srv-wss/Schnittstellen/_Scripte/py/SPEDION/config.json", "r", encoding="utf-8") as conf:
    CONFIG = json.load(conf)

XML_URL = CONFIG["XML_URL"]
LKW_PATCH = CONFIG["LKW_PATCH"]
USERNAME = CONFIG["USERNAME"]
PASSWORD = CONFIG["PASSWORD"]
AUTHORIZATION = CONFIG["AUTHORIZATION"]
SQL_SERVER = CONFIG["SQL_SERVER"]
SQL_USER = CONFIG["SQL_USER"]
SQL_PASSWORD = CONFIG["SQL_PASSWORD"]
SQL_DATABASE = CONFIG["SQL_DATABASE"]


def TextMAIKER(STRLoader, NNAME):
    with open(f'{NNAME}.txt', 'a') as out:
        out.write(STRLoader + '\n')

headers = {
    'charset': 'utf-8',
    'SOAPAction': '"http://ws.spedion.de/VehicleAdd"',
    'Content-Type': 'text/xml',  # лучше text/xml, без заглавной T!
    'Host': 'services.spedion.de',
    'Authorization': AUTHORIZATION,  # попробуй так!
}

STAT_SQL = """
SELECT istlkw, b.LKW, a.LKWINr, a.Hersteller, a.Modell, a.FahrgNr, a.Handy, a.ModelShort, b.polKz, b.ErstDat, b.AendDat
FROM XXALKWZU AS a
LEFT JOIN XXALKW AS b ON a.lKWinr = b.lKWinr
WHERE CAST(b.ErstDat AS DATE) >= GETDATE() -4
"""
#print(STAT_SQL)
db = pymssql.connect(SQL_SERVER, SQL_USER, SQL_PASSWORD, SQL_DATABASE)
cursor = db.cursor(as_dict=True)
cursor.execute(STAT_SQL)

for row in cursor:
    if row['istlkw'] == 1:
        category_id = "PullingUnit"
        category_name = "LKW"
        subcategory_xml = ""  # не добавляем
    else:
        category_id = "PulledUnit"
        category_name = "Anhänger"
        subcategory_xml = """
        <Subcategory>
            <Id>2</Id>
            <Name>Trailer</Name>
            <CategoryId>2</CategoryId>
            <CustomerId>0</CustomerId>
        </Subcategory>
        """
        
    LKWINr = str(row['LKW'])
    Hersteller = str(row['Hersteller'])
    Modell = str(row['Modell'])
    FahrgNr = str(row['FahrgNr'])
    Handy = str(row['Handy'])
    ModelShort = str(row['ModelShort'])
    #LKw = str(row['LKw'])
    polKz = str(row['polKz'])
    
    with open(LKW_PATCH) as d:
        lkw_list = d.read().splitlines()
    if str(LKWINr) in lkw_list:
        print(LKWINr + ' ist schon Da')
    else:
        print(LKWINr + ' ist nicht Da')
        STRLoader = f"""<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <VehicleAdd xmlns="http://ws.spedion.de/">
      <vehicle>
        <Name>{LKWINr}</Name>
        <NumberPlate>{polKz}</NumberPlate>
        <VehicleState>Active</VehicleState>
        <HasAndroid>true</HasAndroid>
        <Category>
            <CategoryId>{category_id}</CategoryId>
            <Name>{category_name}</Name>
        </Category>
        {subcategory_xml}
        <TankCapacity>0</TankCapacity>
        <InfoField>{ModelShort}</InfoField>
        <TelephoneNumber>{Handy}</TelephoneNumber>
        <VehicleIdentificationNumber>{FahrgNr}</VehicleIdentificationNumber>
        <BranchLocation>Chr. Carstensen</BranchLocation>
      </vehicle>
    </VehicleAdd>
  </soap12:Body>
</soap12:Envelope>
"""
        #NNAME = str(LKWINr)
        #TextMAIKER(STRLoader, NNAME)
        response = requests.post(
            XML_URL,
            headers=headers,
            data=STRLoader
        )
        if response.status_code == 200 and "VehicleAddResult" in response.text:
            with open(LKW_PATCH, 'a') as file_2:
                file_2.write(LKWINr + '\n')
            print(f"{LKWINr} In Datei hinzugefuegt.")
        else:
            print(f"Error {LKWINr}: {response.status_code}")
            print(response.text)
