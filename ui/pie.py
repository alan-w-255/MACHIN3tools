import bpy
import os
from bpy.types import Menu
from bpy.props import IntProperty, StringProperty, BoolProperty, FloatProperty, EnumProperty
import bmesh
from .. utils import MACHIN3 as m3


# SNAPPING

class SnapActive(bpy.types.Operator):
    bl_idname = "snap.active"
    bl_label = "Snap Active"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.use_snap == (True):
            bpy.context.scene.tool_settings.use_snap = False

        elif bpy.context.scene.tool_settings.use_snap == (False):
            bpy.context.scene.tool_settings.use_snap = True

        return {'FINISHED'}


class SnapVolume(bpy.types.Operator):
    bl_idname = "snap.volume"
    bl_label = "Snap Volume"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'VOLUME'

        if bpy.context.scene.tool_settings.snap_element != 'VOLUME':
            bpy.context.scene.tool_settings.snap_element = 'VOLUME'
        return {'FINISHED'}


class SnapFace(bpy.types.Operator):
    bl_idname = "snap.face"
    bl_label = "Snap Face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'FACE'

        if bpy.context.scene.tool_settings.snap_element != 'FACE':
            bpy.context.scene.tool_settings.snap_element = 'FACE'
        return {'FINISHED'}


class SnapEdge(bpy.types.Operator):
    bl_idname = "snap.edge"
    bl_label = "Snap Edge"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'EDGE'

        if bpy.context.scene.tool_settings.snap_element != 'EDGE':
            bpy.context.scene.tool_settings.snap_element = 'EDGE'
        return {'FINISHED'}


class SnapVertex(bpy.types.Operator):
    bl_idname = "snap.vertex"
    bl_label = "Snap Vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'VERTEX'

        if bpy.context.scene.tool_settings.snap_element != 'VERTEX':
            bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        return {'FINISHED'}


class SnapIncrement(bpy.types.Operator):
    bl_idname = "snap.increment"
    bl_label = "Snap Increment"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if bpy.context.scene.tool_settings.use_snap == (False):
            # bpy.context.scene.tool_settings.use_snap = True
            # bpy.context.scene.tool_settings.snap_element = 'INCREMENT'

        if bpy.context.scene.tool_settings.snap_element != 'INCREMENT':
            bpy.context.scene.tool_settings.snap_element = 'INCREMENT'
        return {'FINISHED'}


class SnapAlignRotation(bpy.types.Operator):
    bl_idname = "snap.alignrotation"
    bl_label = "Snap Align rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.scene.tool_settings.use_snap_align_rotation == (True):
            bpy.context.scene.tool_settings.use_snap_align_rotation = False

        elif bpy.context.scene.tool_settings.use_snap_align_rotation == (False):
            bpy.context.scene.tool_settings.use_snap_align_rotation = True

        return {'FINISHED'}


class SnapTargetVariable(bpy.types.Operator):
    bl_idname = "object.snaptargetvariable"
    bl_label = "Snap Target Variable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_target=self.variable
        return {'FINISHED'}


# ORIENTATION

class OrientationVariable(bpy.types.Operator):
    bl_idname = "object.orientationvariable"
    bl_label = "Orientation Variable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.space_data.transform_orientation=self.variable
        return {'FINISHED'}


# OBJECT SHADING

class WireSelectedAll(bpy.types.Operator):
    bl_idname = "wire.selectedall"
    bl_label = "Wire Selected All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        for obj in bpy.data.objects:
            if bpy.context.selected_objects:
                if obj.select:
                    if obj.show_wire:
                        obj.show_all_edges = False
                        obj.show_wire = False
                    else:
                        obj.show_all_edges = True
                        obj.show_wire = True
            elif not bpy.context.selected_objects:
                if obj.show_wire:
                    obj.show_all_edges = False
                    obj.show_wire = False
                else:
                    obj.show_all_edges = True
                    obj.show_wire = True
        return {'FINISHED'}


class ToggleGridAxis(bpy.types.Operator):
    bl_idname = "scene.togglegridaxis"
    bl_label = "Toggle Grid and Axis in 3D view"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.show_axis_y = not bpy.context.space_data.show_axis_y
        bpy.context.space_data.show_axis_x = not bpy.context.space_data.show_axis_x
        bpy.context.space_data.show_floor = not bpy.context.space_data.show_floor
        return {'FINISHED'}


class MeshDisplayOverlays(bpy.types.Menu):
    bl_idname = "meshdisplay.overlays"
    bl_label = "Mesh Display Overlays"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout

        # with_freestyle = bpy.app.build_options.freestyle

        mesh = context.active_object.data
        # scene = context.scene

        split = layout.split()

        col = split.column()
        col.label(text="Overlays:")
        col.prop(mesh, "show_faces", text="Faces")
        col.prop(mesh, "show_edges", text="Edges")
        col.prop(mesh, "show_edge_crease", text="Creases")
        col.prop(mesh, "show_edge_seams", text="Seams")
        layout.prop(mesh, "show_weight")
        col.prop(mesh, "show_edge_sharp", text="Sharp")
        col.prop(mesh, "show_edge_bevel_weight", text="Bevel")
        col.prop(mesh, "show_freestyle_edge_marks", text="Edge Marks")
        col.prop(mesh, "show_freestyle_face_marks", text="Face Marks")


######################
#    Pivot Point     #
######################

class PivotPointVariable(bpy.types.Operator):
    bl_idname = "pivotpoint.variable"
    bl_label = "PivotPointVariable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.space_data.pivot_point = self.variable
        return {'FINISHED'}


class UsePivotAlign(bpy.types.Operator):
    bl_idname = "use.pivotalign"
    bl_label = "Use Pivot Align"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.space_data.use_pivot_point_align == (False):
            bpy.context.space_data.use_pivot_point_align = True
        elif bpy.context.space_data.use_pivot_point_align == (True):
            bpy.context.space_data.use_pivot_point_align = False
        return {'FINISHED'}

######################
#    Manipulators    #
######################
class ManipTranslate(bpy.types.Operator):
    bl_idname = "manip.translate"
    bl_label = "Manip Translate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE'}
        return {'FINISHED'}

class ManipRotate(bpy.types.Operator):
    bl_idname = "manip.rotate"
    bl_label = "Manip Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'ROTATE'}
        if bpy.context.space_data.transform_manipulators != {'ROTATE'}:
            bpy.context.space_data.transform_manipulators = {'ROTATE'}
        return {'FINISHED'}

class ManipScale(bpy.types.Operator):
    bl_idname = "manip.scale"
    bl_label = "Manip Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'SCALE'}
        return {'FINISHED'}

class TranslateRotate(bpy.types.Operator):
    bl_idname = "translate.rotate"
    bl_label = "Translate Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE', 'ROTATE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE'}
        return {'FINISHED'}

class TranslateScale(bpy.types.Operator):
    bl_idname = "translate.scale"
    bl_label = "Translate Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE', 'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'SCALE'}
        return {'FINISHED'}

class RotateScale(bpy.types.Operator):
    bl_idname = "rotate.scale"
    bl_label = "Rotate Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'ROTATE', 'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'ROTATE', 'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'ROTATE', 'SCALE'}
        return {'FINISHED'}

