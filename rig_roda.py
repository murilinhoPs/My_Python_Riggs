import maya.cmds as cmds
import maya.mel as mel

#roda("roda_Left", "engrenagem_P_Left", "engrenagem_M_Left")
#roda("roda_Right", "engrenagem_P_Right", "engrenagem_M_Right")

def roda (joint1, joint2, joint3):
    selection = cmds.ls(selection= True)

    cmds.duplicate(selection)

    cmds.rename(joint1)
    RigJoint1 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    cmds.rename(joint2)
    RigJoint2 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    cmds.rename(joint3)
    RigJoint3 = cmds.ls(selection= True)

    ControllerRoda1 = cmds.circle(n= joint1 + "_controller", r= 5.0)
    ControllerEngrenagem3 = cmds.circle(n= joint1 + "_controller", r= 3.0)

    ControllerRoda1Null = cmds.group(em= True, n= joint1 + "_controller_NULL")
    ControllerEngrenagem3Null = cmds.group(em= True, n= joint3 + "_controller_NULL")


    cmds.parent(ControllerRoda1, ControllerRoda1Null)
    cmds.parent(ControllerEngrenagem3, ControllerEngrenagem3Null)


    cmds.delete(cmds.parentConstraint(RigJoint1, ControllerRoda1Null))
    cmds.delete(cmds.parentConstraint(RigJoint3, ControllerEngrenagem3Null))


    cmds.rotate("90deg", 0, 0, joint1 + "_controller_NULL")


    cmds.parentConstraint(ControllerRoda1, RigJoint1)
    cmds.parentConstraint(ControllerRoda1, RigJoint2)

    cmds.parentConstraint(ControllerEngrenagem3, RigJoint3)


    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)
