# rkt_nodes

sharing a few custom maya nodes for people to play with

rkt_ikSplineSolver alpha available for now

```python
from maya import cmds


def build():
    ik_node = cmds.createNode('rkt_ikSplineSolver')
    control_1 = cmds.spaceLocator()[0]
    control_2 = cmds.spaceLocator()[0]
    control_3 = cmds.spaceLocator()[0]

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
    for x in xrange(samples):
        joint_obj = cmds.createNode('joint')
        cmds.connectAttr('{}.outSRT[{}].outTranslate'.format(ik_node, x),
                         '{}.translate'.format(joint_obj))
        cmds.connectAttr('{}.outSRT[{}].outRotate'.format(ik_node, x),
                         '{}.rotate'.format(joint_obj))

build()
```
