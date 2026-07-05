import bpy
import mathutils

def slice_object_by_exact_2mm_final():
    # 選択されたアクティブオブジェクトを取得
    obj = bpy.context.active_object
    if not obj or obj.type != 'MESH':
        print("メッシュオブジェクトを選択してください。")
        return

    # スケールを物理寸法に強制適用
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 単位設定を確認し、2mmに相当する内部数値を決定
    unit_settings = bpy.context.scene.unit_settings
    step = 2.0
    
    if unit_settings.system == 'METRIC':
        if unit_settings.length_unit == 'METERS':
            step = 0.002
        elif unit_settings.length_unit == 'MILLIMETERS':
            step = 2.0

    # ワールド座標での正確なZ軸の範囲（高さ）を取得
    bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
    z_coords = [v.z for v in bbox]
    min_z = min(z_coords)
    max_z = max(z_coords)
    
    total_height = max_z - min_z
    
    if total_height <= step:
        step = total_height / 10.0

    original_name = obj.name
    obj.select_set(False)
    
    current_z = min_z
    slice_idx = 1
    
    while current_z < max_z:
        next_z = current_z + step
        
        if (max_z - next_z) < (step * 0.01):
            next_z = max_z
            
        # オブジェクトを複製してアクティブにする
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        bpy.context.collection.objects.link(new_obj)
        
        bpy.context.view_layer.objects.active = new_obj
        new_obj.select_set(True)
        
        # 編集モードに入って全選択
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        
        # 1. 下限のカット（current_z より下を削除）
        if current_z > min_z:
            bpy.ops.mesh.bisect(
                plane_co=(0, 0, current_z),
                plane_no=(0, 0, 1),
                clear_inner=True,
                clear_outer=False
            )
            # エラーの原因になる引数を避けて、カット後に直接面を張るコマンドを実行
            bpy.ops.mesh.fill_holes(sides=0)
            
        # 2. 上限のカット（next_z より上を削除）
        if next_z < max_z:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.bisect(
                plane_co=(0, 0, next_z),
                plane_no=(0, 0, 1),
                clear_inner=False,
                clear_outer=True
            )
            # カット後に直接面を張る
            bpy.ops.mesh.fill_holes(sides=0)
        
        # オブジェクトモードに戻る
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # メッシュが残っているかチェックしてリネーム
        if len(new_obj.data.vertices) == 0:
            bpy.data.objects.remove(new_obj, do_unlink=True)
        else:
            new_obj.name = f"{original_name}_slice_{slice_idx}"
            slice_idx += 1
            
        new_obj.select_set(False)
        current_z = next_z

    print(f"スライス完了：合計 {slice_idx - 1} 個のパーツに切り分けました。")

# スクリプトの実行
slice_object_by_exact_2mm_final()