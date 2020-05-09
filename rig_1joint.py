import maya.cmds as cmds
import maya.mel as mel

#rigg("cano_1")

def riggOne (joint):
    selection = cmds.ls(selection= True)

    cmds.duplicate(selection)

    cmds.rename(joint)
    RigJoint = cmds.ls(selection= True)
    #mel.eval("pickWalk -d down;")

    Controller = cmds.circle(n= joint + "_controler", r=5.0)
    ControllerNull = cmds.group(em= True, n= joint + "_control_NULL")

    cmds.parent(Controller, ControllerNull)
    cmds.delete(cmds.parentConstraint(RigJoint, ControllerNull))
    
    #cmds.rotate("90deg", joint + "_controler", y= True)

    cmds.pointConstraint(Controller, RigJoint, mo= True)

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)