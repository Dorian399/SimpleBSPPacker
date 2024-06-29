import os
import tkinter as tk
from tkinter import filedialog

def list_files_recursive(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.normpath(os.path.join(root, file))
            relative_path = os.path.relpath(full_path, path)
            file_list.append((relative_path, full_path))
    return file_list

def create_bat_file(bsp_file_path, output_file):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    bsp_filename = os.path.basename(bsp_file_path)
    bat_file = os.path.join(script_dir, 'pack_bsp.bat')
    
    with open(bat_file, 'w') as f:
        f.write(f'..\\..\\bin\\bspzip -addlist "{bsp_filename}" "{output_file}" "{os.path.splitext(bsp_filename)[0]}_packed.bsp"\n')
        f.write('pause\n')
        f.write(f'del "{output_file}"\n')
        f.write(f'del "{bat_file}"\n')
    
    print(f"Batch file created: {bat_file}")
    
    os.system(f'cmd /c "{bat_file}"')

def main():
    root = tk.Tk()
    root.withdraw()

    path = filedialog.askdirectory(title="Select a Directory")
    
    if path:
        if os.path.isdir(path):
            file_list = list_files_recursive(path)
            
            script_dir = os.path.dirname(os.path.realpath(__file__))
            output_file = os.path.join(script_dir, 'output.txt')
            
            with open(output_file, 'w') as f:
                for relative_path, full_path in file_list:
                    f.write(f"{relative_path}\n{full_path}\n")
                    
            print(f"File list saved to {output_file}")

            bsp_file_path = filedialog.askopenfilename(
                initialdir=script_dir,
                title="Select a .bsp file",
                filetypes=[("BSP files", "*.bsp")]
            )
            
            if bsp_file_path:
                print(f"Selected BSP file: {bsp_file_path}")
                
                create_bat_file(bsp_file_path, output_file)
                
            else:
                print("No BSP file selected.")
        else:
            print("The provided path is not a valid directory.")
    else:
        print("No directory selected.")

if __name__ == "__main__":
    main()
