import asyncio
import json
import random
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError

def show_api_instructions():
    """
    Menampilkan panduan untuk mendapatkan api_id dan api_hash
    """
    print("\n=== Cara Dapatkan API ID dan API Hash ===")
    print("1. Buka https://my.telegram.org di browser.")
    print("2. Login dengan nomor telepon Telegram.")
    print("3. Pilih 'API development tools'.")
    print("4. Isi formulir aplikasi:")
    print("   - App title: Misal 'MyPromoBot'.")
    print("   - Short name: Misal 'PromoBot'.")
    print("   - Platform: Pilih 'Other' atau 'Android'.")
    print("   - Description: Misal 'Bot promosi'.")
    print("5. Klik 'Create application'.")
    print("6. Salin 'App api_id' (angka) dan 'App api_hash' (string).")
    print("====================================\n")

async def login_account(session_name, api_id, api_hash, phone):
    """
    Login ke akun Telegram dan buat file sesi
    """
    client = TelegramClient(session_name, api_id, api_hash)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input(f"Masukkan kode verifikasi untuk {phone}: ")
            try:
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = input(f"Masukkan kata sandi 2FA untuk {phone}: ")
                await client.sign_in(password=password)
        print(f"Berhasil login untuk {phone}")
        return client
    except PhoneCodeInvalidError:
        print(f"Kode verifikasi salah untuk {phone}.")
        return None
    except Exception as e:
        print(f"Error login untuk {phone}: {e}")
        return None
    finally:
        await client.disconnect()

def validate_group_input(group_input):
    """
    Validasi input grup (username atau ID)
    """
    if group_input.startswith('@'):
        return group_input
    elif group_input.startswith('-') and group_input[1:].isdigit():
        return group_input
    else:
        return None

def get_create_input():
    """
    Kumpulkan input untuk mode Create
    """
    config = {"accounts": [], "groups": [], "source_group": "", "message_id": None, "use_fixed_message_id": False, "delay": {}, "loop_interval": 300}
    
    show_api_instructions()
    
    while True:
        try:
            num_accounts = int(input("Jumlah akun Telegram: "))
            if num_accounts > 0:
                break
            print("Jumlah akun harus lebih dari 0.")
        except ValueError:
            print("Masukkan angka.")
    
    for i in range(num_accounts):
        print(f"\nAkun {i+1}:")
        phone = input("Nomor telepon (contoh: +628123456789): ")
        while not phone.startswith('+') or not phone[1:].isdigit():
            print("Nomor harus diawali '+' dan hanya angka.")
            phone = input("Nomor telepon: ")
        
        api_id = input("API ID (angka): ")
        while not api_id.isdigit():
            print("API ID harus angka.")
            api_id = input("API ID: ")
        
        api_hash = input("API Hash (string panjang): ")
        while len(api_hash) < 32:
            print("API Hash biasanya 32 karakter.")
            api_hash = input("API Hash: ")
        
        session_name = f"session_{phone.replace('+', '')}"
        config["accounts"].append({
            "api_id": api_id,
            "api_hash": api_hash,
            "phone": phone,
            "session": session_name
        })
    
    config["source_group"] = input("ID atau username grup sumber (contoh: -100987654321 atau @NamaGrup): ")
    while not validate_group_input(config["source_group"]):
        print("Masukkan ID grup (diawali '-') atau username (diawali '@').")
        config["source_group"] = input("ID atau username grup sumber: ")
    
    message_id = input("ID pesan (kosongkan untuk pesan terbaru): ")
    config["message_id"] = int(message_id) if message_id.strip() and message_id.isdigit() else None
    
    use_fixed = input("Gunakan pesan dengan ID tertentu untuk setiap loop? (y/n): ").lower() == 'y'
    config["use_fixed_message_id"] = use_fixed
    
    while True:
        try:
            num_groups = int(input("Jumlah grup tujuan: "))
            if num_groups > 0:
                break
            print("Jumlah grup harus lebih dari 0.")
        except ValueError:
            print("Masukkan angka.")
    
    for i in range(num_groups):
        group_id = input(f"ID atau username grup tujuan {i+1} (contoh: -100123456789 atau @NamaGrup): ")
        while not validate_group_input(group_id):
            print("Masukkan ID grup (diawali '-') atau username (diawali '@').")
            group_id = input(f"ID atau username grup tujuan {i+1}: ")
        config["groups"].append(group_id)
    
    while True:
        try:
            min_delay = float(input("Delay minimum per forwarding (detik, contoh: 60): "))
            if min_delay >= 0:
                break
            print("Delay minimum harus 0 atau lebih.")
        except ValueError:
            print("Masukkan angka.")
    
    while True:
        try:
            max_delay = float(input("Delay maksimum per forwarding (detik, contoh: 120): "))
            if max_delay >= min_delay:
                break
            print("Delay maksimum harus >= delay minimum.")
        except ValueError:
            print("Masukkan angka.")
    
    while True:
        try:
            loop_interval = float(input("Interval cek pesan baru (detik, contoh: 300 untuk 5 menit): "))
            if loop_interval >= 60:
                break
            print("Interval harus minimal 60 detik.")
        except ValueError:
            print("Masukkan angka.")
    
    config["delay"] = {"min_delay": min_delay, "max_delay": max_delay}
    config["loop_interval"] = loop_interval
    
    return config