class TranslateRotateScale(bpy.types.Operator):
    bl_idname = "translate.rotatescale"
    bl_label = "Translate Rotate Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.space_data.show_manipulator == (False) :
            bpy.context.space_data.show_manipulator = True
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE', 'SCALE'}
        if bpy.context.space_data.transform_manipulators != {'TRANSLATE', 'ROTATE', 'SCALE'}:
            bpy.context.space_data.transform_manipulators = {'TRANSLATE', 'ROTATE', 'SCALE'}
        return {'FINISHED'}

class WManupulators(bpy.types.Operator):
    bl_idname = "w.manupulators"
    bl_label = "W Manupulators"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.space_data.show_manipulator == (True):
            bpy.context.space_data.show_manipulator = False

        elif bpy.context.space_data.show_manipulator == (False):
            bpy.context.space_data.show_manipulator = True

        return {'FINISHED'}

######################
#       Modes        #
######################

# Define Class Texture Paint
class ClassTexturePaint(bpy.types.Operator):
    bl_idname = "class.pietexturepaint"
    bl_label = "Class Texture Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.texture_paint_toggle()
        else:
            bpy.ops.paint.texture_paint_toggle()
        return {'FINISHED'}

# Define Class Weight Paint
class ClassWeightPaint(bpy.types.Operator):
    bl_idname = "class.pieweightpaint"
    bl_label = "Class Weight Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.weight_paint_toggle()
        else:
            bpy.ops.paint.weight_paint_toggle()
        return {'FINISHED'}

# Define Class Vertex Paint
class ClassVertexPaint(bpy.types.Operator):
    bl_idname = "class.pievertexpaint"
    bl_label = "Class Vertex Paint"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.paint.vertex_paint_toggle()
        else:
            bpy.ops.paint.vertex_paint_toggle()
        return {'FINISHED'}

# Define Class Particle Edit
class ClassParticleEdit(bpy.types.Operator):
    bl_idname = "class.pieparticleedit"
    bl_label = "Class Particle Edit"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        if bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.particle.particle_edit_toggle()
        else:
            bpy.ops.particle.particle_edit_toggle()

        return {'FINISHED'}



######################
#   Selection Mode   #
######################

# Components Selection Mode
class VertsEdges(bpy.types.Operator):
    bl_idname = "verts.edges"
    bl_label = "Verts Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (True, True, False)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (True, True, False)
            return {'FINISHED'}


class EdgesFaces(bpy.types.Operator):
    bl_idname = "edges.faces"
    bl_label = "EdgesFaces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (False, True, True)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (False, True, True)
            return {'FINISHED'}

class VertsFaces(bpy.types.Operator):
    bl_idname = "verts.faces"
    bl_label = "Verts Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (True, False, True)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (True, False, True)
            return {'FINISHED'}

class VertsEdgesFaces(bpy.types.Operator):
    bl_idname = "verts.edgesfaces"
    bl_label = "Verts Edges Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        if bpy.context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (True, True, True)
        if bpy.context.object.mode == "EDIT":
            bpy.context.tool_settings.mesh_select_mode = (True, True, True)
            return {'FINISHED'}

#Select All By Selection
class SelectAllBySelection(bpy.types.Operator):
    bl_idname = "object.selectallbyselection"
    bl_label = "Verts Edges Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.select_all(action='TOGGLE')
        return {'FINISHED'}

######################
#       Views        #
######################

# Split area horizontal
class SplitHorizontal(bpy.types.Operator):
    bl_idname = "split.horizontal"
    bl_label = "split horizontal"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        bpy.ops.screen.area_split(direction='HORIZONTAL')
        return {'FINISHED'}

# Split area vertical
class SplitVertical(bpy.types.Operator):
    bl_idname = "split.vertical"
    bl_label = "split vertical"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout

        bpy.ops.screen.area_split(direction='VERTICAL')
        return {'FINISHED'}


# Join area
class JoinArea(bpy.types.Operator):
    """Join 2 area, clic on the second area to join"""
    bl_idname = "area.joinarea"
    bl_label = "Join Area"
    bl_options = {'REGISTER', 'UNDO'}

    min_x = IntProperty()
    min_y = IntProperty()

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            self.max_x = event.mouse_x
            self.max_y = event.mouse_y
            bpy.ops.screen.area_join(min_x=self.min_x, min_y=self.min_y, max_x=self.max_x, max_y=self.max_y)
            bpy.ops.screen.screen_full_area()
            bpy.ops.screen.screen_full_area()
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.min_x = event.mouse_x
        self.min_y = event.mouse_y
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

#View Class menu
class ViewMenu(bpy.types.Operator):
    """Menu to change views"""
    bl_idname = "object.view_menu"
    bl_label = "View_Menu"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.area.type=self.variable
        return {'FINISHED'}

# MACHIN3
class LayoutSwitch(bpy.types.Operator):
    """Menu to switch screen layouts"""
    bl_idname = "machin3.layout_switch"
    bl_label = "Layout_Switch"
    bl_options = {'REGISTER', 'UNDO'}


    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.window.screen=bpy.data.screens[self.variable]

        if self.variable == "M3 compositing":
            context.scene.render.use_compositing = True

        return {'FINISHED'}
# /MACHIN3

# MACHIN3
class DissolveGroupPro(bpy.types.Operator):
    bl_idname = "machin3.dissolve_grouppro"
    bl_label = "Dissolve GroupPro"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        groupobjects = bpy.context.active_object.dupli_group.objects

        bpy.ops.object.edit_grouppro()

        m3.unselect_all("OBJECT")

        for obj in groupobjects:
            obj.select = True

        bpy.ops.object.remove_from_grouppro()
        bpy.ops.object.close_grouppro()

        m3.make_active(obj)

        return {'FINISHED'}
# /MACHIN3


##############
#   Sculpt   #
##############

# Sculpt Polish
class SculptPolish(bpy.types.Operator):
    bl_idname = "sculpt.polish"
    bl_label = "Sculpt Polish"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        bpy.context.tool_settings.sculpt.brush=bpy.data.brushes['Polish']
        return {'FINISHED'}

# Sculpt Polish
class SculptSculptDraw(bpy.types.Operator):
    bl_idname = "sculpt.sculptraw"
    bl_label = "Sculpt SculptDraw"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        layout = self.layout
        bpy.context.tool_settings.sculpt.brush=bpy.data.brushes['SculptDraw']
        return {'FINISHED'}

######################
#   Cursor/Origin    #
######################

#Pivot to selection
class PivotToSelection(bpy.types.Operator):
    bl_idname = "object.pivot2selection"
    bl_label = "Pivot To Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        saved_location = bpy.context.scene.cursor_location.copy()
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor_location = saved_location
        return {'FINISHED'}

#Pivot to Bottom
class PivotBottom(bpy.types.Operator):
    bl_idname = "object.pivotobottom"
    bl_label = "Pivot To Bottom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        o=bpy.context.active_object
        init=0
        for x in o.data.vertices:
            if init==0:
                a=x.co.z
                init=1
            elif x.co.z<a:
                a=x.co.z

        for x in o.data.vertices:
            x.co.z-=a

        o.location.z+=a
        bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}

#####################
#   Simple Align    #
#####################
#Align X
class AlignX(bpy.types.Operator):
    bl_idname = "align.x"
    bl_label = "Align  X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}

#Align Y
class AlignY(bpy.types.Operator):
    bl_idname = "align.y"
    bl_label = "Align  Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(1, 0, 1), constraint_axis=(False, True, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}

