bl_info = {
    "name": "BatchRUV",
    "author": "Ben",
    "version": (0, 1),
    "blender": (3, 2, 1),
    "location": "View3D - Sidebar",
    "description": "Batch Rename Selected Objects and UVs, Batch Active UV Slots",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import os
import bpy

os.system("cls")
print(os.getcwd())
print("Data Filepath: ", bpy.data.filepath)

tog_uv = True

class Input_Properties(bpy.types.PropertyGroup):
    objs_name : bpy.props.StringProperty(name="", description="Batch_Objects_Name", maxlen=24, default="NewName")
    uv0_name : bpy.props.StringProperty(name="", description="UV0_Name", maxlen=10, default="UV0")
    uv1_name : bpy.props.StringProperty(name="", description="UV0_Name", maxlen=10, default="UV1")
    grid_vec : bpy.props.IntVectorProperty(name="", description="Grid Vector", default=(2,2,1), min=1, soft_max=32)
    
class Renamer_UV(bpy.types.Panel):
    bl_label = "BatchRUV"
    bl_idname = "RENAMER_PT_RenamerUV"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BatchRUV"
    
    def draw(self, context):
        layout = self.layout        
        scene = context.scene
        renamerprop = scene.renamer_props
        
        row=layout.row()
        row.label(text="Batch Objects Name:")
        row=layout.row()
        row.prop(renamerprop, 'objs_name', icon='OBJECT_DATA')
        row=layout.row()
        
        row.label(text="UV Names:")
        split = layout.split(align=True, factor = 0.4)
        col = split.column()
        col.scale_y = 1.0          
        col.label(text='Slot Name 1:')
        col.label(text='Slot Name 2:')
        
        col = split.column(align=True)
        
        col.prop(renamerprop, 'uv0_name')
        col.prop(renamerprop, 'uv1_name')
        
        row=layout.row()
        row.label(text="")
        row.scale_y = 0.1
        row=layout.row()
        
        row.label(text='Batch UV Slot Selection:')
        row=layout.row(align=False)
        if tog_uv == True:
            row.operator('batch_rename.btn_uv0', text=renamerprop.uv0_name, icon='GROUP_UVS', depress=True)
            row.operator('batch_rename.btn_uv1', text=renamerprop.uv1_name, icon='GROUP_UVS')
        else:
            row.operator('batch_rename.btn_uv0', text=renamerprop.uv0_name, icon='GROUP_UVS')
            row.operator('batch_rename.btn_uv1', text=renamerprop.uv1_name, icon='GROUP_UVS', depress=True)
        row=layout.row()
        row.label(text="")
        row.scale_y = 0.5
        row=layout.row()
        row.operator('batch_rename.btn_rename', icon='FILE_REFRESH')
        row.scale_y = 1.5

class BATCHRUV_OT_btn_uv0(bpy.types.Operator):
    """UV Slot 0"""
    bl_label = "slot0"
    bl_idname = 'batch_rename.btn_uv0'
    #bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        renamerprop = context.scene.renamer_props
        sel_objs = bpy.context.selected_objects
        global tog_uv
        tog_uv = True
        for obj in sel_objs:
            obj.data.uv_layers.active_index = 0
            obj.data.uv_layers.active.name = renamerprop.uv0_name      
        return {'FINISHED'}
    
class BATCHRUV_OT_btn_uv1(bpy.types.Operator):
    """UV Slot 1"""
    bl_label = "slot1"
    bl_idname = 'batch_rename.btn_uv1'
    #bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        renamerprop = context.scene.renamer_props
        sel_objs = bpy.context.selected_objects
        global tog_uv
        tog_uv = False
        for obj in sel_objs:
            obj.data.uv_layers.active_index = 1
            obj.data.uv_layers.active.name = renamerprop.uv1_name
        return {'FINISHED'}
    
class BATCHRUV_OT_btn_rename(bpy.types.Operator):
    """Batch Rename"""
    bl_label = "Batch Rename"
    bl_idname = 'batch_rename.btn_rename'
    #bl_options = {'REGISTER', 'UNDO'}   
    def execute(self, context):
        renamerprop = context.scene.renamer_props
        sel_objs = bpy.context.selected_objects
        new_name = renamerprop.objs_name
        obj_list = []

        for obj in sel_objs:
            obj_list.append(obj.name)
            obj.name = new_name
            obj.data.name = new_name

        print(str(len(obj_list)) + " object names were changed to " + "'" + new_name + "'")
        obj_list = []       
        return {'FINISHED'}

classes = [Input_Properties,
            Renamer_UV,
            BATCHRUV_OT_btn_rename,
            BATCHRUV_OT_btn_uv0,
            BATCHRUV_OT_btn_uv1,
            ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)        
        bpy.types.Scene.renamer_props = bpy.props.PointerProperty(type = Input_Properties)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
        del bpy.types.Scene.input_props
        
if __name__ == '__main__':
    register()
