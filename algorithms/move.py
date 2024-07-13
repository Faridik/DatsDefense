def check_base(units, move):
    our_base = units.get("base", []) or []
    for cell in our_base:
        if move["x"] == cell["x"] and move["y"] == cell["y"]:
            return True
    return False

PREVIOUS_UPDATE = 0

def move(units, world, head):

    if (PREVIOUS_UPDATE < 5):
        PREVIOUS_UPDATE += 1
        return None
    
    PREVIOUS_UPDATE = 0

    zpots = world.get("zpots", []) or []
    dx = 0
    dy = 0
    for zpot in zpots:
        if zpot["type"] == "default":
            dx_curr = head["x"] - zpot["x"]
            dy_curr = head["y"] - zpot["y"]
            dist = ((dx_curr * dx_curr) + (dy_curr * dy_curr)) ** (1/2)
            dx += dx_curr / dist / dist
            dy += dy_curr / dist / dist


    if abs(dy) - abs(dx) > 0:
        if dy > 0:
            move = {"x": head["x"], "y": head["y"] + 1}
            if check_base(units, move):
                return move
            else:
                if dx > 0:
                    move["x"] += 1
                    if not check_base(units, move):
                        move["y"] += 1
                    return move
                else:
                    move["x"] -= 1
                    return move if check_base(units, move) else None
        else:
            move = {"x": head["x"], "y": head["y"] - 1}
            if check_base(units, move):
                return move
            else:
                if dx > 0:
                    move["x"] += 1
                    return move if check_base(units, move) else None
                else:
                    move["x"] -= 1
                    if not check_base(units, move):
                        move["y"] -= 1
                    return move
    else:
        if dx > 0:
            move = {"x": head["x"] + 1, "y": head["y"]}
            if check_base(units, move):
                return move
            else:
                if dy > 0:
                    move["y"] += 1
                    if not check_base(units, move):
                        move["x"] += 1
                    return move
                else:
                    move["y"] -= 1
                    return move if check_base(units, move) else None
        else:
            move = {"x": head["x"] - 1, "y": head["y"]}
            if check_base(units, move):
                return move
            else:
                if dy > 0:
                    move["y"] += 1
                    return move if check_base(units, move) else None
                else:
                    move["y"] -= 1
                    if not check_base(units, move):
                        move["x"] -= 1
                    return move