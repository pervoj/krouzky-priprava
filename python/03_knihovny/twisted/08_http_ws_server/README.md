# Odmaskování těla zprávy

## Střídání bytů maskovacího klíče

- délka klíče je 4 byty
- pro každý byte těla postupně střídáme byty klíče

```
25551206343864151512454254364
12341234123412341234123412341
```

```python
payload_length = 9
key_length = 4

for payload_index in range(payload_length):
  key_index = payload_index % key_length
  key_index_math_str = f"{payload_index} % {key_length}"
  print(f"{key_index_math_str} = {key_index}")
```

```
0 % 4 = 0
1 % 4 = 1
2 % 4 = 2
3 % 4 = 3
4 % 4 = 0
5 % 4 = 1
6 % 4 = 2
7 % 4 = 3
8 % 4 = 0
```

## Odmaskování bytu zprávy pomocí operace XOR

Mezi bytem těla a bytem klíče se provede operace XOR. Ta porovná každý bit a pokud je každý jiný, nastaví 1, pokud jsou stejné, nastaví 0.

```
6 = 0000000000000110  ← zamaskovaný byte těla
3 = 0000000000000011  ← byte klíče
--------------------
5 = 0000000000000101  ← odmaskovaný byte těla
```

Zpětné zamaskování funguje stejným způsobem:

```
5 = 0000000000000101  ← odmaskovaný byte těla
3 = 0000000000000011  ← byte klíče
--------------------
6 = 0000000000000110  ← zamaskovaný byte těla
```

Operaci XOR lze v Pythonu provést pomocí operátoru `^`:

```python
print(6 ^ 3)  # → 5
print(5 ^ 3)  # → 6
```
