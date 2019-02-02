from hashlib import md5

secret = "bgvyzdsv"
hash_out = "xxxxxx"

# part 1
i = 0
while hash_out[:5] != '00000':
    i += 1
    hash_out = md5(str(secret + str(i)).encode()).hexdigest()
print("part 1:\ti: {}, hash: {}".format(i, hash_out))

# part 2
while hash_out[:6] != '000000':
    i += 1
    hash_out = md5(str(secret + str(i)).encode()).hexdigest()
print("part 2:\ti: {}, hash: {}".format(i, hash_out))
