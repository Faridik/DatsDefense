import api

def nearest_enemy_manhattan(units):
    """Ближайший враг по Манхеттеновскому расстоянию."""
    head = {}

    # Главный штабик.
    for cell in units["base"]:
        if cell.get("isHead", False):
            head = cell
            break
    
    print("База", head)
    
    zombies = units.get("zombies", []) or []
    nearest_zombie_distance = 100000000
    nearest_zombie = None
    print("Поиск зомбаков")
    for zombie in zombies:
        x_len = abs(zombie["x"] - head["x"])
        y_len = abs(zombie["y"] - head["y"])
        zombie["distance"] = x_len + y_len
        if zombie["distance"] < nearest_zombie_distance:
            nearest_zombie_distance = zombie["distance"]
            nearest_zombie = zombie
    print("Ближайший зомби ", nearest_zombie)

    enemies = units.get("enemyBlocks", []) or []
    nearest_enemy_distance = 100000000
    nearest_enemy = None
    print("Поиск людей")
    for enemy in enemies:
        x_len = abs(enemy["x"] - head["x"])
        y_len = abs(enemy["y"] - head["y"])
        enemy["distance"] = x_len + y_len
        if enemy["distance"] < nearest_enemy_distance:
            nearest_enemy_distance = enemy["distance"]
            nearest_enemy = enemy
    print("Ближайший чел", nearest_enemy)

    if nearest_zombie is None and nearest_enemy is None:
        return None
    
    if nearest_enemy is None and nearest_zombie is not None:
        return nearest_zombie
    
    if nearest_enemy is not None and nearest_zombie is None:
        return nearest_enemy

    if  nearest_zombie["distance"] < nearest_enemy["distance"]:
        return nearest_zombie
    else:
        return nearest_enemy
    

