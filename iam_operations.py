from datetime import datetime
import time
import boto3
import json
import datetime
import sys

DAYS = 90 # Numero de dias utilizados para verificar as chaves.
DATE_FORMAT = "%d/%m/%Y" # Formato da data, DD/MM/YYYY
IDENT = 3 # Identacao do json 

iam = boto3.client("iam")
today = datetime.datetime.today()

# Salvar output em um arquivo
def outToFile(path, output):
    try:
        with open(path, "w") as file:
            file.write(output)
    except Exception as e:
        sys.exit(f"Cannot open the file, error: {e}")
        
# Formata a data
def formatDate(date):
    return date.strftime(DATE_FORMAT)

# Lista todos os usuarios
def listUsers():
    usersList = []
    users = iam.list_users()
    for user in users["Users"]:
        usersList.append(user)
    return usersList

# Lista todas as Access Keys pertencentes a um usuario.
def listAccessKey(user):
    keysList = []
    keys = iam.list_access_keys(UserName=user)
    for key in keys["AccessKeyMetadata"]:
        lastUsed = iam.get_access_key_last_used(AccessKeyId=key["AccessKeyId"])
        if lastUsed["AccessKeyLastUsed"]["ServiceName"] == "N/A":
            lastUsed = "N/A"
        else:
            lastUsed = formatDate(lastUsed["AccessKeyLastUsed"]["LastUsedDate"])
        dictKey = {"AccessKeyId": key["AccessKeyId"], "Status": key["Status"], "CreateDate": formatDate(key["CreateDate"]),"LastUsed": lastUsed}
        keysList.append(dictKey)
    return keysList

# Essa funcao obtem a lista de todos os usuarios e suas respectivas Access Keys.
def getUsersKeys():
    client_keys =  {"Date": f"{today}","Users":[]}
    usersList = listUsers()
    for user in usersList:
        keysDict = listAccessKey(user["UserName"])
        try:
            passwordLastUsed = formatDate(user["PasswordLastUsed"])
        except:
            passwordLastUsed = "N/A"
        userDict = {"UserName": user["UserName"],"PasswordLastUsed": passwordLastUsed , "AccessKeys":keysDict}
        client_keys["Users"].append(userDict)
    return client_keys

# Essa funcao valida as Access Keys de todos os usuarios, se elas foram usadas nos ultimos X dias.
def validateKeys():
    userKeys = getUsersKeys()
    client_keys =  {"Date": f"{today}", "Users":[]}
    for user in userKeys["Users"]:
        invalid_keys = []
        #Validate keys
        for key in user["AccessKeys"]:
            try:
                lastUsed = datetime.datetime.strptime(key["LastUsed"], DATE_FORMAT)
            except:
                lastUsed = datetime.datetime.strptime(key["CreateDate"], DATE_FORMAT)
            diff = today - lastUsed
            if (diff.days > DAYS):
                invalid_keys.append(key)
        if (invalid_keys):
            user["AccessKeys"] = invalid_keys
            client_keys["Users"].append(user)
    return client_keys 

def main():
    print("Initializing...")
    # Modo - all ou validateKeys
    try:
        arg = sys.argv[1]
    except:
        arg = "all"

    # Caminho do arquivo
    try:
        path = sys.argv[2]
    except:
        path = ""

    # Verifica o caminho do arquivo.
    if path:
        outToFile(path, "")

    # Retorna todos os clientes e todas as Access Keys, sem validacao
    if arg == "all":
        if not path:
            print(json.dumps(getUsersKeys(), indent=IDENT))
        else:
            outToFile(path,json.dumps(getUsersKeys(), indent=IDENT))
    # Retorna apenas clientes com Access Keys que não estão sendo utilizadas a mais de X dias.
    elif arg =="validateKeys":
        if not path:
            print(json.dumps(validateKeys(), indent=IDENT))
        else:
            outToFile(path,json.dumps(validateKeys(), indent=IDENT))
    else:
        sys.exit("Verifique o argumento passado, argumentos aceitos: all, validateKeys")

# Executa a função main
init = time.time()
main()
end = time.time()
print(f"Execution finished!!! Time: {(end - init):.3f} seconds")