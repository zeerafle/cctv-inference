import http.client
import os
import dotenv
dotenv.load_dotenv()

conn = http.client.HTTPSConnection("api.samarindakota.go.id")
headers = {
	'Accept': "application/json",
	'Content-Type': "application/json",
	'Authorization': f"Bearer {os.getenv('API_KEY')}",
}

conn.request("GET", "/api/v2/generate/dinas-komunikasi-dan-informatika/cctv", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

