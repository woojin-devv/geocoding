import pandas as pd
import requests
import time

# CSV 파일 읽기
df = pd.read_csv("csv_file.csv")

# Google Maps Geocoding API 키 입력
API_KEY = "AIzaSyDTTn9TrBBE-CaokzsBiCUR0KKCxuTb61E"

# 지오코딩 함수
def geocode(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

# 결과 저장용 컬럼 추가
df["위도"] = None
df["경도"] = None

# 주소 기반으로 위도/경도 구하기
for i, row in df.iterrows():
    address = row["주소"]
    lat, lng = geocode(address)
    df.at[i, "위도"] = lat
    df.at[i, "경도"] = lng
    print(f"{i+1}/{len(df)}: {address} → ({lat}, {lng})")
    time.sleep(0.2)  # 쿼터 제한 방지 (초당 5회 이하 권장)

# 결과 저장
df.to_csv("results.csv", index=False)
print("결과 파일: results.csv")
