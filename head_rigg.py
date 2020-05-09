# coding: utf-8

import maya.cmds as cmds
import maya.mel as mel

def rigHead():
    selection = cmds.ls(selection= True)

    cmds.duplicate(selection)
    #cmds.parent(world = True)

    cmds.rename('pescocoJoint')
    RIGJointNeck1 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    cmds.rename('headJoint')
    RIGJoint2 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    cmds.rename('headFinalJoint')
    RIGJointFinal3 = cmds.ls(selection= True)

    NeckControl = cmds.circle(n= 'neck_Control')
    HeadControl = cmds.circle(n= 'head_Control')

    NeckControlNull = cmds.group(em= True, n= 'neck_Null')
    HeadControlNull = cmds.group(em= True, n= 'head_Null')

    cmds.parent(NeckControl, NeckControlNull)
    cmds.parent(HeadControl, HeadControlNull)

    cmds.delete(cmds.parentConstraint(RIGJointNeck1, NeckControlNull))
    cmds.delete(cmds.parentConstraint(RIGJointFinal3, HeadControlNull))

    cmds.rotate(0, '90deg', 0, 'neck_Null')
    cmds.rotate('90deg', '90deg', 0, 'head_Null')

    cmds.orientConstraint(NeckControl,RIGJointNeck1, mo= True)
    cmds.orientConstraint(HeadControl,RIGJoint2, mo= True)

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True )

    cmds.parent(HeadControlNull, NeckControl)


