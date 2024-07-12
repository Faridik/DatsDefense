
def get_coords_base(units):
    our_base = units.get("base", []) or []
    return list(map(lambda t: [t['x'], t['y']], our_base))

def where_can_build_base_using_our_base(units):
    coords_our_base = get_coords_base(units)
    coords = []
    for x,y in coords_our_base:
        if [x+1, y] not in coords_our_base:
            coords.append([x+1, y])
        if [x-1, y] not in coords_our_base:
            coords.append([x-1, y])
        if [x, y+1] not in coords_our_base:
            coords.append([x, y+1])
        if [x, y-1] not in coords_our_base:
            coords.append([x, y+1])

    return coords

def where_can_build_base(units, world):
    # Размещать новые клетки можно только впритык к одной из 4х
    coords_to_build = where_can_build_base_using_our_base(units)
    
    # Если зомби
    zombies = units.get("zombies", []) or []
    for zombie in zombies:
        for x,y in coords_to_build:
            if x == zombie['x'] and y == zombie['y']:
                coords_to_build.remove([x,y])
                continue

    # Если клетка базы игрока
    anPlayerBases = units.get("enemyBlocks", []) or []
    for anPlayerBase in anPlayerBases:
        for x,y in coords_to_build:
            if x >= anPlayerBase['x'] - 1 and x <= anPlayerBase['x'] + 1 and \
                    y >= anPlayerBase['y'] - 1 and y <= anPlayerBase['y'] + 1:
                coords_to_build.remove([x,y])
                continue
    
    # Блок базы нельзя ставить вплотную к клетке спота зомби
    zposts = world.get("zpots", [])  or []
    for zpost in zposts:
        for x,y in coords_to_build:
            distance = abs(zpost - x) + abs(zpost - y)
            if distance <= 1:
                coords_to_build.remove([x,y])
                continue


    return coords_to_build





def build_bases(coords):
    """
    Строит базы в координатах списка coords
    coords = [[x1,y1], [x2,y2], ...]
    """

    lst = []
    for x,y in coords:
        lst.append(build_base(x,y))
    return {'build' : lst}


def build_base(x,y):
    return {'x': x, 'y': y}



