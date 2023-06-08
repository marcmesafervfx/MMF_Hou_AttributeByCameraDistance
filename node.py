import sys
import toolutils

outputitem = None
inputindex = -1
inputitem = None
outputindex = -1

num_args = 1
h_extra_args = ''
pane = toolutils.activePane(kwargs)
if not isinstance(pane, hou.NetworkEditor):
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage(
               'Cannot create node: cannot find any network pane')
       sys.exit(0)
else: # We're creating this tool from the TAB menu inside a network editor
    pane_node = pane.pwd()
    if "outputnodename" in kwargs and "inputindex" in kwargs:
        outputitem = pane_node.item(kwargs["outputnodename"])
        inputindex = kwargs["inputindex"]
        h_extra_args += 'set arg4 = "' + kwargs["outputnodename"] + '"\n'
        h_extra_args += 'set arg5 = "' + str(inputindex) + '"\n'
        num_args = 6
    if "inputnodename" in kwargs and "outputindex" in kwargs:
        inputitem = pane_node.item(kwargs["inputnodename"])
        outputindex = kwargs["outputindex"]
        h_extra_args += 'set arg6 = "' + kwargs["inputnodename"] + '"\n'
        h_extra_args += 'set arg9 = "' + str(outputindex) + '"\n'
        num_args = 9
    if "autoplace" in kwargs:
        autoplace = kwargs["autoplace"]
    else:
        autoplace = False
    # If shift-clicked we want to auto append to the current
    # node
    if "shiftclick" in kwargs and kwargs["shiftclick"]:
        if inputitem is None:
            inputitem = pane.currentNode()
            outputindex = 0
    if "nodepositionx" in kwargs and             "nodepositiony" in kwargs:
        try:
            pos = [ float( kwargs["nodepositionx"] ),
                    float( kwargs["nodepositiony"] )]
        except:
            pos = None
    else:
        pos = None

    if not autoplace and not pane.listMode():
        if pos is not None:
            pass
        elif outputitem is None:
            pos = pane.selectPosition(inputitem, outputindex, None, -1)
        else:
            pos = pane.selectPosition(inputitem, outputindex,
                                      outputitem, inputindex)

    if pos is not None:
        if "node_bbox" in kwargs:
            size = kwargs["node_bbox"]
            pos[0] -= size[0] / 2
            pos[1] -= size[1] / 2
        else:
            pos[0] -= 0.573625
            pos[1] -= 0.220625
        h_extra_args += 'set arg2 = "' + str(pos[0]) + '"\n'
        h_extra_args += 'set arg3 = "' + str(pos[1]) + '"\n'
h_extra_args += 'set argc = "' + str(num_args) + '"\n'

pane_node = pane.pwd()
child_type = pane_node.childTypeCategory().nodeTypes()

if 'subnet' not in child_type:
   hou.ui.displayMessage(
           'Cannot create node: incompatible pane network type')
   sys.exit(0)

# First clear the node selection
pane_node.setSelected(False, True)

