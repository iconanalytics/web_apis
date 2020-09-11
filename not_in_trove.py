

f = open("trove_test4.txt", "r")
done_domains = []

while True:
    a = f.readline()
    if not a:
        break

    done_domains.append(a.split(",")[4])
    

f.close()

print("BOATODA.COM" in done_domains)