#Align Z
class AlignZ(bpy.types.Operator):
    bl_idname = "align.z"
    bl_label = "Align  Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for vert in bpy.context.object.data.vertices:
            bpy.ops.transform.resize(value=(1, 1, 0), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
        return {'FINISHED'}

#####################
#    Align To 0     #
#####################

#Align to X - 0
class AlignToX0(bpy.types.Operator):
    bl_idname = "align.2x0"
    bl_label = "Align To X-0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[0] = 0
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

#Align to Z - 0
class AlignToY0(bpy.types.Operator):
    bl_idname = "align.2y0"
    bl_label = "Align To Y-0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[1] = 0
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

#Align to Z - 0
class AlignToZ0(bpy.types.Operator):
    bl_idname = "align.2z0"
    bl_label = "Align To Z-0"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[2] = 0
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

#Align X Left
class AlignXLeft(bpy.types.Operator):
    bl_idname = "alignx.left"
    bl_label = "Align X Left"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 0
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align X Right
class AlignXRight(bpy.types.Operator):
    bl_idname = "alignx.right"
    bl_label = "Align X Right"

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 0
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Y Back
class AlignYBack(bpy.types.Operator):
    bl_idname = "aligny.back"
    bl_label = "Align Y back"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 1
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Y Front
class AlignYFront(bpy.types.Operator):
    bl_idname = "aligny.front"
    bl_label = "Align Y Front"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 1
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Z Top
class AlignZTop(bpy.types.Operator):
    bl_idname = "alignz.top"
    bl_label = "Align Z Top"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 2
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] > max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#Align Z Bottom
class AlignZBottom(bpy.types.Operator):
    bl_idname = "alignz.bottom"
    bl_label = "Align Z Bottom"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode='OBJECT')
        count = 0
        axe = 2
        for vert in bpy.context.object.data.vertices:
            if vert.select:
                if count == 0:
                    max = vert.co[axe]
                    count += 1
                    continue
                count += 1
                if vert.co[axe] < max:
                    max = vert.co[axe]

        bpy.ops.object.mode_set(mode='OBJECT')

        for vert in bpy.context.object.data.vertices:
            if vert.select:
                vert.co[axe] = max
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

#################
#    Delete     #
#################

#Limited Dissolve
class DeleteLimitedDissolve(bpy.types.Operator):
    bl_idname = "delete.limiteddissolve"
    bl_label = "Delete Limited Dissolve"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        bpy.ops.mesh.dissolve_limited(angle_limit=3.14159, use_dissolve_boundaries=False)
        return {'FINISHED'}

####################
#    Animation     #
####################

#Insert Auto Keyframe
class InsertAutoKeyframe(bpy.types.Operator):
    bl_idname = "insert.autokeyframe"
    bl_label = "Insert Auto Keyframe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if bpy.context.scene.tool_settings.use_keyframe_insert_auto == True :
            bpy.context.scene.tool_settings.use_keyframe_insert_auto = False

        if bpy.context.scene.tool_settings.use_keyframe_insert_auto == False :
            bpy.context.scene.tool_settings.use_keyframe_insert_auto = True

        return {'FINISHED'}

###########################
#    Apply Transforms     #
###########################

#Apply Transforms
class ApplyTransformLocation(bpy.types.Operator):
    bl_idname = "apply.transformlocation"
    bl_label = "Apply Transform Location"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformRotation(bpy.types.Operator):
    bl_idname = "apply.transformrotation"
    bl_label = "Apply Transform Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformScale(bpy.types.Operator):
    bl_idname = "apply.transformscale"
    bl_label = "Apply Transform Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformRotationScale(bpy.types.Operator):
    bl_idname = "apply.transformrotationscale"
    bl_label = "Apply Transform Rotation Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        return {'FINISHED'}

#Apply Transforms
class ApplyTransformAll(bpy.types.Operator):
    bl_idname = "apply.transformall"
    bl_label = "Apply Transform All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {'FINISHED'}


# Clear Menu
class ClearMenu(bpy.types.Menu):
    bl_idname = "clear.menu"
    bl_label = "Clear Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.location_clear", text="Clear Location", icon='MAN_TRANS')
        layout.operator("object.rotation_clear", text="Clear Rotation", icon='MAN_ROT')
        layout.operator("object.scale_clear", text="Clear Scale", icon='MAN_SCALE')
        layout.operator("object.origin_clear", text="Clear Origin", icon='MANIPUL')

#Clear all
class ClearAll(bpy.types.Operator):
    bl_idname = "clear.all"
    bl_label = "Clear All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()
        return {'FINISHED'}

########################
#    Open/Save/...     #
########################

#ExtVernal Data
class ExternalData(bpy.types.Menu):
    bl_idname = "external.data"
    bl_label = "External Data"

    def draw(self, context):
        layout = self.layout

        layout.operator("file.autopack_toggle", text="Automatically Pack Into .blend")
        layout.separator()
        layout.operator("file.pack_all", text="Pack All Into .blend")
        layout.operator("file.unpack_all", text="Unpack All Into Files")
        layout.separator()
        layout.operator("file.make_paths_relative", text="Make All Paths Relative")
        layout.operator("file.make_paths_absolute", text="Make All Paths Absolute")
        layout.operator("file.report_missing_files", text="Report Missing Files")
        layout.operator("file.find_missing_files", text="Find Missing Files")


######################
#    Views Ortho     #
######################
#Persp/Ortho
class PerspOrthoView(bpy.types.Operator):
    bl_idname = "persp.orthoview"
    bl_label = "Persp/Ortho"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.view3d.view_persportho()
        return {'FINISHED'}


#######################################################
# Camera                                              #
#######################################################

#Lock Camera Transforms
class LockCameraTransforms(bpy.types.Operator):
    bl_idname = "object.lockcameratransforms"
    bl_label = "Lock Camera Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.lock_rotation[0] == False:
            bpy.context.object.lock_rotation[0] = True
            bpy.context.object.lock_rotation[1] = True
            bpy.context.object.lock_rotation[2] = True
            bpy.context.object.lock_location[0] = True
            bpy.context.object.lock_location[1] = True
            bpy.context.object.lock_location[2] = True
            bpy.context.object.lock_scale[0] = True
            bpy.context.object.lock_scale[1] = True
            bpy.context.object.lock_scale[2] = True

        elif bpy.context.object.lock_rotation[0] == True :
            bpy.context.object.lock_rotation[0] = False
            bpy.context.object.lock_rotation[1] = False
            bpy.context.object.lock_rotation[2] = False
            bpy.context.object.lock_location[0] = False
            bpy.context.object.lock_location[1] = False
            bpy.context.object.lock_location[2] = False
            bpy.context.object.lock_scale[0] = False
            bpy.context.object.lock_scale[1] = False
            bpy.context.object.lock_scale[2] = False
        return {'FINISHED'}

#Active Camera
bpy.types.Scene.cameratoto = bpy.props.StringProperty(default="")

class ActiveCameraSelection(bpy.types.Operator):
    bl_idname = "object.activecameraselection"
    bl_label = "Active Camera Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.data.objects[context.scene.cameratoto].select=True
        bpy.ops.view3d.object_as_camera()
        return {'FINISHED'}

#Select Camera
class CameraSelection(bpy.types.Operator):
    bl_idname = "object.cameraselection"
    bl_label = "Camera Selection"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for cam in bpy.data.cameras:
            bpy.ops.object.select_camera()

        return {'FINISHED'}

