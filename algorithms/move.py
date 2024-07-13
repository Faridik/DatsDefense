def move(world, head):
    zpots = world.get("zpots", []) or []
    dx = 0
    dy = 0
    for zpot in zpots:
        if zpot["type"] == "default":
            dx_curr = head["x"] - zpot["x"]
            dy_curr = head["y"] - zpot["y"]
            dx += dx_curr
            dy += dy_curr

    return {"x": dx, "y": dy}