h_path = pane_node.path()
h_preamble = 'set arg1 = "' + h_path + '"\n'
h_cmd = r'''
if ($argc < 2 || "$arg2" == "") then
   set arg2 = 0
endif
if ($argc < 3 || "$arg3" == "") then
   set arg3 = 0
endif
# Automatically generated script
# $arg1 - the path to add this node
# $arg2 - x position of the tile
# $arg3 - y position of the tile
# $arg4 - input node to wire to
# $arg5 - which input to wire to
# $arg6 - output node to wire to
# $arg7 - the type of this node
# $arg8 - the node is an indirect input
# $arg9 - index of output from $arg6

\set noalias = 1
set saved_path = `execute("oppwf")`
opcf $arg1

# Node $_obj_geo1_MMF_AttributeByCameraDistance (Sop/subnet)
set _obj_geo1_MMF_AttributeByCameraDistance = `run("opadd -e -n -v subnet MMF_AttributeByCameraDistance")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_geo1_MMF_AttributeByCameraDistance
opspareds '    parm {         name    "label1"         baseparm         label   "Input #1 Label"         invisible         export  all     }     parm {         name    "label2"         baseparm         label   "Input #2 Label"         invisible         export  all     }     parm {         name    "label3"         baseparm         label   "Input #3 Label"         invisible         export  all     }     parm {         name    "label4"         baseparm         label   "Input #4 Label"         invisible         export  all     }     groupsimple {         name    "settings"         label   "Settings"          parm {             name    "camera"             label   "Camera"             type    oppath             default { "/obj/cam1" }             parmtag { "opfilter" "!!OBJ/CAMERA!!" }             parmtag { "oprelative" "." }             parmtag { "script_callback_language" "python" }         }         parm {             name    "attr_name"             label   "Attribute Name"             type    string             default { "distance" }             parmtag { "script_callback_language" "python" }         }         parm {             name    "attr_ramp"             label   "Attr Ramp"             type    ramp_flt             default { "2" }             range   { 1! 10 }             parmtag { "script_callback_language" "python" }         }     }  ' $_obj_geo1_MMF_AttributeByCameraDistance
opparm $_obj_geo1_MMF_AttributeByCameraDistance  attr_ramp ( 2 )
opparm -V 19.0.383 $_obj_geo1_MMF_AttributeByCameraDistance attr_ramp2pos ( 1 ) attr_ramp2value ( 1 )
opcolor -c 0.45100000500679016 0.36899998784065247 0.79600000381469727 $_obj_geo1_MMF_AttributeByCameraDistance
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance
opuserdata -n '___Version___' -v '18.5.696' $_obj_geo1_MMF_AttributeByCameraDistance
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance
opcf $_obj_geo1_MMF_AttributeByCameraDistance

# Node $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist (Sop/attribwrangle)
set _obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist = `run("opadd -e -n -v attribwrangle attr_by_dist")`
oplocate -x `$arg2 + -3.4809999999999999` -y `$arg3 + 1.9924999999999999` $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "attr_ramp"         label   "Attr Ramp"         type    ramp_flt         default { "2" }         range   { 1! 10 }     } ' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist
opmultiparm $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist 'color_ramp#pos' '../attr_ramp#pos' 'color_ramp#cr' '../attr_ramp#cr' 'color_ramp#cg' '../attr_ramp#cg' 'color_ramp#cb' '../attr_ramp#cb' 'color_ramp#interp' '../attr_ramp#interp' 'attr_ramp#pos' '../attr_ramp#pos' 'attr_ramp#value' '../attr_ramp#value' 'attr_ramp#interp' '../attr_ramp#interp'
opparm $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist  bindings ( 1 ) groupbindings ( 0 ) attr_ramp ( 2 )
chblockbegin
chadd -t 0 0 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist attr_ramp
chkey -t 0 -v 2 -m 0 -a 0 -A 0 -T a  -F 'ch("../attr_ramp")' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist/attr_ramp
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist attr_ramp1pos
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attr_ramp1pos")' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist/attr_ramp1pos
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist attr_ramp1value
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attr_ramp1value")' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist/attr_ramp1value
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist attr_ramp1interp
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../attr_ramp1interp")' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist/attr_ramp1interp
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist attr_ramp2pos
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attr_ramp2pos")' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist/attr_ramp2pos
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist attr_ramp2value
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("../attr_ramp2value")' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist/attr_ramp2value
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist attr_ramp2interp
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../attr_ramp2interp")' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist/attr_ramp2interp
chblockend
opparm $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist snippet ( 'float maxdist = detail(0, \'_maxdist\', 0);\nfloat mindist = detail(0, \'_mindist\', 0);\n\nfloat normDist = fit(@_dist, mindist, maxdist, 0, 1);\n\nfloat attr = chramp(\'attr_ramp\', normDist);\n\nf@user_attr = attr;\n\n' ) bindings ( 1 ) attr_ramp ( attr_ramp ) attr_ramp1pos ( attr_ramp1pos ) attr_ramp1value ( attr_ramp1value ) attr_ramp1interp ( attr_ramp1interp ) attr_ramp2pos ( attr_ramp2pos ) attr_ramp2value ( attr_ramp2value ) attr_ramp2interp ( attr_ramp2interp ) bindname1 ( '`chs("../attr_name")`' ) bindparm1 ( user_attr )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist
opuserdata -n '___Version___' -v '' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist

# Node $_obj_geo1_MMF_AttributeByCameraDistance_get_distance (Sop/attribwrangle)
set _obj_geo1_MMF_AttributeByCameraDistance_get_distance = `run("opadd -e -n -v attribwrangle get_distance")`
oplocate -x `$arg2 + -3.4809999999999999` -y `$arg3 + 5.0702999999999996` $_obj_geo1_MMF_AttributeByCameraDistance_get_distance
opparm $_obj_geo1_MMF_AttributeByCameraDistance_get_distance  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_geo1_MMF_AttributeByCameraDistance_get_distance snippet ( 'vector pos = point(1, \'P\', 0);\n@_dist = distance(@P, pos);' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance_get_distance
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance_get_distance
opuserdata -n '___Version___' -v '' $_obj_geo1_MMF_AttributeByCameraDistance_get_distance
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance_get_distance
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance_get_distance

# Node $_obj_geo1_MMF_AttributeByCameraDistance_maxdist (Sop/attribpromote)
set _obj_geo1_MMF_AttributeByCameraDistance_maxdist = `run("opadd -e -n -v attribpromote maxdist")`
oplocate -x `$arg2 + -3.4813999999999998` -y `$arg3 + 4.0324` $_obj_geo1_MMF_AttributeByCameraDistance_maxdist
opparm -V 19.0.383 $_obj_geo1_MMF_AttributeByCameraDistance_maxdist inname ( _dist ) outclass ( detail ) method ( max ) useoutname ( on ) outname ( _maxdist ) deletein ( off )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance_maxdist
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance_maxdist
opuserdata -n '___Version___' -v '18.5.696' $_obj_geo1_MMF_AttributeByCameraDistance_maxdist
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance_maxdist
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance_maxdist

# Node $_obj_geo1_MMF_AttributeByCameraDistance_mindist (Sop/attribpromote)
set _obj_geo1_MMF_AttributeByCameraDistance_mindist = `run("opadd -e -n -v attribpromote mindist")`
oplocate -x `$arg2 + -3.4813999999999998` -y `$arg3 + 3.0324` $_obj_geo1_MMF_AttributeByCameraDistance_mindist
opparm -V 19.0.383 $_obj_geo1_MMF_AttributeByCameraDistance_mindist inname ( _dist ) outclass ( detail ) method ( min ) useoutname ( on ) outname ( _mindist ) deletein ( off )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance_mindist
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance_mindist
opuserdata -n '___Version___' -v '18.5.696' $_obj_geo1_MMF_AttributeByCameraDistance_mindist
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance_mindist
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance_mindist

# Node $_obj_geo1_MMF_AttributeByCameraDistance_in_cam (Sop/object_merge)
set _obj_geo1_MMF_AttributeByCameraDistance_in_cam = `run("opadd -e -n -v object_merge in_cam")`
oplocate -x `$arg2 + -2.5012500286102295` -y `$arg3 + 6.3397692196796118` $_obj_geo1_MMF_AttributeByCameraDistance_in_cam
opparm $_obj_geo1_MMF_AttributeByCameraDistance_in_cam  numobj ( 1 )
opparm -V 19.0.383 $_obj_geo1_MMF_AttributeByCameraDistance_in_cam xformtype ( local ) objpath1 ( '`chsop("../camera")`/camOrigin' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance_in_cam
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance_in_cam
opuserdata -n '___Version___' -v '18.5.696' $_obj_geo1_MMF_AttributeByCameraDistance_in_cam
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance_in_cam
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance_in_cam

# Node $_obj_geo1_MMF_AttributeByCameraDistance_output0 (Sop/output)
set _obj_geo1_MMF_AttributeByCameraDistance_output0 = `run("opadd -e -n -v output output0")`
oplocate -x `$arg2 + -3.4780000000000002` -y `$arg3 + -0.077668100000000004` $_obj_geo1_MMF_AttributeByCameraDistance_output0
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_geo1_MMF_AttributeByCameraDistance_output0 outputidx
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'max(opdigits("."),0)' $_obj_geo1_MMF_AttributeByCameraDistance_output0/outputidx
chblockend
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance_output0
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance_output0
opuserdata -n '___Version___' -v '18.5.696' $_obj_geo1_MMF_AttributeByCameraDistance_output0
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance_output0
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance_output0

# Node $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr (Sop/attribdelete)
set _obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr = `run("opadd -e -n -v attribdelete remove_used_attr")`
oplocate -x `$arg2 + -3.4814500000000002` -y `$arg3 + 0.94987600000000005` $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr
opparm $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr ptdel ( _* ) dtldel ( _* )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr
opexprlanguage -s hscript $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr
opuserdata -n '___Version___' -v '' $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr
opuserdata -n '___toolcount___' -v '2' $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr
opuserdata -n '___toolid___' -v 'dist' $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr
oporder -e attr_by_dist get_distance maxdist mindist in_cam output0 remove_used_attr 
opcf ..
opset -p on $_obj_geo1_MMF_AttributeByCameraDistance

opcf $arg1
opcf $_obj_geo1_MMF_AttributeByCameraDistance
opwire -n $_obj_geo1_MMF_AttributeByCameraDistance_mindist -0 $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist
opwire -n -i 0 -0 $_obj_geo1_MMF_AttributeByCameraDistance_get_distance
opwire -n $_obj_geo1_MMF_AttributeByCameraDistance_in_cam -1 $_obj_geo1_MMF_AttributeByCameraDistance_get_distance
opwire -n $_obj_geo1_MMF_AttributeByCameraDistance_get_distance -0 $_obj_geo1_MMF_AttributeByCameraDistance_maxdist
opwire -n $_obj_geo1_MMF_AttributeByCameraDistance_maxdist -0 $_obj_geo1_MMF_AttributeByCameraDistance_mindist
opwire -n $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr -0 $_obj_geo1_MMF_AttributeByCameraDistance_output0
opwire -n $_obj_geo1_MMF_AttributeByCameraDistance_attr_by_dist -0 $_obj_geo1_MMF_AttributeByCameraDistance_remove_used_attr
opcf ..

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_geo1_MMF_AttributeByCameraDistance
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_geo1_MMF_AttributeByCameraDistance
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)
