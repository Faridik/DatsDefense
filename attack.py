import api
import base

def nearest_enemy(cell, units):

    zombies = units.get("zombies", []) or []
    nearest_zombie_distance = 100000000
    nearest_zombie = None
    print("Поиск зомбаков")
    for zombie in zombies:
        x_len = abs(zombie["x"] - cell["x"])
        y_len = abs(zombie["y"] - cell["y"])
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
        x_len = abs(enemy["x"] - cell["x"])
        y_len = abs(enemy["y"] - cell["y"])
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

def nearest_enemies(units):
    """Ближайший враг по Манхеттеновскому расстоянию."""

    result = []
    for cell in units.get("base") or []:
        enemy = nearest_enemy(cell, units)
        hit = {
            "blockId": cell["id"],
            "target": {
                "x": enemy["x"],
                "y": enemy["y"]
            }
        }
        result.append(hit)
    return result