#Pie Material
class MaterialListMenu(bpy.types.Menu): # menu appelé par le pie
    bl_idname = "object.material_list_menu"
    bl_label = "Material_list"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        if len(bpy.data.materials): # "len" retourne le nombre d'occurence donc, si il y a des materiaux dans les datas:
            for mat in bpy.data.materials:
                name = mat.name
                try:
                    icon_val = layout.icon(mat) # récupère l'icon du materiau
                except:
                    icon_val = 1
                    print ("WARNING [Mat Panel]: Could not get icon value for %s" % name)

                op = col.operator("object.apply_material", text=name, icon_value=icon_val) # opérateur qui apparait dans le menu pour chaque matériau présent dans les datas materials
                op.mat_to_assign = name # on "stock" le nom du matériau dans la variable "mat_to_assign" declarée dans la class opérateur "ApplyMaterial"
        else:
            layout.label("No data materials")



class ApplyMaterial(bpy.types.Operator):
    bl_idname = "object.apply_material"
    bl_label = "Apply material"

    mat_to_assign = bpy.props.StringProperty(default="")

    def execute(self, context):

        if context.object.mode == 'EDIT':
            obj = context.object
            bm = bmesh.from_edit_mesh(obj.data)

            selected_face = [f for f in bm.faces if f.select]  # si des faces sont sélectionnées, elles sont stockées dans la liste "selected_faces"

            mat_name = [mat.name for mat in bpy.context.object.material_slots if len(bpy.context.object.material_slots)] # pour tout les material_slots, on stock les noms des mat de chaque slots dans la liste "mat_name"

            if self.mat_to_assign in mat_name: # on test si le nom du mat sélectionné dans le menu est présent dans la liste "mat_name" (donc, si un des slots possède le materiau du même nom). Si oui:
                context.object.active_material_index = mat_name.index(self.mat_to_assign) # on definit le slot portant le nom du comme comme étant le slot actif
                bpy.ops.object.material_slot_assign() # on assigne le matériau à la sélection
            else: # sinon
                bpy.ops.object.material_slot_add() # on ajout un slot
                bpy.context.object.active_material = bpy.data.materials[self.mat_to_assign] # on lui assigne le materiau choisi
                bpy.ops.object.material_slot_assign() # on assigne le matériau à la sélection

            return {'FINISHED'}

        elif context.object.mode == 'OBJECT':

            obj_list = [obj.name for obj in context.selected_objects]

            for obj in obj_list:
                bpy.ops.object.select_all(action='DESELECT')
                bpy.data.objects[obj].select = True
                bpy.context.scene.objects.active = bpy.data.objects[obj]
                bpy.context.object.active_material_index = 0

                if self.mat_to_assign == bpy.data.materials:
                    bpy.context.active_object.active_material = bpy.data.materials[mat_name]

                else:
                    if not len(bpy.context.object.material_slots):
                        bpy.ops.object.material_slot_add()

                    bpy.context.active_object.active_material = bpy.data.materials[self.mat_to_assign]

            for obj in obj_list:
                bpy.data.objects[obj].select = True

            return {'FINISHED'}
######################
#     Pie Menus      #
######################

# Pie Edit/Object Others modes - Tab
class PieObjectEditotherModes(Menu):
    bl_idname = "pie.objecteditmodeothermodes"
    bl_label = "Select Other Modes"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("class.pieweightpaint", text="Weight Paint", icon='WPAINT_HLT')
        #6 - RIGHT
        pie.operator("class.pietexturepaint", text="Texture Paint", icon='TPAINT_HLT')
        #2 - BOTTOM
        pie.operator("class.pieparticleedit", text="Particle Edit", icon='PARTICLEMODE')
        #8 - TOP
        pie.operator("class.pievertexpaint", text="Vertex Paint", icon='VPAINT_HLT')
        #7 - TOP - LEFT
        #9 - TOP - RIGHT
        #1 - BOTTOM - LEFT
        #3 - BOTTOM - RIGHT

# Pie Vertex/Edges/Faces Modes - Tab
class PieVertexEdgesFacesModes(Menu):
    bl_idname = "pie.vertexedgesfacesmodes"
    bl_label = "Select Multi Components"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("verts.faces", text="Vertex/Faces", icon='LOOPSEL')
        # 6 - RIGHT
        pie.operator("verts.edges", text="Vertex/Edges", icon='VERTEXSEL')
        # 2 - BOTTOM
        pie.operator("verts.edgesfaces", text="Vertex/Edges/Faces", icon='OBJECT_DATAMODE')
        # 8 - TOP
        pie.operator("edges.faces", text="Edges/Faces", icon='FACESEL')
        # 7 - TOP - LEFT
        # 9 - TOP - RIGHT
        # 1 - BOTTOM - LEFT
        # 3 - BOTTOM - RIGHT


