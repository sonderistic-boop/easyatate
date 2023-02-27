import pygame as pg
import gameMultiplayer.logic.collisions as collisions
#static value, if true then object will move, if false then object will not move

#given two objects, objects, with mass, velocity and restitution, 
#simulate a physics collision between them, and 
#return the new velocities of the objects after the collision
def objectCollision(obj1,obj2,normalVector = None):

    
    print(normalVector)
    if normalVector is None:
        normalVector = ((obj2.position + pg.math.Vector2(obj2.w//2,obj2.h//2)) - (obj1.position + pg.math.Vector2(obj1.w//2,obj1.h//2))).normalize()
    

    
    relativeVelocity = obj2.velocity - obj1.velocity

    normalVelocity = relativeVelocity.dot(normalVector)
    print(normalVelocity)

    
    if(normalVelocity > 0) and ((obj1.staticValue == True) and (obj2.staticValue == True)):
        return
    
    e = min(obj1.restitution,obj2.restitution)

    j = -(1+e) * normalVelocity / (obj1.inverseMass + obj2.inverseMass)

    impulse = normalVector * j

   
    obj1.velocity -= impulse * (obj1.inverseMass) * obj1.staticValue
    obj2.velocity += impulse * (obj2.inverseMass) * obj2.staticValue
    #floating_error(obj1,obj2,normalVector)




#obj1 gets kicked by obj2
def thrust(obj1,obj2):
    e = min(obj1.restitution,obj2.restitution)
    normalVector = ((obj2.position + pg.math.Vector2(obj2.w//2,obj2.h//2)) - (obj1.position + pg.math.Vector2(obj1.w//2,obj1.h//2))).normalize()
    obj1.velocity = normalVector * 6 *-(1+e)







"""
def floating_error(obj1,obj2,normalVector):

    magnitude = normalVector.magnitude()
    penetrationDepth = -(magnitude - obj1.radius - obj2.radius)
    
    slack = 0.6

    allowance = 0.001
  
    correction = max(penetrationDepth - slack, 0 ) / (obj1.inverseMass + obj2.inverseMass) * allowance * normalVector
    obj1.position -= obj1.inverseMass * correction
    obj2.position += obj2.inverseMass * correction





#given an object, and a wall, simulate a physics collision between them, and
#return the new velocity of the object after the collision
def wallCollision(obj,wall):
    if wall == "left":
        if obj.position[0] < 0:
            obj.position[0] = 0
            obj.velocity[0] *= -1
    if wall == "right":
        if obj.position[0] > 1200 - obj.w:
            obj.position[0] = 1200 - obj.w
            obj.velocity[0] *= -1
    if wall == "top":
        if obj.position[1] < 0:
            obj.position[1] = 0
            obj.velocity[1] *= -1
    if wall == "bottom":
        if obj.position[1] > 600 - obj.h:
            obj.position[1] = 600 - obj.h
            obj.velocity[1] *= -1
"""