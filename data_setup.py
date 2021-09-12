import encryptionSystem as Es


def fileCreation():
    adminFile = open("data\\admin", "w")
    admin1 = Es.encrypt_message("Name:admin")
    admin2 = Es.encrypt_message("Nickname:admin")
    admin3 = Es.encrypt_message("Password:admin")
    admin4 = Es.encrypt_message("Gender:noun")
    admin5 = Es.encrypt_message("Age:100")
    admin6 = Es.encrypt_message("Birthday:2000/01/01")
    adminFile.write("{}\n{}\n{}\n{}\n{}\n{}".format(admin1, admin2, admin3, admin4, admin5, admin6))
    adminFile.close()

    loginAttempts = open("data\\logins", "w")
    loginAttempts.close()

    accounts = open("data\\accounts", "w")
    text = Es.encrypt_message("False")
    accounts.write(text)
    accounts.close()

    dataSet = open("data\\dataSetUp", "w")
    dataTrue = Es.encrypt_message("True")
    dataSet.write("{}".format(dataTrue))
    dataSet.close()
