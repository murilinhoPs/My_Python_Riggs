# coding: utf-8

import maya.cmds as cmds
import maya.mel as mel

def rigSpline():
    selection = cmds.ls(selection= True)

    cmds.duplicate(selection)

    cmds.rename('spine4')
    RIGJointStart1 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    cmds.rename('spine3')
    RIGJoint2 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    cmds.rename('spine2')
    RIGJoint3 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    cmds.rename('spine1')
    RIGJointFinal4 = cmds.ls(selection= True)
    mel.eval("pickWalk -d down;")

    BaseControl = cmds.circle(n= 'spine_base_Control')
    FinalControl = cmds.circle(n= 'spine_final_Control')

    BaseControlNull = cmds.group(em= True, n= 'spine_base_Null')
    FinalControlNull = cmds.group(em= True, n= 'spine_final_Null')

    cmds.parent(BaseControl, BaseControlNull)
    cmds.parent(FinalControl, FinalControlNull)

    cmds.delete(cmds.parentConstraint(RIGJointStart1, BaseControlNull))
    cmds.delete(cmds.parentConstraint(RIGJointFinal4, FinalControlNull))

    cmds.rotate(0, '90deg', 0, 'spine_base_Null')
    cmds.rotate(0, '90deg', 0, 'spine_final_Null')

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True )

    # Spline Ik and curve
    splineHandle = cmds.ikHandle( name= 'spline_ik_handle', solver= 'ikSplineSolver', 
    startJoint= RIGJointStart1[0], ee=  RIGJointFinal4[0], p = 1, w = 1, 
    createCurve= True,parentCurve= True)
    cmds.parent("spline_ik_handle", BaseControl) 


    cmds.select(BaseControl)
    cmds.addAttr(sn = "rl", longName = "Roll", attributeType = 'float', r = True, w = True, h = False, k = True)
    cmds.connectAttr('spine_base_Control.Roll','spline_ik_handle.roll' )

    cmds.select(FinalControl)
    cmds.addAttr(sn = "tw", longName = "Twist", attributeType = 'float', r = True, w = True, h = False, k = True)
    cmds.connectAttr('spine_final_Control.Twist','spline_ik_handle.twist' )

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True )