class PieSelectMode(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_select_modes"
    bl_label = "Select Mode"


    def draw(self, context):
        layout = self.layout
        toolsettings = context.tool_settings

        ob = context

        if ob.object is not None:
            if ob.object.type == 'MESH':
                pie = layout.menu_pie()
                # 4 - LEFT
                pie.operator("machin3.select_vertex_mode", text="Vertex", icon='VERTEXSEL')
                # 6 - RIGHT
                pie.operator("machin3.select_face_mode", text="Face", icon='FACESEL')
                # 2 - BOTTOM
                pie.operator("machin3.select_edge_mode", text="Edge", icon='EDGESEL')
                # 8 - TOP
                if bpy.context.object.mode == "OBJECT":
                    text = "Edit"
                    icon = "EDITMODE_HLT"
                elif bpy.context.object.mode == "EDIT":
                    text = "Object"
                    icon = "OBJECT_DATAMODE"
                pie.operator("machin3.toggle_edit_mode", text=text, icon=icon)
                # 7 - TOP - LEFT
                if bpy.context.object.mode == "EDIT":
                    pie.prop(bpy.context.space_data, "use_occlude_geometry", text="Occlude")
                else:
                    pie.separator()

                # 9 - TOP - RIGHT
                pie.separator()
                # 1 - BOTTOM - LEFT
                pie.separator()
                # 3 - BOTTOM - RIGHT
                if bpy.context.object.mode == "EDIT":
                    box = pie.split()
                    column = box.column()
                    column.prop(toolsettings, "use_mesh_automerge", text="Auto Merge")
                else:
                    pie.separator()

            elif ob.object.type == 'EMPTY':
                pass

            elif ob.object.type == 'CURVE':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'ARMATURE':
                pie = layout.menu_pie()

                # 4 - LEFT
                pie.operator("object.editmode_toggle", text="Edit Mode", icon='OBJECT_DATAMODE')
                # 6 - RIGHT
                pie.operator("object.posemode_toggle", text="Pose", icon='POSE_HLT')
                # 2 - BOTTOM
                pie.separator()
                # 8 - TOP
                pie.operator("class.object", text="Object Mode", icon='OBJECT_DATAMODE')
                # 7 - TOP - LEFT
                pie.separator()
                # 9 - TOP - RIGHT
                pie.separator()
                # 1 - BOTTOM - LEFT
                pie.separator()
                # 3 - BOTTOM - RIGHT

            elif ob.object.type == 'FONT':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'SURFACE':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'META':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            elif ob.object.type == 'LATTICE':
                pie = layout.menu_pie()
                pie.operator("object.editmode_toggle", text="Edit/Object", icon='OBJECT_DATAMODE')

            else:
                pass


class PieLayoutSwitch(Menu):
    bl_idname = "pie.layout_swtich"
    bl_label = "Layout Switch"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("machin3.layout_switch", text="MACHIN3", icon='VIEW3D').variable="M3"
        # 6 - RIGHT
        pie.operator("machin3.layout_switch", text="Compositing", icon='NODETREE').variable="M3 compositing"
        # 2 - BOTTOM
        box = pie.split()
        column = box.column(align=True)
        column.operator("machin3.layout_switch", text="Animation", icon='ACTION_TWEAK').variable="M3 animation"
        column.operator("machin3.layout_switch", text="Drivers", icon='UI').variable="M3 drivers"
        # 8 - TOP
        pie.operator("machin3.layout_switch", text="Materials", icon='MATERIAL_DATA').variable="M3 materials"
        # 7 - TOP - LEFT
        pie.operator("machin3.layout_switch", text="UVs", icon='GROUP_UVS').variable="M3 UVs"
        # 9 - TOP - RIGHT
        pie.operator("machin3.layout_switch", text="Lighting", icon='IMAGE_COL').variable="M3 lighting"
        # box = pie.split()
        # row = box.row(align=True)
        # row.operator("machin3.layout_switch", text="Lighting", icon='IMAGE_COL').variable="M3 lighting"
        # row.operator("machin3.layout_switch", text="Baking", icon='MOD_UVPROJECT').variable="M3 baking"
        # 1 - BOTTOM - LEFT
        box = pie.split()
        row = box.row(align=True)
        row.operator("machin3.layout_switch", text="Scripting", icon='SCRIPT').variable="M3 scripting"
        row.operator("machin3.layout_switch", text="Console", icon='CONSOLE').variable="M3 console"
        # 3 - BOTTOM - RIGHT
        pie.operator("machin3.layout_switch", text="Video Editing", icon='RENDER_ANIMATION').variable="M3 video"


class SetFinal(bpy.types.Operator):
    bl_idname = "machin3.set_final"
    bl_label = "MACHIN3: Set Final"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("\nSetting up for Rendering ")

        context.scene.cycles.film_transparent = True
        print(" » turned ON transparancy")

        context.scene.render.layers["bg"].use = True
        print(" » turned ON render layer 'bg'")

        context.scene.render.use_compositing = True
        print(" » turned ON compositing")

        world = context.scene.world
        for node in world.node_tree.nodes:
            if node.type == "GROUP":
                if node.label == "environment":
                    blur = node.inputs['Blur']
                    blur.default_value = 0

                    print(" » turned OFF environment blur")
                    break

        context.scene.render.resolution_percentage = context.scene.machin3.final_percentage
        print(" » set render percentage to %d%%" % context.scene.machin3.final_percentage)

        bpy.context.scene.cycles.samples = context.scene.machin3.final_samples
        print(" » set cycles (render) samples to %d" % context.scene.machin3.final_samples)

        bpy.context.scene.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'
        bpy.context.scene.render.image_settings.color_depth = '32'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        print(" » set file format to Open EXR Multilayer, 32bit, RGBA")

        bpy.context.scene.cycles.device = 'CPU'
        print(" » set render device to CPU")

        return {'FINISHED'}


class SetPreview(bpy.types.Operator):
    bl_idname = "machin3.set_preview"
    bl_label = "MACHIN3: Set Preview"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("\nSetting up for Testing")

        context.scene.cycles.film_transparent = False
        print(" » turned OFF transparancy")

        context.scene.render.layers["bg"].use = False
        print(" » turned OFF render layer 'bg'")

        context.scene.render.use_compositing = False
        print(" » turned OFF compositing")

        world = context.scene.world
        for node in world.node_tree.nodes:
            if node.type == "GROUP":
                if node.label == "environment":
                    blur = node.inputs['Blur']
                    blur.default_value = 0.5

                    print(" » turned ON environment blur")
                    break

        context.scene.render.resolution_percentage = context.scene.machin3.preview_percentage
        print(" » set render percentage to %d%%" % context.scene.machin3.preview_percentage)

        bpy.context.scene.cycles.samples = context.scene.machin3.preview_samples
        print(" » set cycles (render) samples to %d" % context.scene.machin3.preview_samples)

        bpy.context.scene.cycles.device = 'GPU'
        print(" » set render device to GPU")

        return {'FINISHED'}


class PieViewsAndCams(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_views_and_cams"
    bl_label = "Views and Cams"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # ob = bpy.context.object
        # obj = context.object
        scene = context.scene
        view = context.space_data
        r3d = view.region_3d
        # rd = scene.render

        # align_active = bpy.context.scene.machin3.pieviewsalignactive

        # 4 - LEFT
        op = pie.operator("machin3.view_axis", text="Front")
        op.axis='FRONT'

        # 6 - RIGHT
        op = pie.operator("machin3.view_axis", text="Right")
        op.axis='RIGHT'
        # 2 - BOTTOM
        op = pie.operator("machin3.view_axis", text="Top")
        op.axis='TOP'
        # 8 - TOP

        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        column = b.column()
        self.draw_left_column(scene, view, column)

        b = box.box()
        column = b.column()
        self.draw_center_column(column)

        b = box.box()
        column = b.column()
        self.draw_right_column(view, r3d, column)


        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()


        """
        box = pie.split()
        column = box.column()
        column.scale_x = 0.8


        row = column.row()
        row.label("Resolution")
        row.prop(context.scene.machin3, "preview_percentage", text="")
        row.prop(context.scene.machin3, "final_percentage", text="")

        row = column.row()
        row.label("Samples")
        row.prop(context.scene.machin3, "preview_samples", text="")
        row.prop(context.scene.machin3, "final_samples", text="")

        row = column.row(align=True)
        row.label("Set")
        row.operator("machin3.set_preview", text="Preview")
        row.operator("machin3.set_final", text="Final")

        column.separator()
        column.operator("machin3.pack_images", text="Pack Images")
        column.separator()
        column.separator()
        column.separator()
        # """

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        pie.separator()

    def draw_left_column(self, scene, view, col):
        col.scale_x = 1.7

        col.prop(scene, "camera", text="Active")
        row = col.row(align=True)
        row.operator("view3d.view_camera", text="View Cam", icon='VISIBLE_IPO_ON')
        row.operator("view3d.camera_to_view", text="Cam to view", icon='MAN_TRANS')

        text, icon = ("Unlock Cam from View", "UNLOCKED") if view.lock_camera else ("Lock Camera to View", "LOCKED")
        col.operator("wm.context_toggle", text=text, icon=icon).data_path = "space_data.lock_camera"

    def draw_center_column(self, col):
        col.scale_y = 1.5
        op = col.operator("machin3.view_axis", text="Bottom")
        op.axis='BOTTOM'

        row = col.row(align=True)
        op = row.operator("machin3.view_axis", text="Left")
        op.axis='LEFT'

        op = row.operator("machin3.view_axis", text="Back")
        op.axis='BACK'

    def draw_right_column(self, view, r3d, col):
        text, icon = ("Orthographic", "MESH_CUBE") if r3d.is_perspective else ("Perspective", "VIEW3D")
        col.operator("view3d.view_persportho", text=text, icon=icon)
        col.prop(view, "lens")


class PieSnaping(Menu):
    bl_idname = "pie.snapping"
    bl_label = "Pie Snapping"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("snap.vertex", text="Vertex", icon='SNAP_VERTEX')
        #6 - RIGHT
        pie.operator("snap.face", text="Face", icon='SNAP_FACE')
        #2 - BOTTOM
        pie.operator("snap.edge", text="Edge", icon='SNAP_EDGE')
        #8 - TOP
        pie.prop(context.tool_settings, "use_snap", text="Snap On/Off")
        #7 - TOP - LEFT
        pie.operator("snap.volume", text="Volume", icon='SNAP_VOLUME')
        #9 - TOP - RIGHT
        if bpy.context.scene.tool_settings.snap_element != 'INCREMENT':
            pie.operator("snap.increment", text="Increment", icon='SNAP_INCREMENT')
        else:
            pie.prop(context.scene.tool_settings, "use_snap_grid_absolute")
        #1 - BOTTOM - LEFT
        pie.operator("snap.alignrotation", text="Align rotation", icon='SNAP_NORMAL')
        #3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="Snap Target", icon='SNAP_SURFACE').name="snap.targetmenu"


class SnapTargetMenu(Menu):
    bl_idname = "snap.targetmenu"
    bl_label = "Snap Target Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.snaptargetvariable", text="Active").variable='ACTIVE'
        #6 - RIGHT
        pie.operator("object.snaptargetvariable", text="Median").variable='MEDIAN'
        #2 - BOTTOM
        pie.operator("object.snaptargetvariable", text="Center").variable='CENTER'
        #8 - TOP
        pie.operator("object.snaptargetvariable", text="Closest").variable='CLOSEST'
        # 7 - TOP - LEFT
        # 9 - TOP - RIGHT
        # 1 - BOTTOM - LEFT
        # 3 - BOTTOM - RIGHT


class SwitchOrientation(bpy.types.Operator):
    bl_idname = "machin3.switch_orientation"
    bl_label = "MACHIN3: Switch Orientation"

    orientation = StringProperty()

    def execute(self, context):
        if self.orientation == 'NORMAL':
            bpy.context.space_data.transform_orientation=self.orientation
            bpy.context.space_data.show_manipulator = False
        elif self.orientation == 'LOCAL':
            bpy.context.space_data.transform_orientation=self.orientation
            bpy.context.space_data.show_manipulator = True
        elif self.orientation == 'VIEW':
            bpy.context.space_data.transform_orientation=self.orientation
            bpy.context.space_data.show_manipulator = True
        elif self.orientation == 'SELECTION':
            bpy.ops.transform.create_orientation(use=True)
            bpy.context.space_data.show_manipulator = True
        return {'FINISHED'}


class ChangePivot(bpy.types.Operator):
    bl_idname = "machin3.change_pivot"
    bl_label = "MACHIN3: Change Pivot"
    bl_options = {'REGISTER', 'UNDO'}

    pivot = StringProperty()

    def execute(self, context):
        bpy.context.space_data.pivot_point = self.pivot
        return {'FINISHED'}


class PieOrientationAndPivot(Menu):
    bl_idname = "pie.orientation_and_pivot"
    bl_label = "Pie Orientation and Pivot"

    def draw(self, context):
        mode = m3.get_mode()

        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        icon = "PROP_ON" if bpy.context.space_data.transform_orientation == 'NORMAL' else 'BLANK1'
        pie.operator("machin3.switch_orientation", text="Normal", icon=icon).orientation = 'NORMAL'
        # 6 - RIGHT
        icon = "PROP_ON" if bpy.context.space_data.transform_orientation == 'LOCAL' else 'BLANK1'
        pie.operator("machin3.switch_orientation", text="Local", icon=icon).orientation = 'LOCAL'
        # 2 - BOTTOM
        icon = "PROP_ON" if bpy.context.space_data.transform_orientation not in ['NORMAL', 'LOCAL', 'GLOBAL', 'VIEW', 'GIMBAL'] else 'BLANK1'
        pie.operator("machin3.switch_orientation", text=mode.capitalize(), icon=icon).orientation = 'SELECTION'
        # 8 - TOP
        column = pie.column()
        column.prop(bpy.context.space_data, "show_manipulator")
        if mode =="OBJECT":
            column.prop(bpy.context.scene.tool_settings, "use_proportional_edit_objects", text="Proportional Editing")
            if bpy.context.scene.tool_settings.use_proportional_edit_objects:
                column.prop(bpy.context.scene.tool_settings, "proportional_edit_falloff")
        else:
            column.prop(bpy.context.scene.tool_settings, "proportional_edit")
        icon = "PROP_ON" if bpy.context.space_data.transform_orientation == 'VIEW' else 'BLANK1'
        column.operator("machin3.switch_orientation", text="View", icon=icon).orientation = 'VIEW'

        # 7 - TOP - LEFT
        column = pie.column()
        column.scale_y = 1.5
        icon = "SPACE3" if bpy.context.space_data.pivot_point == 'INDIVIDUAL_ORIGINS' else 'BLANK1'
        column.operator("machin3.change_pivot", text="Individual", icon=icon).pivot = 'INDIVIDUAL_ORIGINS'
        # 9 - TOP - RIGHT
        column = pie.column()
        column.scale_y = 1.5
        icon = "SPACE3" if bpy.context.space_data.pivot_point == 'ACTIVE_ELEMENT' else 'BLANK1'
        column.operator("machin3.change_pivot", text="Active", icon=icon).pivot = 'ACTIVE_ELEMENT'
        # 1 - BOTTOM - LEFT
        column = pie.column()
        column.scale_y = 1.5
        icon = "SPACE3" if bpy.context.space_data.pivot_point == 'MEDIAN_POINT' else 'BLANK1'
        column.operator("machin3.change_pivot", text="Median", icon=icon).pivot = 'MEDIAN_POINT'
        # 3 - BOTTOM - RIGHT
        column = pie.column()
        column.scale_y = 1.5
        icon = "SPACE3" if bpy.context.space_data.pivot_point == 'CURSOR' else 'BLANK1'
        column.operator("machin3.change_pivot", text="Cursor", icon=icon).pivot = 'CURSOR'


class AOPreset(bpy.types.Operator):
    bl_idname = "machin3.ao_preset"
    bl_label = "MACHIN3: AO Preset"

    strength = FloatProperty()

    def execute(self, context):
        fx_settings = context.space_data.fx_settings
        if self.strength !=0:
            fx_settings.use_ssao = True
            fx_settings.ssao.factor = self.strength
        else:
            if fx_settings.use_ssao:
                fx_settings.use_ssao = False
            else:
                fx_settings.use_ssao = True

        return {'FINISHED'}


class PieChangeShading(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_change_shading"
    bl_label = "Change Shading"

    def draw(self, context):
        layout = self.layout

        view = context.space_data


        pie = layout.menu_pie()

        # 4 - LEFT
        text, icon = self.get_text_icon(context, "SOLID")
        pie.operator("machin3.shade_solid", text=text, icon=icon)

        # 6 - RIGHT
        text, icon = self.get_text_icon(context, "MATERIAL")
        pie.operator("machin3.shade_material", text=text, icon=icon)

        # 2 - BOTTOM
        text, icon = self.get_text_icon(context, "RENDERED")
        pie.operator("machin3.shade_rendered", text=text, icon=icon)

        # 8 - TOP
        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        column = b.column()
        self.draw_left_column(context, view, column)

        b = box.box()
        column = b.column()
        self.draw_center_column(view, column)

        b = box.box()
        column = b.column()
        self.draw_right_column(context, view, column)

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        pie.separator()

        # 3 - BOTTOM - RIGHT
        pie.separator()

    def draw_left_column(self, context, view, col):
        row = col.split(percentage=0.45)
        row.operator("machin3.toggle_grid", text="Grid Toggle", icon="GRID")
        r = row.split().row(align=True)
        r.active = view.overlay.show_floor
        r.prop(view.overlay, "show_axis_x", text="X", toggle=True)
        r.prop(view.overlay, "show_axis_y", text="Y", toggle=True)
        r.prop(view.overlay, "show_axis_z", text="Z", toggle=True)

        # col.separator()
        row = col.split(percentage=0.45)
        row.operator("machin3.toggle_wireframe", text="Wire Toggle", icon="WIRE")
        r = row.split().row()
        if context.mode == "OBJECT":
            r.active = view.overlay.show_wireframes
            r.prop(view.overlay, "wireframe_threshold", text="Wireframe")
        elif context.mode == "EDIT_MESH":
            r.active = view.shading.show_xray
            r.prop(view.shading, "xray_alpha", text="X-Ray")

        row = col.split(percentage=0.45)
        row.operator("machin3.toggle_outline", text="(Q) Outline Toggle")
        row.prop(view.shading, "object_outline_color", text="")

        active = context.active_object
        if active:
            if active.type == "MESH":
                mesh = active.data

                col.separator()
                row = col.split(percentage=0.55)
                r = row.split().row(align=True)
                r.operator("machin3.shade_smooth", text="Smooth", icon="MATSPHERE")
                r.operator("machin3.shade_flat", text="Flat", icon="MATCUBE")
                row.prop(mesh, "use_auto_smooth")
                if mesh.use_auto_smooth:
                    if mesh.has_custom_normals:
                        col.operator("mesh.customdata_custom_splitnormals_clear", text="Clear Custom Normals")
                    else:
                        col.prop(mesh, "auto_smooth_angle")

                if context.mode == "EDIT_MESH":
                    row = col.row(align=True)
                    row.prop(view.overlay, "show_vertex_normals", text="", icon='VERTEXSEL')
                    row.prop(view.overlay, "show_split_normals", text="", icon='LOOPSEL')
                    row.prop(view.overlay, "show_face_normals", text="", icon='FACESEL')

                    r = row.row(align=True)
                    r.active = view.overlay.show_vertex_normals or view.overlay.show_face_normals or view.overlay.show_split_normals
                    r.prop(view.overlay, "normals_length", text="Size")


        if context.mode == "EDIT_MESH":
            col.separator()
            # row = col.row()
            # row.prop(mesh, "show_edges", text="Edges")
            # row.prop(mesh, "show_faces", text="Faces")

            row = col.row(align=True)
            row.prop(mesh, "show_edge_crease", text="Creases", toggle=True)
            row.prop(mesh, "show_edge_sharp", text="Sharp", toggle=True)
            row.prop(mesh, "show_edge_bevel_weight", text="Bevel", toggle=True)

            if not bpy.app.build_options.freestyle:
                row.prop(mesh, "show_edge_seams", text="Seams", toggle=True)

    def draw_center_column(self, view, col):
        row = col.split(percentage=0.42)
        row.prop(view.overlay, "show_cursor", text="3D Cursor")
        r = row.split().row(align=True)
        r.prop(view.overlay, "show_object_origins", text="Origins")
        r.prop(view.overlay, "show_object_origins_all", text="All")

        col.separator()
        row = col.row()
        row.prop(view.overlay, "show_backface_culling")
        row.prop(view.overlay, "show_face_orientation")
        col.prop(view.overlay, "show_relationship_lines")

    def draw_right_column(self, context, view, col):
        if view.shading.type == "SOLID":

            # light type
            row = col.row(align=True)
            row.scale_y = 1.5
            row.prop(view.shading, "light", expand=True)
            if view.shading.light == "MATCAP":
                row.operator('VIEW3D_OT_toggle_matcap_flip', text="", icon='ARROW_LEFTRIGHT')

            # studio / matcap selection
            if view.shading.light in ["STUDIO", "MATCAP"]:
                row = col.row()
                row.scale_y = 0.6
                row.template_icon_view(view.shading, "studio_light", show_labels=True, scale=3)

            # color type
            row = col.row(align=True)
            row.prop(view.shading, "color_type", expand=True)

            # single color
            if view.shading.color_type == 'SINGLE':
                col.prop(view.shading, "single_color", text="")
            elif view.shading.color_type == 'MATERIAL':
                col.operator("machin3.colorize_materials", icon='MATERIAL')

        elif view.shading.type == "MATERIAL":

            # use scene lights and world
            studio_worlds = [w for w in context.user_preferences.studio_lights if "datafiles/studiolights/world" in w.path]

            if any([bpy.data.lights, studio_worlds]):
                row = col.row()
                if bpy.data.lights:
                    row.prop(view.shading, "use_scene_lights")

                if studio_worlds:
                    row.prop(view.shading, "use_scene_world")

                    # world hdri selection and manipulation
                    if not view.shading.use_scene_world:
                            row = col.row()
                            row.scale_y = 0.6
                            row.template_icon_view(view.shading, "studio_light")

                            col.prop(view.shading, "studiolight_rotate_z", text="Rotation")
                            col.prop(view.shading, "studiolight_background_alpha")

            # world background node props

            if view.shading.use_scene_world or not studio_worlds:
                if context.scene.world:
                    tree = context.scene.world.node_tree
                    output = tree.nodes.get("World Output")

                    if output:
                        input_surf = output.inputs.get("Surface")

                        if input_surf:
                            if input_surf.links:
                                node = input_surf.links[0].from_node

                                if node.type == "BACKGROUND":
                                    color = node.inputs['Color']
                                    strength = node.inputs['Strength']

                                    if color.links:
                                        col.prop(strength, "default_value", text="Background Strength")
                                    else:
                                        row = col.split(percentage=0.7)
                                        row.prop(strength, "default_value", text="Background Strength")
                                        row.prop(color, "default_value", text="")

                                    col.separator()

            # eevee settings
            icon = "TRIA_DOWN" if context.scene.eevee.use_ssr else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_ssr", icon=icon)
            if context.scene.eevee.use_ssr:
                col.prop(context.scene.eevee, "ssr_thickness")

            icon = "TRIA_DOWN" if context.scene.eevee.use_gtao else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_gtao", icon=icon)
            if context.scene.eevee.use_gtao:
                row = col.row(align=True)
                row.prop(context.scene.eevee, "gtao_distance")
                row.prop(context.scene.eevee, "gtao_factor")

            icon = "TRIA_DOWN" if context.scene.eevee.use_bloom else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_bloom", icon=icon)
            if context.scene.eevee.use_bloom:
                row = col.row(align=True)
                row.prop(context.scene.eevee, "bloom_threshold")
                row.prop(context.scene.eevee, "bloom_radius")

            icon = "TRIA_DOWN" if context.scene.eevee.use_volumetric else "TRIA_RIGHT"
            col.prop(context.scene.eevee, "use_volumetric", icon=icon)
            if context.scene.eevee.use_volumetric:
                row = col.row(align=True)
                row.prop(context.scene.eevee, "volumetric_start")
                row.prop(context.scene.eevee, "volumetric_end")

    def get_text_icon(self, context, shading):
        if context.space_data.shading.type == shading:
            text = "Toggle Overlays"
            icon = "WIRE"
        else:
            if shading == "SOLID":
                text = "Solid"
                icon = "SOLID"
            elif shading == "MATERIAL":
                text = "LookDev"
                icon = "MATERIAL"
            elif shading == "RENDERED":
                text = "Rendered"
                icon = "SMOOTH"

        return text, icon


class PieAlign(Menu):
    bl_idname = "pie.align"
    bl_label = "Pie Align"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("align.x", text="Align X", icon='TRIA_LEFT')
        # 6 - RIGHT
        pie.operator("align.z", text="Align Z", icon='TRIA_DOWN')
        # 2 - BOTTOM
        pie.operator("align.y", text="Align Y", icon='PLUS')
        # 8 - TOP
        pie.operator("align.2y0", text="Align To Y-0")
        # 7 - TOP - LEFT
        pie.operator("align.2x0", text="Align To X-0")
        # 9 - TOP - RIGHT
        pie.operator("align.2z0", text="Align To Z-0")
        # 1 - BOTTOM - LEFT
        # pie.menu("align.xyz")
        box = pie.split().box().column()
        box.label("Align :")
        row = box.row(align=True)
        row.label("X")
        row.operator("alignx.left", text="Neg")
        row.operator("alignx.right", text="Pos")
        row = box.row(align=True)
        row.label("Y")
        row.operator("aligny.front", text="Neg")
        row.operator("aligny.back", text="Pos")
        row = box.row(align=True)
        row.label("Z")
        row.operator("alignz.bottom", text="Neg")
        row.operator("alignz.top", text="Pos")
        # 3 - BOTTOM - RIGHT
        if m3.addon_check("rRMB"):
            column = pie.column()
            column.scale_y = 1.5
            column.operator("object.ralign_orientation_to_selection")
            column.operator("object.ralign_and_move_origin_to_selection")
        else:
            pie.separator()



class PieSaveOpenAppend(Menu):
    bl_idname = "VIEW3D_MT_MACHIN3_save_open_append"
    bl_label = "Save, Open, Append"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # 4 - LEFT
        pie.operator("wm.open_mainfile", text="Open file", icon='FILE_FOLDER')

        # 6 - RIGHT
        pie.operator("wm.save_as_mainfile", text="Save As...", icon='SAVE_AS')

        # 2 - BOTTOM

        pie.operator("machin3.save", text="Save", icon='FILE_TICK')

        # 8 - TOP
        box = pie.split()
        # box = pie.box().split()

        b = box.box()
        column = b.column()
        self.draw_left_column(column)

        b = box.box()
        column = b.column()
        self.draw_center_column(column)

        b = box.box()
        column = b.column()
        self.draw_right_column(column)

        # 7 - TOP - LEFT
        pie.separator()

        # 9 - TOP - RIGHT
        pie.separator()

        # 1 - BOTTOM - LEFT
        pie.operator("wm.read_homefile", text="New", icon='NEW')

        # 3 - BOTTOM - RIGHT
        pie.operator("machin3.save_incremental", text="Incremental Save", icon='SAVE_COPY')

    def draw_left_column(self, col):
        col.scale_x = 1.1

        row = col.row()
        row.scale_y = 1.5
        row.operator("machin3.load_most_recent", text="(R) Most Recent", icon='FILE_FOLDER')
        row.operator("wm.call_menu", text="All Recent", icon='FILE_FOLDER').name = "INFO_MT_file_open_recent"

        col.separator()
        col.operator("wm.recover_auto_save", text="Recover Auto Save...", icon='RECOVER_AUTO')
        # col.operator("wm.recover_last_session", text="Recover Last Session", icon='RECOVER_LAST')
        col.operator("wm.revert_mainfile", text="Revert", icon='FILE_REFRESH')

    def draw_center_column(self, col):
        row = col.split(percentage=0.25)
        row.label("Alembic")
        r = row.row(align=True)
        r.operator("wm.alembic_import", text="Import", icon='IMPORT')
        r.operator("wm.alembic_export", text="Export", icon='EXPORT')

        row = col.split(percentage=0.25)
        row.label("Collada")
        r = row.row(align=True)
        r.operator("wm.collada_import", text="Import", icon='IMPORT')
        r.operator("wm.collada_export", text="Export", icon='EXPORT')

    def draw_right_column(self, col):
        row = col.row()
        r = row.row(align=True)
        r.operator("wm.link", text="Link", icon='LINK_BLEND')
        r.operator("wm.append", text="Append", icon='APPEND_BLEND')
        row.operator("wm.call_menu", text="", icon='EXTERNAL_DATA').name = "INFO_MT_file_external_data"


        # append world and materials

        appendworldpath = m3.M3_prefs().appendworldpath
        appendmatspath = m3.M3_prefs().appendmatspath

        if any([appendworldpath, appendmatspath]):
            col.separator()

            if appendworldpath:
                row = col.split(percentage=0.8)
                row.scale_y = 1.5
                row.operator("machin3.append_world", text="World", icon='WORLD')
                row.operator("machin3.load_world_source", text="", icon='FILE_FOLDER')

            if appendmatspath:
                row = col.split(percentage=0.8)
                row.scale_y = 1.5
                row.operator("wm.call_menu", text="Material", icon='MATERIAL').name = "VIEW3D_MT_MACHIN3_append_materials"
                row.operator("machin3.load_materials_source", text="", icon='FILE_FOLDER')


class PIE_IMAGE_MT_uvs_select_mode(Menu):
    bl_label = "UV Select Mode"
    bl_idname = "pie.uvsselectmode"

    def draw(self, context):
        layout = self.layout

        layout.operator_context = 'INVOKE_REGION_WIN'
        toolsettings = context.tool_settings
        pie = layout.menu_pie()
        # do smart things depending on whether uv_select_sync is on

        if toolsettings.use_uv_select_sync:

            props = pie.operator("wm.context_set_value", text="Vertex", icon='VERTEXSEL')
            props.value = "(True, False, False)"
            props.data_path = "tool_settings.mesh_select_mode"

            props = pie.operator("wm.context_set_value", text="Face", icon='FACESEL')
            props.value = "(False, False, True)"
            props.data_path = "tool_settings.mesh_select_mode"

            props = pie.operator("wm.context_set_value", text="Edge", icon='EDGESEL')
            props.value = "(False, True, False)"
            props.data_path = "tool_settings.mesh_select_mode"

        else:
            props = pie.operator("wm.context_set_string", text="Vertex", icon='UV_VERTEXSEL')
            props.value = 'VERTEX'
            props.data_path = "tool_settings.uv_select_mode"

            props = pie.operator("wm.context_set_string", text="Face", icon='UV_FACESEL')
            props.value = 'FACE'
            props.data_path = "tool_settings.uv_select_mode"

            props = pie.operator("wm.context_set_string", text="Edge", icon='UV_EDGESEL')
            props.value = 'EDGE'
            props.data_path = "tool_settings.uv_select_mode"

            props = pie.operator("wm.context_set_string", text="Island", icon='UV_ISLANDSEL')
            props.value = 'ISLAND'
            props.data_path = "tool_settings.uv_select_mode"
