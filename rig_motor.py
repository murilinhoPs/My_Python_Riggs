import maya.cmds as cmds
import maya.mel as mel

#motor("spine1", "spine2", "spine3", "spine4", "spine5")

def motor (joint1, joint2, joint3, joint4, joint5):
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
    mel.eval("pickWalk -d down;")

    cmds.rename(joint5)
    RigJoint5 = cmds.ls(selection= True)

    #Criar os controles
    ControllerJoint1 = cmds.circle(n= joint1 + "_controller", r= 2.5)
    ControllerJoint3 = cmds.circle(n= joint3 + "_controller", r= 5.0)
    ControllerJoint5 = cmds.circle(n= joint5 + "_controller", r= 2.5)

    ControllerJoint1Null = cmds.group(em= True, n= joint1 + "_controller_NULL")
    ControllerJoint3Null = cmds.group(em= True, n= joint3 + "_controller_NULL")
    ControllerJoint5Null = cmds.group(em= True, n= joint5 + "_controller_NULL")


    cmds.parent(ControllerJoint1, ControllerJoint1Null)
    cmds.parent(ControllerJoint3, ControllerJoint3Null)
    cmds.parent(ControllerJoint5, ControllerJoint5Null)

    cmds.delete(cmds.parentConstraint(RigJoint1, ControllerJoint1Null))
    cmds.delete(cmds.parentConstraint(RigJoint3, ControllerJoint3Null))
    cmds.delete(cmds.parentConstraint(RigJoint5, ControllerJoint5Null))

    cmds.parentConstraint(ControllerJoint1, RigJoint1, mo= True)
    cmds.parentConstraint(ControllerJoint3, RigJoint3, mo= True)
    cmds.parentConstraint(ControllerJoint5, RigJoint5, mo= True)
    

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)

    cmds.select(ControllerJoint3)
    cmds.addAttr(sn= "TopCtrl", ln= "ShowTopController", at= "bool", r = True, w = True, h = False, k = True)
    cmds.addAttr(sn= "BotCtrl", ln= "ShowBottomController", at= "bool", r = True, w = True, h = False, k = True)

    cmds.connectAttr(joint3 + "_controller" + ".ShowTopController", joint5 + "_controller" +".visibility")
    cmds.connectAttr(joint3 + "_controller" + ".ShowBottomController", joint1 + "_controller" + ".visibility")
