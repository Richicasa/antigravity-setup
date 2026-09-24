import os
import time
import subprocess
import requests
import sqlite3
import json

ZOTERO_EXE_DEFAULT = r"C:\Program Files\Zotero\zotero.exe"
ZOTERO_SQLITE_DEFAULT = os.path.expanduser(r"~\Zotero\zotero.sqlite")
ZOTERO_CONNECTOR_URL = "http://127.0.0.1:23119/connector"

def is_zotero_running():
    try:
        r = requests.get(f"{ZOTERO_CONNECTOR_URL}/ping", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def ensure_zotero_running(exe_path=ZOTERO_EXE_DEFAULT, max_wait_sec=15):
    if is_zotero_running():
        return True
    if not os.path.exists(exe_path):
        print(f"[WARN] No se encontró el ejecutable de Zotero en {exe_path}")
        return False
    
    print("[INFO] Iniciando Zotero Desktop en segundo plano...")
    subprocess.Popen([exe_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    start_time = time.time()
    while time.time() - start_time < max_wait_sec:
        time.sleep(2)
        if is_zotero_running():
            print("[OK] Conexión establecida con Zotero Connector API en el puerto 23119.")
            return True
            
    print("[WARN] Se inició Zotero pero el puerto 23119 aún no responde.")
    return False

def inject_items_to_zotero(items, tags=None):
    """
    Inyecta una lista de diccionarios de ítems directamente en Zotero mediante su API Connector local.
    Cada ítem debe seguir el formato esperado por Zotero:
    {
        "itemType": "journalArticle",
        "title": "...",
        "creators": [{"creatorType": "author", "firstName": "...", "lastName": "..."}],
        "publicationTitle": "...",
        "date": "2024",
        "volume": "10",
        "issue": "2",
        "pages": "100-110",
        "DOI": "...",
        "abstractNote": "...",
        "tags": [{"tag": "..."}]
    }
    """
    if not ensure_zotero_running():
        print("[ERROR] Zotero no está disponible. No se pueden inyectar las referencias vía API.")
        return False

    url = f"{ZOTERO_CONNECTOR_URL}/saveItems"
    headers = {"Content-Type": "application/json"}
    
    if tags:
        for it in items:
            it_tags = it.get("tags", [])
            for t in tags:
                if {"tag": t} not in it_tags:
                    it_tags.append({"tag": t})
            it["tags"] = it_tags

    payload = {"items": items}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code in [200, 201]:
            print(f"[OK] {len(items)} referencias inyectadas directamente en Zotero con éxito!")
            return True
        else:
            print(f"[WARN] Zotero respondió con código {r.status_code}: {r.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Error al contactar la API de Zotero: {e}")
        return False

def read_local_zotero_items(db_path=ZOTERO_SQLITE_DEFAULT, limit=100):
    """
    Lee los últimos ítems registrados en la base de datos SQLite local de Zotero.
    """
    if not os.path.exists(db_path):
        print(f"[ERROR] No existe la base de datos de Zotero en {db_path}")
        return []

    conn = sqlite3.connect(f"file:{db_path.replace(os.sep, '/')}?mode=ro&nolock=1", uri=True)
    c = conn.cursor()
    c.execute(f"""
        SELECT items.itemID, items.key, itemDataValues.value, fields.fieldName
        FROM items 
        JOIN itemData ON items.itemID = itemData.itemID 
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID 
        JOIN fields ON itemData.fieldID = fields.fieldID 
        WHERE items.itemTypeID = (SELECT itemTypeID FROM itemTypes WHERE typeName = 'journalArticle')
        ORDER BY items.itemID DESC
        LIMIT {limit * 10}
    """)
    
    items_map = {}
    for itemID, key, val, fieldName in c.fetchall():
        if itemID not in items_map:
            items_map[itemID] = {"itemID": itemID, "key": key, "fields": {}}
        items_map[itemID]["fields"][fieldName] = val
        
    conn.close()
    return list(items_map.values())[:limit]
