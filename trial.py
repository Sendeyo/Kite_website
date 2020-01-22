print("")
userdata = {'_id': '5e255a376a2a7bf4c1fc0280', 'accountType': 'consumer', 'cooprateCode': '001', 'phoneNo': '254715232942', 'received': 100.0, 'sent': 0.0, 'username': 'Sendeyo', 'wallet': [{'_id': '5e255a377e0f49143400bba0', 'balance': 100.0, 'walletNo': '001015232942'}]}

print(userdata)

userdata["admins"] = ["1234"]

print(userdata)
print(type(userdata))