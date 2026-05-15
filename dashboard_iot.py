import paho.mqtt.client as paho

#KONFIGURASI BROKER
BROKER = "broker.hivemq.com"
PORT = 1883
CLIENT_ID = "Dashboard_PC_Kel5_01" 
TOPIC_SUBSCRIBE = "smarthome_kel5/#"

#1. FUNGSI CONNECT 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Berhasil terhubung ke Broker HiveMQ!")
        client.subscribe(TOPIC_SUBSCRIBE, qos=1) 
        print(f"Menunggu data di jalur: {TOPIC_SUBSCRIBE}")
    else:
        print(f"Gagal terhubung, kode error: {rc}")

#2. FUNGSI SUBSCRIBE (MENERIMA & MENGOLAH PESAN) 
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = str(msg.payload.decode("utf-8"))
    
    print(f"[{topic}] Data: {payload}")
    
    #LOGIKA NODE 1 (RUANG TAMU)
    if topic == "smarthome_kel5/living_room/temperature":
        suhu = float(payload)
        
        BATAS_BAWAH = 22.0
        BATAS_ATAS = 28.0
        
        if suhu < BATAS_BAWAH:
            print(f"WARNING: Suhu Ruang Tamu terlalu DINGIN ({suhu} C)! (Ideal: {BATAS_BAWAH}-{BATAS_ATAS} C)")
        elif suhu > BATAS_ATAS:
            print(f"WARNING: Suhu Ruang Tamu terlalu PANAS ({suhu} C)! (Ideal: {BATAS_BAWAH}-{BATAS_ATAS} C)")
        else:
            print(f"INFO: Suhu Ruang Tamu IDEAL dan Nyaman ({suhu} C).")
            
    elif topic == "smarthome_kel5/living_room/motion":
        if payload == "DETECTED":
            print("ALERT: Terdeteksi pergerakan di Ruang Tamu!")
            
#LOGIKA KELEMBAPAN (HUMIDITY)
    elif topic == "smarthome_kel5/living_room/humidity":
        kelembapan = float(payload)
        
        HUM_BAWAH = 45.0
        HUM_ATAS = 65.0
        
        if kelembapan < HUM_BAWAH:
            print(f"WARNING: Udara Ruang Tamu terlalu KERING ({kelembapan} %)! (Ideal: {HUM_BAWAH}-{HUM_ATAS} %)")
        elif kelembapan > HUM_ATAS:
            print(f"WARNING: Udara Ruang Tamu terlalu LEMBAP ({kelembapan} %)! (Ideal: {HUM_BAWAH}-{HUM_ATAS} %)")
        else:
            print(f"INFO: Kelembapan Udara Ruang Tamu IDEAL ({kelembapan} %).")
            
    # LOGIKA NODE 2 (DAPUR) 
    elif topic == "smarthome_kel5/kitchen/gas":
        gas_value = int(payload)
        
        if gas_value > 2000:
            print("BAHAYA: Kebocoran Gas di Dapur terdeteksi (Nilai > 2000)!")

    #LOGIKA STATUS LWT (LAST WILL & TESTAMENT)
    elif "status" in topic:
        if payload == "OFFLINE":
             print(f"ALERT KRITIS: {topic} terputus secara tidak wajar (LWT Aktif)!")
        elif payload == "ONLINE":
             print(f"INFO: {topic} berhasil online kembali.")

#3. INISIALISASI & EKSEKUSI 
client = paho.Client(client_id=CLIENT_ID, clean_session=False)

client.on_connect = on_connect
client.on_message = on_message

print("Memulai Dashboard IoT Kelompok 5...")
try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nMenutup Dashboard...")
    client.disconnect()