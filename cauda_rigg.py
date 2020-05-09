# coding: utf-8


import maya.cmds as cmds
import maya.mel as mel


def rigRabo():
    selection = cmds.ls(selection = True)

    cmds.duplicate(selection)
    SkinRabo1Joint = selection
    #cmds.parent(world = True)
    cmds.rename('rabo1_')
    Rabo1Joint = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    cmds.rename('rabo2_')
    Rabo2Joint = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;") #ultima selecao, ele pega a selecao anterior e pega o de baixo (pickWalk)
    cmds.rename('rabo3_')
    Rabo3Joint = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    cmds.rename('rabo4_')
    Rabo4Joint = cmds.ls(selection = True)
    #mel.eval("pickWalk -d down;")
    #cmds.rename('rabo5_')
    Rabo5Joint = cmds.ls(selection = True)

    #criar controles. Um controle pra cada
    Rabo1Control = cmds.circle(n = 'tail_1_Control')
    Rabo2Control = cmds.circle(n = 'tail_2_Control')
    Rabo3Control = cmds.circle(n = 'tail_3_Control')
    Rabo4Control = cmds.circle(n = 'tail_4_Control')
    RaboMControl = cmds.circle(n = 'tail_M_Control')

    #Rabo5Control = cmds.circle(n = 'tail_5_Control')

    #criar Nulls cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0) 
    Rabo1Null = cmds.group(empty = True,n = 'tail_1_Pos')
    Rabo2Null = cmds.group(empty = True,n = 'tail_2_Pos')
    Rabo3Null = cmds.group(empty = True,n = 'tail_3_Pos')
    Rabo4Null = cmds.group(empty = True,n = 'tail_4_Pos') 
    RaboMNull = cmds.group(empty = True,n = 'tail_M_Pos')
    #Rabo5Null = cmds.group(empty = True,n = 'tail_5_Pos')

    #parentear os cotroles nos nulls
    cmds.parent(Rabo1Control,Rabo1Null)
    cmds.parent(Rabo2Control,Rabo2Null)
    cmds.parent(Rabo3Control,Rabo3Null)
    cmds.parent(Rabo4Control,Rabo4Null)
    cmds.parent(RaboMControl,RaboMNull)
    #cmds.parent(Rabo5Control,Rabo5Null)

    #mover nulls para as pos desejadas
    cmds.delete(cmds.parentConstraint(Rabo1Joint, Rabo1Null))
    cmds.delete(cmds.parentConstraint(Rabo2Joint, Rabo2Null))
    cmds.delete(cmds.parentConstraint(Rabo3Joint, Rabo3Null))
    cmds.delete(cmds.parentConstraint(Rabo4Joint, Rabo4Null))
    cmds.delete(cmds.parentConstraint(Rabo4Joint, RaboMNull))

    cmds.rotate(0, '90deg', 0, 'tail_1_Control')
    cmds.rotate(0, '90deg', 0, 'tail_2_Control')
    cmds.rotate(0, '90deg', 0, 'tail_3_Control')
    cmds.rotate(0, '90deg', 0, 'tail_4_Control')
    cmds.rotate(0, '90deg', 0, 'tail_M_Control')

    #cmds.delete(cmds.parentConstraint(Rabo5Joint, Rabo5Null))
    #cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)

    cmds.orientConstraint(Rabo1Control,Rabo1Joint, mo=True)
    cmds.orientConstraint(Rabo2Control,Rabo2Joint, mo=True)
    cmds.orientConstraint(Rabo3Control,Rabo3Joint, mo=True)
    cmds.orientConstraint(Rabo4Control,Rabo4Joint, mo=True)
    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True )
    #cmds.parentConstraint(Rabo5Control,Rabo5Joint, mo= False)

    # Parentear as partes da cauda
    cmds.parent(Rabo2Null, Rabo1Null)
    cmds.parent(Rabo3Null, Rabo2Null)
    cmds.parent(Rabo4Null, Rabo3Null)

    # Master Controller
    cmds.select(RaboMControl) #RIGJointPeitoPe
    #cmds.addAttr(sn= 'g_r', ln= 'Gira_rabo', at= 'float', r=True, w=True,h=False,k=True) #min value= min e max value= max
    cmds.connectAttr("tail_1_Control.rotateY",'tail_M_Control.translateX')
    #cmds.connectAttr("rabo2_.rotateY",'tail_M_Control.translateX')
    #cmds.connectAttr("rabo3_.rotateY",'tail_M_Control.translateX')
    #cmds.connectAttr("rabo4_.rotateY",'tail_M_Control.translateX')

    #parentear os joints
    cmds.select(SkinRabo1Joint)
    mel.eval("pickWalk -d down;")
    skinRabo1 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    skinRabo2 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    skinRabo3 = cmds.ls(selection = True)
    #mel.eval("pickWalk -d down;")
    #skinRabo4 = cmds.ls(selection = True)
    #mel.eval("pickWalk -d down;")
    #skinRabo5 = cmds.ls(selection = True)

    cmds.parentConstraint(Rabo1Joint, SkinRabo1Joint, mo = True)
    cmds.parentConstraint(Rabo2Joint, skinRabo1, mo = True)
    cmds.parentConstraint(Rabo3Joint, skinRabo2, mo = True)
    cmds.parentConstraint(Rabo4Joint, skinRabo3, mo = True)
    #cmds.parentConstraint(Rabo5Joint, skinRabo4, mo = True)

    # parentear a 2 na 1, a 3 na 2 e a 4 na 3 OS NULLS

    
    
    




