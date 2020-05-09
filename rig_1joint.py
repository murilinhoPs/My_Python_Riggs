import maya.cmds as cmds
import maya.mel as mel

#rigg("cano_1")

def rigg (joint):
    selection = cmds.ls(selection= True)

    cmds.duplicate(selection)

    cmds.rename(joint)
    RigJoint = cmds.ls(selection= True)

    Controller = cmds.circle(n= joint + "_controler", r=2.0)
    ControllerNull = cmds.group(em= True, n= joint + "_control_NULL")

    cmds.parent(Controller, ControllerNull)
    cmds.delete(cmds.parentConstraint(RigJoint, ControllerNull))

    cmds.pointConstraint(Controller, RigJoint, mo= True)

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)