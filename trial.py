print(" ##### Api test  ####")

import apis

# responce = GetUserToken("254715232942", "12341234")
# print(responce)
# print(responce.json()["body"]["token"])
# print(responce.text)

for x in range(0, 10):
    responce = apis.GetUserData("254715232942", "12341234")
    print(responce.text)
    if responce.status_code == 200:
        print("########### fine #########")   

    else:
        print("##### finally #########")
        print(responce.status_code)
        # break