def load_config():
    """
    Baca konfigurasi dari configuration.json
    """
    try:
        with open('configuration.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: configuration.json tidak ditemukan. Jalankan mode Create terlebih dahulu.")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Format JSON salah di configuration.json.")
        exit(1)

def save_config(config):
    """
    Simpan konfigurasi ke configuration.json
    """
    try:
        with open('configuration.json', 'w') as file:
            json.dump(config, file, indent=2)
        print("Konfigurasi disimpan ke configuration.json")
    except Exception as e:
        print(f"Error menyimpan configuration.json: {e}")

async def check_group_access(client, group_input):
    """
    Periksa apakah akun memiliki akses ke grup
    """
    try:
        entity = await client.get_entity(group_input)
        return True
    except Exception as e:
        print(f"Gagal mengakses grup {group_input}: {e}")
        return False

async def get_message_to_forward(client, source_group, message_id, use_fixed_message_id, last_message_id):
    """
    Ambil pesan untuk di-forward (fixed message_id atau pesan baru)
    """
    try:
        entity = await client.get_entity(source_group)
        if use_fixed_message_id and message_id:
            messages = await client.get_messages(entity, ids=[message_id])
            if messages and messages[0]:
                return messages[0], message_id
            else:
                print(f"Tidak ada pesan dengan ID {message_id} di grup sumber.")
                return None, last_message_id
        else:
            messages = await client.get_messages(entity, limit=1)
            if messages and messages[0].id > last_message_id:
                return messages[0], messages[0].id
            else:
                print("Tidak ada pesan baru di grup sumber.")
                return None, last_message_id
    except Exception as e:
        print(f"Error mengakses grup sumber {source_group}: {e}")
        return None, last_message_id

async def forward_message(client, account, group_id, message, min_delay, max_delay):
    """
    Forward pesan ke grup tujuan
    """
    try:
        async with client:
            me = await client.get_me()
            print(f"Logged in sebagai {me.first_name}")
            await client.forward_messages(group_id, message)
            print(f"Pesan diteruskan dari {me.first_name} ke grup {group_id}")
            delay = random.uniform(min_delay, max_delay)
            print(f"Menunggu {delay:.2f} detik...")
            await asyncio.sleep(delay)
    except Exception as e:
        print(f"Error dengan {account['phone']} untuk grup {group_id}: {e}")

async def main():
    # Menu utama
    print("\n=== Telegram Auto Forward ===")
    print("1. Create (Buat sesi dan configuration.json)")
    print("2. Run (Jalankan auto forward dengan loop)")
    mode = input("Pilih mode (1 atau 2): ")
    
    if mode == "1":
        # Mode Create
        config = get_create_input()
        
        # Login ke setiap akun
        for account in config["accounts"]:
            client = await login_account(
                account["session"],
                account["api_id"],
                account["api_hash"],
                account["phone"]
            )
            if not client:
                print(f"Gagal login untuk {account['phone']}. Melewati akun ini.")
                config["accounts"].remove(account)
        
        # Simpan konfigurasi
        if config["accounts"]:
            save_config(config)
        else:
            print("Tidak ada akun yang berhasil login. Keluar.")
            return
    
    elif mode == "2":
        # Mode Run (dengan loop)
        config = load_config()
        
        # Tampilkan konfigurasi untuk verifikasi
        print("\n=== Isi configuration.json ===")
        print(json.dumps(config, indent=2))
        print("====================================\n")
        
        # Inisialisasi last_message_id
        last_message_id = 0
        
        while True:
            try:
                tasks = []
                for account in config["accounts"]:
                    client = TelegramClient(
                        account["session"],
                        account["api_id"],
                        account["api_hash"]
                    )
                    async with client:
                        # Periksa akses ke grup sumber
                        if not await check_group_access(client, config["source_group"]):
                            print(f"Akun {account['phone']} tidak memiliki akses ke grup sumber {config['source_group']}.")
                            print("Pastikan akun sudah bergabung. Jalankan mode Create ulang jika perlu.")
                            return
                        
                        # Periksa akses ke grup tujuan
                        for group_id in config["groups"]:
                            if not await check_group_access(client, group_id):
                                print(f"Akun {account['phone']} tidak memiliki akses ke grup tujuan {group_id}. Melewati grup ini.")
                                config["groups"].remove(group_id)
                        
                        # Ambil pesan untuk di-forward
                        message, new_message_id = await get_message_to_forward(
                            client, 
                            config["source_group"], 
                            config["message_id"], 
                            config.get("use_fixed_message_id", False), 
                            last_message_id
                        )
                        if message:
                            last_message_id = new_message_id
                            for group_id in config["groups"]:
                                tasks.append(forward_message(
                                    client, account, group_id, message,
                                    config["delay"]["min_delay"], config["delay"]["max_delay"]
                                ))
                
                if tasks:
                    await asyncio.gather(*tasks)
                else:
                    print("Menunggu pesan baru...")
                
                # Tunggu interval berikutnya
                await asyncio.sleep(config.get("loop_interval", 300))
            
            except KeyboardInterrupt:
                print("\nProgram dihentikan oleh pengguna.")
                break
            except Exception as e:
                print(f"Error di loop: {e}. Mencoba lagi setelah interval...")
                await asyncio.sleep(config.get("loop_interval", 300))
    
    else:
        print("Pilihan tidak valid. Gunakan 1 atau 2.")
        return

if __name__ == "__main__":
    asyncio.run(main())
