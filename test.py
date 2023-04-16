import xiangshi as xs
# Simhash
print(type(xs.simhash(["-", "-"])))
# Minhash
print(xs.minhash(["小明爱吃榴莲", "榴莲是小明的最爱"]))

# Simhash
print(xs.simhash(["我曾经失落失望失掉所有方向", "我曾经失落失望失掉所有方向"]))
# Minhash
print(xs.minhash(["我曾经失落失望失掉所有方向", "我曾经失落失望失掉所有方向"]))
