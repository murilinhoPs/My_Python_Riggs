import maya.cmds as cmds
import maya.mel as mel

#pistao("pist1_Right", "pist2_Right", "pist3_Right", "pist4_Right")

def pistao (joint1, joint2, joint3, joint4):
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
    mel.eval("pickWalk -d down;")

    cmds.rename(joint4)
    RigJoint4 = cmds.ls(selection= True)

    Controller = cmds.circle(n= "pist_controler", r=5.0)
    ControllerNull = cmds.group(em= True, n= "pist_control_NULL")

    cmds.parent(Controller, ControllerNull)

    cmds.delete(cmds.parentConstraint(RigJoint2, ControllerNull))

    cmds.rotate("90deg", 0, 0, "pist_control_NULL")

    cmds.pointConstraint(Controller, RigJoint2, mo= True)

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True) #Duvids

    #create attributes 
    cmds.select(Controller)
    cmds.addAttr(sn= "upDown", ln= "Move_Up_Down", at= "float", min= 18, max= 40, r = True, w = True, h = False, k = True)
    cmds.connectAttr("pist_controler.Move_Up_Down", joint3 + ".translateX")