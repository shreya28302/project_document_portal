f = open("sample.txt","r+")
list1 = []
for line in f:
    word = line.split(",")
    list1.append({"Name":word[0],"Age":word[1],"Gender":word[2],"Username":word[3]})
for a in list1:
    a["Name"]=a["Name"].lower()
    for i in range (10):
        a["Username"]=a["Username"].replace(str(i)," ")

f.close()
print(list1)

f = open("sample.txt","r+")
k = 1
user_name = str(input("enter the username you are searching for:"))
for line in f:
    word = line.split(",")
    if word[3] == user_name+"\n":
        print(word[0]+","+word[1]+","+word[2]+","+word[3])
        k = 0
if k == 1:
    name=input("Name: ")
    age=input("Age: ")
    gender=input("Gender: ")
    f.write(name+","+age+","+gender+","+user_name)        
f.close()

list2 = []
f=open("sample.txt","r+")

for line in f:
    word = line.split(",")
    list2.append(word[3])

u_names= set(list2)
b = 0
print("The number of users who have the same name are:")

for p in u_names:
    if list2.count(p)>1:
        ok = p.replace("\n","")
        print(ok+":"+str(list2.count(p)))
        b += 1

if b == 0:
    print("no two have same names")