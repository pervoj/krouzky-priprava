# špatný způsob

x = 1

print("Původní hodnota:", x)

if x == 0:
  x = 1

if x == 1:
  x = 0

print("Nová hodnota:", x)



# správný způsob

x = 1

print("Původní hodnota:", x)

if x == 0:
  x = 1
else:
  x = 0

print("Nová hodnota:", x)