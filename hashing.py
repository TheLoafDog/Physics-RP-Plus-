import sys
from rp_data import DATA_FILE, TABLE_SIZE, hashGet, hashKey # Shared lookup, also used by Main.py

requiredPracticalList = []

RP1 = {"name": "RP1 Stationary Waves on a String",
       "yAxis": "Frequency (Hz)",
       "xAxis": "1 / Length (1 / m)",
       "xEntryTitle": "Length (m)",
       "yEntryTitle": "Frequency (Hz)",
       "originalEquation": "λ = 2L",
       "linearisedEquation": "f = (v/2)(1/L)",
       "mode": 1
       }
RP2 = {"name": "RP2 Interference Effects",
       "yAxis": "Distance between each fringe (m)",
       "xAxis": "Distance from slit to screen (m)",
       "xEntryTitle": "Slit screen distance (m)",
       "yEntryTitle": "Fringe spacing (m)",
       "originalEquation": "w = λD/s",
       "linearisedEquation": "w = (λ/s)D",
       "mode": 0
       }
RP3 = {"name": "RP3 Determination of g",
       "yAxis": "Height x 2 / Time (m/s)",
       "xAxis": "Time (s)",
       "xEntryTitle": "Time (s)",
       "yEntryTitle": "2h/t (m/s)",
       "originalEquation": "s = ut + 1/2(at)²",
       "linearisedEquation": "2h/t = gt + 2u",
       "mode": 0
       }
RP4 = {'name': "RP4 Determination of Young's Modulus",
       'yAxis': 'Force (N)',
       'xAxis': 'Change in length (m)',
       'xEntryTitle': 'ΔL (m)',
       'yEntryTitle': 'Force (N)',
       'originalEquation': 'E = σ / ε',
       'linearisedEquation': 'F = (E x A / L)ΔL',
       'mode': 0
       }
RP5 = {"name": "RP5 Determination of Resistivity of a Wire",
       "yAxis": "Resistance (Ω)",
       "xAxis": "Length of wire (m)",
       "xEntryTitle": "Length (m)",
       "yEntryTitle": "Resistance (Ω)",
       "originalEquation": "ρ = RA/L",
       "linearisedEquation": "R = (ρ/A)L",
       "mode": 0
       }
RP6 = {"name": "RP6 Internal resistance and emf",
       "yAxis": "Voltage (V)",
       "xAxis": "Current (A)",
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
       "yAxis": "ln(V)",
       "xAxis": "Time (s)",
       "xEntryTitle": "Time (s)",
       "yEntryTitle": "Voltage (V)",
       "originalEquation": "V = V₀e^(-t/RC)",
       "linearisedEquation": "ln(V) = (-1/RC)t + ln(V₀)",
       "mode": 2
       }
RP10 = {"name": "RP10 Magnetic Force on a Wire",
       "yAxis": "Mass (kg)",
       "xAxis": "Current (A)",
       "xEntryTitle": "Current (A)",
       "yEntryTitle": "Mass (kg)",
       "originalEquation": "F = nBIL",
       "linearisedEquation": "m = (nBL/g)I",
       "mode": 0
       }
RP11 = {"name": "RP11 Magnetic Flux Linkage",
       "yAxis": "ε₀ (V)",
       "xAxis": "cos(θ)",
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

# Generator for `RP info.txt`: run `python3 hashing.py --write` after editing the dicts above.
# Each dict goes in slot hashKey(name) (sum of ord() mod 97), probing forward on a collision, and is
# written one `str(dict)` per line with CRLF line endings (the format rp_data.loadTable reads back).

def buildTable(practicals = requiredPracticalList, size = TABLE_SIZE):
    """Return a `size`-slot list of str(dict) / "" for the given practical dicts."""
    table = [""] * size
    for practical in practicals:
        slot = hashKey(practical["name"])
        while table[slot]:
            slot = (slot + 1) % size
        table[slot] = str(practical)
    return table

def writeTable(path = DATA_FILE):
    with open(path, "w", encoding = "utf-8", newline = "") as database:
        for line in buildTable():
            database.write(line + "\r\n")

if __name__ == "__main__":
    if "--write" in sys.argv: # Regenerate RP info.txt from the dicts above
        writeTable()
        print("Wrote", DATA_FILE)
    else: # Quick data check when run directly
        print(hashGet("RP11 Magnetic Flux Linkage"))
    