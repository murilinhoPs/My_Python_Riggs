import maya.cmds as cmds
import maya.mel as mel

#rigArm("arm_R_", "elbow_R_", "wrist_R_",-7, 2)   


def rigArm(joint1, joint2, joint3,moveZ):
    RenameChars = '_' + joint1[4]

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
    ArmController = cmds.circle(n = joint1 + "_Controller")
    WristController = cmds.circle(n = joint3 + "_Controller")

    #Criar Nulos
    ArmControllerNull = cmds.group(em= True, n= joint1 + "Pos_Null" )
    WristControllerNull = cmds.group(em= True, n= joint3 + "Pos_Null" )

    #Parentear controles nos nulos
    cmds.parent(ArmController, ArmControllerNull)
    cmds.parent(WristController, WristControllerNull)

    #Posionar os nulos no lugar certo   
    cmds.delete(cmds.parentConstraint(RIGJoint1, ArmControllerNull))
    cmds.delete(cmds.parentConstraint(RIGJoint2, WristControllerNull))

    #Girar o controle do pulso/wrist
    cmds.rotate("90deg", 0, 0, joint3 + "Pos_Null")

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
    PoleController = cmds.nurbsSquare(n = "pole_Controller" + RenameChars)
    PoleControllerNull = cmds.group(empty = True, n = "pole_Null" + RenameChars) 

    #Criar uma Hieraquia entre os controles do poleVector
    cmds.parent(PoleController, PoleControllerNull)

    #Girar o pole controller para ficar reto
    cmds.rotate("90deg",0, 0, "pole_Null" + RenameChars)

    #Reposicionar o nulo do Pole Vector no lugar certo 
    cmds.delete(cmds.parentConstraint(RIGJoint2, PoleControllerNull))

    #Mover o Pole Controller um pouco para trás
    #cmds.move("pole_Controller" + RenameChars + ".translateX","pole_Controller" + RenameChars + ".translateY",moveZ, 'poleVector_Control' + RenameChars)

    #Adicionar o pole vector constraint no Ik Rps
    cmds.poleVectorConstraint(PoleController, "ik_RPS" + RenameChars)

    #Freeze Transformations
    cmds.makeIdentity(apply=True, rotate=True, translate=True, scale=True)