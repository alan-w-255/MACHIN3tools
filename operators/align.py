import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from mathutils import Matrix, Vector, Euler
from math import radians
from .. utils.math import get_loc_matrix, get_rot_matrix, get_sca_matrix


modeitems = [('ORIGIN', 'Origin', ''),
             ('CURSOR', 'Cursor', ''),
             ('ACTIVE', 'Active', ''),
             ('FLOOR', 'Floor', '')]


class Align(bpy.types.Operator):
    bl_idname = 'machin3.align'
    bl_label = 'MACHIN3: Align'
    bl_options = {'REGISTER', 'UNDO'}

    mode: EnumProperty(name='Mode', items=modeitems, default='ACTIVE')

    location: BoolProperty(name='Align Location', default=True)
    rotation: BoolProperty(name='Align Rotation', default=True)
    scale: BoolProperty(name='Align Scale', default=False)

    loc_x: BoolProperty(name='X', default=True)
    loc_y: BoolProperty(name='Y', default=True)
    loc_z: BoolProperty(name='Z', default=True)

    rot_x: BoolProperty(name='X', default=True)
    rot_y: BoolProperty(name='Y', default=True)
    rot_z: BoolProperty(name='Z', default=True)

    sca_x: BoolProperty(name='X', default=True)
    sca_y: BoolProperty(name='Y', default=True)
    sca_z: BoolProperty(name='Z', default=True)

    parent_to_bone: BoolProperty(name='Parent to Bone', default=True)
    align_z_to_y: BoolProperty(name='Align Z to Y', default=True)
    roll: BoolProperty(name='Roll', default=False)
    roll_amount: FloatProperty(name='Roll Amount in Degrees', default=90)

    def draw(self, context):
        layout = self.layout

        column = layout.column()

        row = column.split(factor=0.3)
        row.label(text='Align to', icon='BONE_DATA' if self.mode == 'ACTIVE' and context.active_bone else 'BLANK1')
        r = row.row()
        r.prop(self, 'mode', expand=True)

        if self.mode == 'ACTIVE' and context.active_bone:
            row = column.split(factor=0.3)
            row.label(text='Parent to Bone')
            row.prop(self, 'parent_to_bone', text='True' if self.parent_to_bone else 'False', toggle=True)

            row = column.split(factor=0.3)
            row.label(text='Align Z to Y')
            row.prop(self, 'align_z_to_y', text='True' if self.align_z_to_y else 'False', toggle=True)

            row = column.split(factor=0.3)
            row.prop(self, 'roll', text='Roll')

            r = row.row(align=True)
            r.active = self.roll
            r.prop(self, 'roll_amount', text='')

        else:
            if self.mode in ['ORIGIN', 'CURSOR', 'ACTIVE']:
                row = column.split(factor=0.3)
                row.prop(self, 'location', text='Location')

                r = row.row(align=True)
                r.active = self.location
                r.prop(self, 'loc_x', toggle=True)
                r.prop(self, 'loc_y', toggle=True)
                r.prop(self, 'loc_z', toggle=True)

            if self.mode in ['CURSOR', 'ACTIVE']:
                row = column.split(factor=0.3)
                row.prop(self, 'rotation', text='Rotation')

                r = row.row(align=True)
                r.active = self.rotation
                r.prop(self, 'rot_x', toggle=True)
                r.prop(self, 'rot_y', toggle=True)
                r.prop(self, 'rot_z', toggle=True)

            if self.mode == 'ACTIVE':
                row = column.split(factor=0.3)
                row.prop(self, 'scale', text='Scale')

                r = row.row(align=True)
                r.active = self.scale
                r.prop(self, 'sca_x', toggle=True)
                r.prop(self, 'sca_y', toggle=True)
                r.prop(self, 'sca_z', toggle=True)

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode in ['OBJECT', 'POSE']

    def execute(self, context):
        sel = context.selected_objects

        if self.mode == 'ORIGIN':
            self.align_to_origin(sel)

        if self.mode == 'CURSOR':
            self.align_to_cursor(context.scene.cursor, sel)

        elif self.mode == 'ACTIVE':
            active = context.active_object

            if active in sel:
                sel.remove(active)

                if context.active_bone:
                    self.align_to_active_bone(active, context.active_bone.name, sel)

                else:
                    self.align_to_active_object(active, sel)


        elif self.mode == 'FLOOR':
            # for some reason a dg is neccessary, in a fresh startup scene, when running clear location followed for floor alignment
            # not for the other alignment types however, and only once at the very beginning at the start of the scene editing
            context.evaluated_depsgraph_get()
            self.drop_to_floor(sel)

        return {'FINISHED'}

    def align_to_origin(self, sel):
        for obj in sel:
            # get object matrix and decompose
            omx = obj.matrix_world
            oloc, orot, osca = omx.decompose()

            # split components into x,y,z axis elements
            olocx, olocy, olocz = oloc
            orotx, oroty, orotz = orot.to_euler('XYZ')
            oscax, oscay, oscaz = osca

            # TRANSLATION

            # if location is aligned, pick the axis elements based on the loc axis props
            if self.location:
                locx = 0 if self.loc_x else olocx
                locy = 0 if self.loc_y else olocy
                locz = 0 if self.loc_z else olocz

                # re-assemble into translation matrix
                loc = get_loc_matrix(Vector((locx, locy, locz)))

            # otherwise, just use the object's location component
            else:
                loc = get_loc_matrix(oloc)


            # ROTATION

            rot = orot.to_matrix().to_4x4()


            # SCALE

            sca = get_sca_matrix(osca)


            # re-combine components into world matrix
            obj.matrix_world = loc @ rot @ sca

    def align_to_cursor(self, cursor, sel):
        cursor.rotation_mode = 'XYZ'

        for obj in sel:
            # get object matrix and decompose
            omx = obj.matrix_world
            oloc, orot, osca = omx.decompose()

            # split components into x,y,z axis elements
            olocx, olocy, olocz = oloc
            orotx, oroty, orotz = orot.to_euler('XYZ')
            oscax, oscay, oscaz = osca

            # TRANSLATION

            # if location is aligned, pick the axis elements based on the loc axis props
            if self.location:
                locx = cursor.location.x if self.loc_x else olocx
                locy = cursor.location.y if self.loc_y else olocy
                locz = cursor.location.z if self.loc_z else olocz

                # re-assemble into translation matrix
                loc = get_loc_matrix(Vector((locx, locy, locz)))

            # otherwise, just use the object's location component
            else:
                loc = get_loc_matrix(oloc)


            # ROTATION

            # if rotation is aligned, pick the axis elements based on the rot axis props
            if self.rotation:
                rotx = cursor.rotation_euler.x if self.rot_x else orotx
                roty = cursor.rotation_euler.y if self.rot_y else oroty
                rotz = cursor.rotation_euler.z if self.rot_z else orotz

                # re-assemble into rotation matrix
                rot = get_rot_matrix(Euler((rotx, roty, rotz), 'XYZ'))

            # otherwise, just use the object's rotation component
            else:
                rot = get_rot_matrix(orot)


            # SCALE

            sca = get_sca_matrix(osca)


            # re-combine components into world matrix
            obj.matrix_world = loc @ rot @ sca

    def align_to_active_object(self, active, sel):
        # get target matrix and decompose
        amx = active.matrix_world
        aloc, arot, asca = amx.decompose()

        # split components into x,y,z axis elements
        alocx, alocy, alocz = aloc
        arotx, aroty, arotz = arot.to_euler('XYZ')
        ascax, ascay, ascaz = asca

        for obj in sel:
            # get object matrix and decompose
            omx = obj.matrix_world
            oloc, orot, osca = omx.decompose()

            # split components into x,y,z axis elements
            olocx, olocy, olocz = oloc
            orotx, oroty, orotz = orot.to_euler('XYZ')
            oscax, oscay, oscaz = osca

            # TRANSLATION

            # if location is aligned, pick the axis elements based on the loc axis props
            if self.location:
                locx = alocx if self.loc_x else olocx
                locy = alocy if self.loc_y else olocy
                locz = alocz if self.loc_z else olocz

                # re-assemble into translation matrix
                loc = get_loc_matrix(Vector((locx, locy, locz)))

            # otherwise, just use the object's location component
            else:
                loc = get_loc_matrix(oloc)


            # ROTATION

            # if rotation is aligned, pick the axis elements based on the rot axis props
            if self.rotation:
                rotx = arotx if self.rot_x else orotx
                roty = aroty if self.rot_y else oroty
                rotz = arotz if self.rot_z else orotz

                # re-assemble into rotation matrix
                rot = get_rot_matrix(Euler((rotx, roty, rotz), 'XYZ'))

            # otherwise, just use the object's rotation component
            else:
                rot = get_rot_matrix(orot)


            # SCALE

            # if scale is aligned, pick the axis elements based on the sca axis props
            if self.scale:
                scax = ascax if self.sca_x else oscax
                scay = ascay if self.sca_y else oscay
                scaz = ascaz if self.sca_z else oscaz

                # re-assemble into scale matrix
                sca = get_sca_matrix(Vector((scax, scay, scaz)))

            # otherwise, just use the object's scale component
            else:
                sca = get_sca_matrix(osca)


            # re-combine components into world matrix
            obj.matrix_world = loc @ rot @ sca

    def align_to_active_bone(self, armature, bonename, sel):
        bone = armature.pose.bones[bonename]

        for obj in sel:
            if self.parent_to_bone:
                obj.parent = armature
                obj.parent_type = 'BONE'
                obj.parent_bone = bonename

            if self.align_z_to_y:
                obj.matrix_world = armature.matrix_world @ bone.matrix @ Matrix.Rotation(radians(-90), 4, 'X') @ Matrix.Rotation(radians(self.roll_amount if self.roll else 0), 4, 'Z')
            else:
                obj.matrix_world = armature.matrix_world @ bone.matrix @ Matrix.Rotation(radians(self.roll_amount if self.roll else 0), 4, 'Y')

    def drop_to_floor(self, selection):
        for obj in selection:
            mx = obj.matrix_world

            if obj.type == 'MESH':
                minz = min((mx @ v.co)[2] for v in obj.data.vertices)

                mx.translation.z -= minz

            elif obj.type == 'EMPTY':
                mx.translation.z -= obj.location.z
