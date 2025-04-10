from collections import deque

def lastkubrow():

    colors = {
        "MundaneA" : "Ash Grey",
        "MundaneB" : "Earth Brown",
        "MundaneC" : "Corpus Grey",
        "MundaneD" : "Hek Green",
        "MundaneE" : "Kril Brown",
        "MundaneF" : "Gallium Grey",
        "MundaneG" : "Grustrag Grey",
        "MundaneH" : "Saturn Brown",
        "MidA" : "Sedna Grey",
        "MidB" : "Derelict Black",
        "MidC" : "Mars red",
        "MidD" : "Infested Black",
        "MidE" : "Void Black",
        "MidF" : "Darvo Blue",
        "MidG" : "Ordis Grey",
        "MidH" : "Mercury Brown",
        "VibrantA" : "Anyo Grey",
        "VibrantB" : "Ambulas Black",
        "VibrantC" : "Shadow Grey",
        "VibrantD" : "Sargas Brown",
        "VibrantE" : "Jupiter Brown",
        "VibrantF" : "Phorid Red",
        "VibrantG" : "Alad Blue",
        "VibrantH" : "Venus Brown",
        "EyesA" : "Green",
        "EyesB" : "Light Gold",
        "EyesC" : "Pink",
        "EyesD" : "Purple",
        "EyesE" : "Blue",
        "EyesF" : "Orange/Red",
        "EyesG" : "Lilac",
        "EyesH" : "Black",
        "EyesI" : "Gold"
    }

    filename = "C:\\Users\\kat\\AppData\\Local\\Warframe\\EE.log"

    buffer_size = 4
    buffer = deque(maxlen=buffer_size)
    last_match_buffer = None
    consecutive = False

    with open(filename, 'r', encoding="utf-8", errors="replace") as f:
        for line in f:
            if not consecutive:
                buffer.clear()
            if "Sys [Info]: Spot-building /Lotus/Types/Game/KubrowPet" in line:
                consecutive = True
                buffer.append(line.strip())
                if "Sys [Info]: Spot-building /Lotus/Types/Game/KubrowPet/Colors/KubrowPetColorEyes" in line:
                    last_match_buffer = list(buffer)
            else:
                consecutive = False
                
    if last_match_buffer:
        for line in last_match_buffer:
            pos = line.find("KubrowPetColor") + len("KubrowPetColor")
            color_code = line[pos:].strip()
            color_name = colors.get(color_code)
            print(f"{color_code}: {color_name}")