import ast

empty_list = [""] * 100

requiredPracticalList = []

RP1 = {"name": "RP1 Stationary Waves on a String",
       "yAxis": "1 / Length (1 / m)",
       "xAxis": "Frequency (Hz)",
       "xEntryTitle": "Length (m)",
       "yEntryTitle": "Frequency (Hz)",
       "originalEquation": "λ = 2L",
       "linearisedEquation": "f = (v/2)(1/L)",
       "mode": 1
       }
RP2 = {"name": "RP2 Interference Effects",
       "yAxis": "Distance from slit to screen (m)",
       "xAxis": "Distance between each fringe (m)",
       "xEntryTitle": "Slit screen distance (m)",
       "yEntryTitle": "Fringe spacing (m)",
       "originalEquation": "w = λD/s",
       "linearisedEquation": "w = (λ/s)D",
       "mode": 0
       }
RP3 = {"name": "RP3 Determination of g",
       "yAxis": "Time (s)",
       "xAxis": "Height x 2 / Time (m/s)",
       "xEntryTitle": "Time (s)",
       "yEntryTitle": "2h/t (m/s)",
       "originalEquation": "s = ut + 1/2(at)²",
       "linearisedEquation": "2h/t = gt + 2u",
       "mode": 0
       }
RP4 = {'name': "RP4 Determination of Young's Modulus",
       'yAxis': 'Change in length (m)',
       'xAxis': 'Force (N)',
       'xEntryTitle': 'ΔL (m)',
       'yEntryTitle': 'Force (N)',
       'originalEquation': 'E = σ / ε',
       'linearisedEquation': 'F = (E x A / L)ΔL',
       'mode': 0
       }
RP5 = {"name": "RP5 Determination of Resistivity of a Wire",
       "yAxis": "Length of wire (m)",
       "xAxis": "Resistance (Ω)",
       "xEntryTitle": "Length (m)",
       "yEntryTitle": "Resistance (Ω)",
       "originalEquation": "ρ = RA/L",
       "linearisedEquation": "R = (ρ/A)L",
       "mode": 0
       }
RP6 = {"name": "RP6 Internal resistance and emf",
       "yAxis": "Current (A)",
       "xAxis": "Voltage (V)",
       "xEntryTitle": "Current (A)",
       "yEntryTitle": "Voltage (V)",
       "originalEquation": "E = I(R + r)",
       "linearisedEquation": "V = (-r)I + E",
       "mode": 0
       }
RP7 = {"name": "RP7 Simple Harmonic Motion",
       "yAxis": "",
       "xAxis": "",
       "xEntryTitle": "",
       "yEntryTitle": "",
       "originalEquation": "",
       "linearisedEquation": "",
       "mode": 0
       }
RP8 = {"name": "RP8 Boyle's Law",
       "yAxis": "",
       "xAxis": "",
       "xEntryTitle": "",
       "yEntryTitle": "",
       "originalEquation": "",
       "linearisedEquation": "",
       "mode": 0
       }
RP9 = {"name": "RP9 Charging and Discharging Capacitors",
       "yAxis": "Time (s)",
       "xAxis": "ln(V)",
       "xEntryTitle": "Time (s)",
       "yEntryTitle": "Voltage (V)",
       "originalEquation": "V = V₀e^(-t/RC)",
       "linearisedEquation": "ln(V) = (-1/RC)t + ln(V₀)",
       "mode": 2
       }
RP10 = {"name": "RP10 Magnetic Force on a Wire",
       "yAxis": "Current (A)",
       "xAxis": "Mass (kg)",
       "xEntryTitle": "Current (A)",
       "yEntryTitle": "Mass (kg)",
       "originalEquation": "F = nBIL",
       "linearisedEquation": "m = (nBL/g)I",
       "mode": 0
       }
RP11 = {"name": "RP11 Magnetic Flux Linkage",
       "yAxis": "cos(θ)",
       "xAxis": "ε₀ (V)",
       "xEntryTitle": "Angle (θ)",
       "yEntryTitle": "Peak emf (V)",
       "originalEquation": "ε = -B₀ANωsin(ωt)cos(θ)",
       "linearisedEquation": "ε₀ = B₀ANωcos(θ)",
       "mode": 3
       }
RP12 = {"name": "RP12 Inverse Square Law",
       "yAxis": "",
       "xAxis": "",
       "xEntryTitle": "",
       "yEntryTitle": "",
       "originalEquation": "",
       "linearisedEquation": "",
       "mode": 1
       }

requiredPracticalList.append(RP1)
requiredPracticalList.append(RP2)
requiredPracticalList.append(RP3)
requiredPracticalList.append(RP4)
requiredPracticalList.append(RP5)
requiredPracticalList.append(RP6)
requiredPracticalList.append(RP7)
requiredPracticalList.append(RP8)
requiredPracticalList.append(RP9)
requiredPracticalList.append(RP10)
requiredPracticalList.append(RP11)
requiredPracticalList.append(RP12)

####################################
#database=open("RP info.txt", "w", encoding="utf-8")
#
#def makeHash(key):
#    #hash function
#
#    hash_val = 0
#    
#    for letter in key:
#        hash_val += ord(letter)
#    hash_val = hash_val % 97
#    
#    return key
#    
#for i in requiredPracticalList:
#    key = makeHash(i["name"])
#    empty_list[key] = str(i)
#
#for i in empty_list:
#    database.write(str(i) + "\n")
#
#database.close()
#####################################

database=open("RP info.txt", "r", encoding="utf-8")
RP_dicts = database.readlines()

def hashGet(key):
    
    #hash function
    
    hash_val = 0
    
    for letter in key:
        hash_val += ord(letter)
    hash_val = hash_val % 97
    
    while ast.literal_eval(RP_dicts[hash_val][:-1])["name"] != key:
        hash_val += 1
        
    return ast.literal_eval(RP_dicts[hash_val][:-1])

print(hashGet("RP11 Magnetic Flux Linkage"))
    