from maya import cmds


def _con(name):
    con = cmds.circle(name=name)[0]
    conShape = cmds.listRelatives(con, s=True)[0]
    cmds.scale(0.5, 0.5, 0.5, '{}.cv[0]'.format(conShape), '{}.cv[2]'.format(conShape), r=True)
    cmds.setAttr("{}.overrideEnabled".format(conShape), 1)
    cmds.setAttr("{}.overrideColor".format(conShape), 17)
    cmds.rotate(0, 90, 0, '{}.cv[0:7]'.format(conShape), r=True, os=True)
    return con


def build():
    ik_node = cmds.createNode('rkt_ikSplineSolver')
    controls = cmds.createNode('transform', name='controls')
    c1_grp = cmds.createNode('transform', name='con1_grp', parent=controls)
    c2_grp = cmds.createNode('transform', name='con2_grp', parent=controls)
    c3_grp = cmds.createNode('transform', name='con3_grp', parent=controls)

    control_1 = _con('base_ctrl')
    cmds.parent(control_1, c1_grp)
    control_2 = _con('mid_ctrl')
    cmds.parent(control_2, c2_grp)
    control_3 = _con('top_ctrl')
    cmds.parent(control_3, c3_grp)

    cmds.setAttr('{}.rz'.format(c1_grp), 90)
    cmds.setAttr('{}.rz'.format(c2_grp), 90)
    cmds.setAttr('{}.rz'.format(c3_grp), 90)
    cmds.setAttr('{}.ty'.format(c2_grp), 4)
    cmds.setAttr('{}.ty'.format(c3_grp), 8)

    cmds.connectAttr('{}.worldMatrix[0]'.format(control_1),
                     '{}.inSplinePoint[0].matrix'.format(ik_node))
    cmds.connectAttr('{}.worldMatrix[0]'.format(control_2),
                     '{}.inSplinePoint[1].matrix'.format(ik_node))
    cmds.connectAttr('{}.worldMatrix[0]'.format(control_3),
                     '{}.inSplinePoint[2].matrix'.format(ik_node))

    cmds.addAttr(control_1, ln='outTangent', at='float', dv=1, keyable=True)
    cmds.addAttr(control_2, ln='inTangent', at='float', dv=1, keyable=True)
    cmds.addAttr(control_2, ln='outTangent', at='float', dv=1, keyable=True)
    cmds.addAttr(control_3, ln='inTangent', at='float', dv=1, keyable=True)

    cmds.connectAttr('{}.outTangent'.format(control_1),
                     '{}.inSplinePoint[0].tangentOut'.format(ik_node))
    cmds.connectAttr('{}.inTangent'.format(control_2),
                     '{}.inSplinePoint[1].tangentIn'.format(ik_node))
    cmds.connectAttr('{}.outTangent'.format(control_2),
                     '{}.inSplinePoint[1].tangentOut'.format(ik_node))
    cmds.connectAttr('{}.inTangent'.format(control_3),
                     '{}.inSplinePoint[2].tangentIn'.format(ik_node))

    samples = 9
    cmds.setAttr('{}.length'.format(ik_node), 10)
    cmds.setAttr('{}.samples'.format(ik_node), samples)
    skel_grp = cmds.createNode('transform', name='skeleton')
    joints = list()
    for x in xrange(samples):
        joint_obj = cmds.createNode('joint', parent=skel_grp)
        cmds.connectAttr('{}.outSRT[{}].outTranslate'.format(ik_node, x),
                         '{}.translate'.format(joint_obj))
        cmds.connectAttr('{}.outSRT[{}].outRotate'.format(ik_node, x),
                         '{}.rotate'.format(joint_obj))
        joints.append(joint_obj)

    cube = cmds.polyCube(sh=samples * 2, h=samples + 2)[0]
    cmds.setAttr("{}.overrideEnabled".format(cube), 1)
    cmds.setAttr("{}.overrideDisplayType".format(cube), 2)
    cmds.setAttr('{}.ty'.format(cube), 5)
    cmds.skinCluster(joints, cube)
    cmds.setAttr('{}.v'.format(skel_grp), False)

    xshader = cmds.shadingNode('lambert', asShader=True, name='xRed')
    cmds.setAttr('{}.color'.format(xshader), 1, 0, 0)
    yshader = cmds.shadingNode('lambert', asShader=True, name='yGreen')
    cmds.setAttr('{}.color'.format(yshader), 0, 1, 0)
    zshader = cmds.shadingNode('lambert', asShader=True, name='zBlue')
    cmds.setAttr('{}.color'.format(zshader), 0, 0, 1)

    for f in xrange(cmds.polyEvaluate(cube, f=True)):
        face = '{}.f[{}]'.format(cube, f)
        normal = [float(x) for x in cmds.polyInfo(face, fn=True)[0].split(':')[-1][1:-2].split(' ')]
        print f, normal
        shader = xshader
        print normal
        if normal[1]:
            shader = yshader
        elif normal[2]:
            shader = zshader

        cmds.select(face)
        cmds.hyperShade(assign=shader)
    cmds.select(clear=True)
    cmds.displaySmoothness(cube, polygonObject=3)
    cmds.connectAttr('{}.worldInverseMatrix[0]'.format(skel_grp), '{}.parentInverseMatrix'.format(ik_node))

build()
