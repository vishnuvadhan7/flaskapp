from pymongo import MongoClient

uri = "mongodb+srv://abhinavin07:QHVgOjDsIeVG5x2U@cluster0.avermlt.mongodb.net/?appName=Cluster0"   # paste the correct one
try:
    client = MongoClient(uri)
    print(client.list_database_names())
    print("✅ Connection successful!")
except Exception as e:
    print("❌ Error:", e)