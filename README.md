# Blender Object Slicer (2mm Interval)

A simple, robust Blender Python script that slices any selected mesh object into separate, solid parts at 2mm intervals along the Z-axis. 

This tool is especially useful for designing mechanical keyboard parts (like custom keycaps), 3D printing prep, prototyping with multi-material/layered structures, or exporting layered STL models.

## Features

- **Exact 2mm Slicing:** Automatically detects your Blender unit settings (meters or millimeters) and slices the mesh precisely every 2mm from the bottom up.
- **Auto-Cap (Solid Fill):** Utilizes Blender's `fill_holes` to automatically seal the cut surfaces, ensuring each slice remains a valid, closed solid mesh.
- **Non-Destructive:** Keeps your original object untouched and generates newly separated, named objects (`*_slice_1`, `*_slice_2`, etc.).
- **High Compatibility:** Avoids version-specific API bugs (like `fill`/`use_fill` keyword errors), making it safe to use across various Blender versions.

## How to Use

1. **Open the Scripting Workspace:**
   In Blender, switch to the **Scripting** tab at the top and click **New** to create a new text block.

2. **Paste the Code:**
   Copy and paste the code from `slice_script.py` into the text editor.

3. **Select Your Target Mesh:**
   In the 3D Viewport, select the mesh object (e.g., your keycap model) you want to slice to make it the active object.

4. **Run the Script:**
   Click the **Run Script** (Play icon) button in the text editor.

5. **Check the Output:**
   The script applies the object's scale and creates layered slices at the exact same location. Hide the original object or move the generated slices along the Z-axis (`G` -> `Z`) to see the result.

## Script Code (`slice_script.py`)

```python
# (You can include the final working Python script here inside your repository)
