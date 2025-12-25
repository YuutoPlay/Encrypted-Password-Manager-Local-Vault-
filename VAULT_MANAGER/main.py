from vault import load_vault, save_vault
import getpass

def main():
    print("🔐 Encrypted Password Manager (Local Vault)")
    master_password = getpass.getpass("Enter master password: ")

    try:
        vault = load_vault(master_password)
    except Exception:
        print("❌ Wrong password or corrupted vault")
        return

    while True:
        print("\n1. Add password")
        print("2. View passwords")
        print("3. Delete password")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            site = input("Site name: ")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            vault[site] = {"username": username, "password": password}
            save_vault(master_password, vault)
            print("✅ Saved")

        elif choice == "2":
            for site, creds in vault.items():
                print(f"\n🔹 {site}")
                print("Username:", creds["username"])
                print("Password:", creds["password"])

        elif choice == "3":
            site = input("Site to delete: ")
            if site in vault:
                del vault[site]
                save_vault(master_password, vault)
                print("🗑️ Deleted")
            else:
                print("❌ Not found")

        elif choice == "4":
            print("👋 Goodbye")
            break

        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
