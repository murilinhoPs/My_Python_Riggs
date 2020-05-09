# coding: utf-8

import maya.cmds as cmds
import maya.mel as mel

#rigLeg("joint1", "joint2", "joint3")   moveX = 3  /    moveX = -7 /     moveZ= 2 ou -2

#rigLeg("hip_R_Front_", "knee_R_Front_", "ankle_R_Front_",-7, 2)   
#rigLeg("hip_R_Back_", "knee_R_Back_", "ankle_R_Back_",3, 2) 
#rigLeg("hip_L_Front_", "knee_L_Front_", "ankle_L_Front_",-7, -2)
#rigLeg("hip_L_Back_", "knee_L_Back_", "ankle_L_Back_", 3, -2)

def rigLeg(joint1, joint2, joint3,moveX,moveZ):

    RenameChars = '_' + joint1[4] + '_' + joint1[6]

    # armazena a seleção atual numa variavel
    selection = cmds.ls(selection = True)

    # duplica a selção para duplicar os joints e nao fuder os joint existentes e guarda essa seleçao numa outra variável
    cmds.duplicate(selection)
    SKINJoint1 = selection
    # parenteia essa seleção no mundo, para desparentear dos joints atuais
    #cmds.parent(world = True)
    
    # renomeia essa seleçao e guarda numa variável, e logo depois seleciona o próximo joint na hierarquia
    cmds.rename(joint1) # Cintura (inicial)
    RIGJoint1 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;") #pega o prox joint na hierarquia
    
    cmds.rename(joint2) # Joelho (meio)
    RIGJointMeio2 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    
    cmds.rename(joint3) # Pé (final)
    RIGJointFinal3 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    
        #, peBool
        #if peBool == True:

    cmds.rename('peito_pe' + RenameChars)
    RIGJointPeitoPe = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    
    cmds.rename('ponta_pe' + RenameChars)
    RIGJointPontaPe = cmds.ls(selection = True)
    
    
    #Criar Controles
    FinalControl = cmds.circle(n = joint2 + "_Control") # essa n (name) representa uma String no python Maya
    BaseControl = cmds.circle(n = joint1 + "_Control")
    
    #Criar Nulos
    FinalControlNull = cmds.group(empty = True,n = joint2 + "_POS_freeze" )
    BaseControlNull = cmds.group(empty = True,n = joint1 + "_POS_freeze" )
    
    #Parentear controles nos nulos
    cmds.parent(FinalControl,FinalControlNull)
    cmds.parent(BaseControl, BaseControlNull)


    #Mover nulos para anklel(pé) e hip joints
    cmds.delete(cmds.parentConstraint(RIGJointFinal3,FinalControlNull))
    cmds.delete(cmds.parentConstraint(RIGJoint1, BaseControlNull))

    #Depois de girados, colocar o constraint do controle no joint
    cmds.parentConstraint(BaseControl,RIGJoint1)
    cmds.orientConstraint(FinalControl,RIGJointFinal3)


    #Depois de criados, girar os nulls antes de criar uma hierarquia entre eles
    cmds.rotate('90deg',0, 0, joint2 + "_Control")
    
    #E por fim de tudo isso, freeze transformations para zerar tudo
    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True) #Duvids
    cmds.parent(FinalControlNull, BaseControlNull)
    

    # Criar o IK
    #sj= startJoint    ee= endEffector(Um end effector ou um joint que tera um effector)  p=priotiry  w= weight do Ik
    principalIk = cmds.ikHandle(sj = RIGJoint1[0], ee = RIGJointFinal3[0], solver = "ikRPsolver", p = 1, w = 1, n = "ik_Principal_RPS" + RenameChars)
    cmds.parent("ik_Principal_RPS" + RenameChars, FinalControl)  #Parentear o IK_RPS noFinalControl (do pé ou mão)

    # Criar o controle do poleVector(joelho/cotovelo) e dar constraint no IK
    PoleControl = cmds.nurbsSquare(n = 'poleVector_Control' + RenameChars)
    PoleControlNull = cmds.group(empty = True,n = "pole_POS" + RenameChars)
    
    cmds.parent(PoleControl, PoleControlNull)
    cmds.rotate('90deg',0, 0, "pole_POS" + RenameChars)

    cmds.delete(cmds.parentConstraint(RIGJointMeio2, PoleControlNull))

    cmds.move(moveX,3,moveZ, 'poleVector_Control' + RenameChars)
    cmds.poleVectorConstraint('poleVector_Control' + RenameChars, 'ik_Principal_RPS' + RenameChars)

    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)
    
    

    #Criar atributo Twist no controle, e setar no comando twist do IK rps (como se fosse setDrivenKey)
    cmds.select(BaseControl)  
    cmds.addAttr(sn = "tw", longName = "Twist", attributeType = 'float', r = True, w = True, h = False, k = True) # sn= shortName  h= hidden (hidden in UI)   r= readable(ler conexões com o atributo)   w= writable(fazer conexões com o atributo)   k= keyable(create keys in animations)
    cmds.connectAttr(joint1 + "_Control.Twist", "ik_Principal_RPS" + RenameChars +'.twist')

    cmds.select(FinalControl) #RIGJointPeitoPe
    cmds.addAttr(sn= 'd_m', ln= 'Dobra_Meio', at= 'float', r=True, w=True,h=False,k=True) #min value= min e max value= max
    cmds.connectAttr(joint2 + "_Control.Dobra_Meio",'peito_pe'+ RenameChars + '.rotateY') # ARRUMAR OS NOMEEEEES
    
    cmds.select(FinalControl) #RIGJointPeitoPe
    cmds.addAttr(sn= 'g_m', ln= 'Gira_Meio', at= 'float', r=True, w=True,h=False,k=True) #min value= min e max value= max
    cmds.connectAttr(joint2 + "_Control.Gira_Meio",'peito_pe'+ RenameChars +'.rotateZ')

    cmds.select(FinalControl) #RIGJointPeitoPe
    cmds.addAttr(sn= 'd_p', ln= 'Dobra_Ponta', at= 'float', r=True, w=True,h=False,k=True)
    cmds.connectAttr(joint2 + "_Control.Dobra_Ponta",'ponta_pe'+ RenameChars +'.rotateY')
    
    #Criar os Parents Constraints para mover os joints skinados 
    cmds.select(SKINJoint1)
    mel.eval("pickWalk -d down;")
    SKINJoint2 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")
    SKINJoint3 = cmds.ls(selection = True)
    
    cmds.parentConstraint(RIGJoint1, SKINJoint1, mo = True)
    cmds.parentConstraint(RIGJointMeio2, SKINJoint2, mo = True)
    cmds.parentConstraint(RIGJointFinal3, SKINJoint3, mo = True)  

    
# TIPS

'''
Twist
Not available for single chain IK handles.

Twists the joint chain from the end joint by the specified amount.

You can also control the rotation of the joint chain by manipulating the twist disc.
'''