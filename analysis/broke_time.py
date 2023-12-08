broken = {21: 86,
          22: 89,
          34: 106,
          41: 82,
          42: 78,
          44: 118,
          51: 98,
          54: 105,
          62: 97,
          71: 86,
          81: 109,
          82: 87,
          83: 112
          }

broken_systems = {21: 2570,
                  22: 2660,
                  34: 3170,
                  41: 2450,
                  42: 2330,
                  44: 3530,
                  51: 2930,
                  54: 3140,
                  62: 2900,
                  71: 2570,
                  81: 3260,
                  82: 2600,
                  83: 3350}

if __name__ == '__main__':
    broken_systems = {}

    for key in broken:
        x = 1020
        for i in range(broken[key] + 1):
            if i == broken[key]:
                broken_systems[key] = x - 1030
            x += 30

    print("{")
    for i in broken_systems:
        print(f"{i}:{broken_systems[i]},")
    print("}")

