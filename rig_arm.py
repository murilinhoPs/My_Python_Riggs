import maya.cmds as cmds
import maya.mel as mel

#rigArm("Arm_R_", "Elbow_R_", "Wrist_R_",-15)
#rigArm("Arm_L_", "Elbow_L_", "Wrist_L_",-15)  


def rigArm(joint1, joint2, joint3,moveZ):
    RenameChars = '_' + joint1[4] + joint1[0] + joint1[1] + joint1[2]

    selection = cmds.ls(selection = True)

    cmds.duplicate(selection)

    cmds.rename(joint1) # Ombro/Arm
    RIGJoint1 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")

    cmds.rename(joint2) # Cotovelo/Elbow
    RIGJoint2 = cmds.ls(selection = True)
    mel.eval("pickWalk -d down;")

    cmds.rename(joint3) # Pulso/Wrist
    RIGJoint3 = cmds.ls(selection = True)

    #Criar Controles
    ArmController = cmds.circle(n = joint1 + "_Controller", r=7.0)
    WristController = cmds.circle(n = joint3 + "_Controller", r=7.0)

    #Criar Nulos
    ArmControllerNull = cmds.group(em= True, n= joint1 + "Pos_Null" )
    WristControllerNull = cmds.group(em= True, n= joint3 + "Pos_Null" )

    #Parentear controles nos nulos
    cmds.parent(ArmController, ArmControllerNull)
    cmds.parent(WristController, WristControllerNull)

    #Posionar os nulos no lugar certo   
    cmds.delete(cmds.parentConstraint(RIGJoint1, ArmControllerNull))
    cmds.delete(cmds.parentConstraint(RIGJoint3, WristControllerNull))

    #Deixar os controles do seu jeito (rotacao, scale, posicao....)
    cmds.rotate("90deg", 0, 0, joint3 + "Pos_Null") #pulso
    
    cmds.rotate(0, "90deg", 0, joint1 + "Pos_Null") #ombro
    

    #Colocar o constraint no joint
    cmds.parentConstraint(ArmController, RIGJoint1)
    cmds.parentConstraint(WristController, RIGJoint3)

    #Criar uma Hieraquia entre os controles
    cmds.parent(WristControllerNull, ArmControllerNull)
    
    #Freeze Transformations
    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)


    # Criar o IK do Cotovelo
    #sj= startJoint    ee= endEffector(Um end effector ou um joint que tera um effector)  p=priotiry  w= weight do Ik
    principalIk = cmds.ikHandle(sj = RIGJoint1[0], ee = RIGJoint3[0], solver = "ikRPsolver", p = 1, w = 1, n = "ik_RPS" + RenameChars)
    cmds.parent("ik_RPS" + RenameChars, WristController)  #Parentear o IK_RPS no WristControl (do pé ou mão)

    # Criar o controle e o nulo do poleVector(joelho/cotovelo)
    PoleController = cmds.nurbsPlane(n = "pole_Controller" + RenameChars)
    PoleControllerNull = cmds.group(empty = True, n = "pole_Null" + RenameChars) 

    #Criar uma Hieraquia entre os controles do poleVector
    cmds.parent(PoleController, PoleControllerNull)

    #Deixar o pole controller no meu estilo 
    cmds.rotate("90deg",0, 0, "pole_Null" + RenameChars)
    cmds.scale(5, 5, 5, "pole_Null" + RenameChars)

    #Reposicionar o nulo do Pole Vector no lugar certo 
    cmds.delete(cmds.parentConstraint(RIGJoint2, PoleControllerNull))

    #Mover o Pole Controller um pouco para trás
    cmds.move(moveZ,"pole_Null" + RenameChars, z= True)

    #Adicionar o pole vector constraint no Ik Rps
    cmds.poleVectorConstraint(PoleController, "ik_RPS" + RenameChars)

    #Freeze Transformations
    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)



def rodar(degX,degY,degZ):
    #rodar("90deg", "-45deg", "-80deg")
    selection = cmds.ls(selection = True)

    cmds.rotate(degX,degY,degZ, selection)
     #Freeze Transformations
    cmds.makeIdentity(apply=True, rotate=True)

