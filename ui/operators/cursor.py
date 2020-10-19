import bpy
import bmesh
from ... utils.math import get_center_between_verts, average_locations, create_rotation_matrix_from_vertex, create_rotation_matrix_from_edge, create_rotation_matrix_from_face
from ... utils.scene import set_cursor
from ... utils.ui import popup_message
from ... utils.draw import draw_vector, draw_point


class CursorToOrigin(bpy.types.Operator):
    bl_idname = "machin3.cursor_to_origin"
    bl_label = "MACHIN3: Cursor to Origin"
    bl_description = "Reset Cursor location and rotation to world origin"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_cursor()
        return {'FINISHED'}


class CursorToSelected(bpy.types.Operator):
    bl_idname = "machin3.cursor_to_selected"
    bl_label = "MACHIN3: Cursor to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def description(cls, context, properties):
        if context.mode == 'OBJECT':
            return "Align Cursor with Selected Object(s)\nALT: Only set Cursor Location\nCTRL: Only set Cursor Rotation"

        elif context.mode == 'EDIT_MESH':
            return "Align Cursor with Vert/Edge/Face\nALT: Only set Cursor Location\nCTRL: Only set Cursor Rotation"

    @classmethod
    def poll(cls, context):
        if context.mode == 'EDIT_MESH' and tuple(context.scene.tool_settings.mesh_select_mode) in [(True, False, False), (False, True, False), (False, False, True)]:
            bm = bmesh.from_edit_mesh(context.active_object.data)
            return [v for v in bm.verts if v.select]
        return context.active_object or context.selected_objects

    def invoke(self, context, event):
        active = context.active_object
        sel = [obj for obj in context.selected_objects if obj != active]

        # make sure there is an active
        if sel and not active:
            context.view_layer.objects.active = sel[0]
            sel.remove(active)

        # if in object mode with multiple selected ojects, pass it on to Blender's op
        if context.mode == 'OBJECT' and active and not sel:
            self.cursor_to_active_object(active, only_location=event.alt, only_rotation=event.ctrl)
            return {'FINISHED'}

        elif context.mode == 'EDIT_MESH':
            if event.alt and event.ctrl:
                popup_message("Hold down ATL, CTRL or neither, not both!", title="Invalid Modifier Keys")

            self.cursor_to_editmesh(context, active, only_location=event.alt, only_rotation=event.ctrl)
            return {'FINISHED'}

        # fall back for cases not covered above
        bpy.ops.view3d.snap_cursor_to_selected()

        return {'FINISHED'}

    def cursor_to_editmesh(self, context, active, only_location, only_rotation):
        bm = bmesh.from_edit_mesh(active.data)
        mx = active.matrix_world

        if tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (True, False, False):
            verts = [v for v in bm.verts if v.select]

            co = average_locations([v.co for v in verts])

            # create vertex world matrix components
            if not only_rotation:
                loc = mx @ co

            if not only_location:
                v = bm.select_history[-1] if bm.select_history else verts[0]
                rot = create_rotation_matrix_from_vertex(active, v)

        elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, True, False):
            edges = [e for e in bm.edges if e.select]
            center = average_locations([get_center_between_verts(*e.verts) for e in edges])

            # create edge world matrix components
            if not only_rotation:
                loc = mx @ center

            if not only_location:
                e = bm.select_history[-1] if bm.select_history else edges[0]
                rot = create_rotation_matrix_from_edge(active, e)

        elif tuple(bpy.context.scene.tool_settings.mesh_select_mode) == (False, False, True):
            faces = [f for f in bm.faces if f.select]

            center = average_locations([f.calc_center_median_weighted() for f in faces])

            # create face world matrix components
            if not only_rotation:
                loc = mx @ center

            if not only_location:
                f = bm.faces.active if bm.faces.active and bm.faces.active in faces else faces[0]
                rot = create_rotation_matrix_from_face(mx, f)

        # set the cursor location/rotation
        set_cursor(None if only_rotation else loc, None if only_location else rot.to_quaternion())

        context.area.tag_redraw()


    def cursor_to_active_object(self, active, only_location, only_rotation):
        mx = active.matrix_world
        loc, rot, _ = mx.decompose()

        set_cursor(None if only_rotation else loc, None if only_location else rot)
