import pygame as pg

def quadManifold(obj1,obj2):
    distanceVector = pg.Vector2(obj2.bounds["x1"],obj2.bounds["y1"])-pg.Vector2(obj1.bounds["x1"],obj1.bounds["y1"])

    obj1X_extent = (obj1.bounds["x2"] - obj1.bounds["x1"])/2
    obj1Y_extent = (obj1.bounds["y2"] - obj1.bounds["y1"])/2

    obj2X_extent = (obj2.bounds["x2"] - obj2.bounds["x1"])/2
    obj2Y_extent = (obj2.bounds["y2"] - obj2.bounds["y1"])/2

    x_overlap = obj1X_extent + obj2X_extent - abs(distanceVector[0])
    y_overlap = obj1Y_extent + obj2Y_extent - abs(distanceVector[1])

    if x_overlap > y_overlap:
        if distanceVector[0]  < 0:
            return pg.Vector2(-1,0)
        else:
            return pg.Vector2(0,0)

    else:
        if distanceVector[1] < 0:
            return pg.Vector2(0,-1)
        else:
            return pg.Vector2(0,1)






def circleQuadManifold(obj1,obj2):
    #obj2 is circle in this case
    distanceVector = pg.Vector2(obj2.position[0]+obj2.w,obj2.position[1]+obj2.h)-pg.Vector2(obj1.bounds["x1"],obj1.bounds["y1"])

    

    obj1X_extent = (obj1.bounds["x2"] - obj1.bounds["x1"])/2
    obj1Y_extent = (obj1.bounds["y2"] - obj1.bounds["y1"])/2


    x_overlap = obj1X_extent + obj2.radius - abs(distanceVector[0])
    y_overlap = obj1Y_extent + obj2.radius - abs(distanceVector[1])

  
    if x_overlap > y_overlap:
            if distanceVector[0]  < 0:
                return pg.Vector2(-1,0)
            else:
                return pg.Vector2(1,0)

    else:
        if distanceVector[1] < 0:
            return pg.Vector2(0,-1)
        else:
            return pg.Vector2(0,1)

    
