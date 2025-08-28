from lib.LoginManagementLib import LoginManagementLib
if __name__ == "__main__":
    print("=== Clinic Management System ===")
    while True:
        print('1.Login')
        print('2.Exit')
        choice = input("Enter your choice :")
        if choice =='1':
                LoginManagementLib.login()
        elif choice =='2':
             print('Exiting...')
             break
        else:
             print('Invalid choice')             
