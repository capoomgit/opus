import subprocess
import hou
import sys
import logging
import os

def render_smth(usd_path, save_path, project_id, work_id, version, frame_count):
    omni_render_out = f"{save_path}/Render_{project_id}_{work_id}_{version}/"
    res = os.system(f'C:/Users/capoom/AppData/Local/ov/pkg/isaac_sim-2022.1.1/python.bat P:/pipeline/standalone_dev/libs/omni_render.py {str(frame_count)} {usd_path} {omni_render_out}')
    print("Omniverse exit code: ", res)
    return True if res == 0 else False

"""
def render_smth(file_path, save_path, project_id, work_id, _version, render_engine, frame_count):
    hou.hipFile.clear(suppress_save_prompt=1)
    version = str(_version).zfill(4)
    print(version)
    try:
        obj = hou.node("/obj")
        out = hou.node("/out")
        

        tx,ty,tz = 0, 10, 80
        rx,ry,rz = -6, 0, 0

        cam = obj.createNode("cam", "cam")
        # set the camera position
        cam.parm("tx").set(tx)
        cam.parm("ty").set(ty)
        cam.parm("tz").set(tz)

        # set the camera rotation
        cam.parm("rx").set(rx)
        cam.parm("ry").set(ry)
        cam.parm("rz").set(rz)

        null = obj.createNode("null", "null")
        null.parm("ry").setExpression(f"$F/{frame_count} * 360")

        cam.setInput(0, null)

        # Create the geo node
        geo = obj.createNode("geo")
        geo.moveToGoodPosition()

        # Create the filecache node
        file = geo.createNode("file")
        file.moveToGoodPosition()
        file.parm("file").set(f"{file_path}")

        matchsize = geo.createNode("matchsize")
        matchsize.moveToGoodPosition()
        matchsize.setInput(0, file)
        matchsize.parm("justify_y").set(1)
        
        matchsize.setDisplayFlag(True)
        matchsize.setRenderFlag(True)

        if render_engine == "redshift":
            try:
                # Create the light
                light = obj.createNode("rslightdome")
                light.moveToGoodPosition()

                # create a rop node
                rop = out.createNode("Redshift_ROP")
                # TODO get this from admin/server
                # set the output path and format
                rop.parm("RS_outputFileNamePrefix").set(f"{save_path}/Render_{project_id}_{work_id}_{version}_$F4.png")
                rop.parm("RS_outputFileFormat").set(3)

                rop.parm("RS_renderCamera").set(cam.path())
                rop.parm("trange").set(1)
                rop.parm("f2").deleteAllKeyframes()
                rop.parm("f2").set(frame_count)
                # execute
                rop.parm('execute').pressButton()
                return True
            except Exception as e:
                print("Error: Redshift raised an exception", e)
                logging.info("Error: Redshift raised an exception", e)
        
        elif render_engine == "mantra":
            # create environment light
            light = obj.createNode("envlight")
            light.moveToGoodPosition()

            # create a rop node
            rop = out.createNode("ifd")

            # set the output path
            rop.parm("vm_picture").set(f"{save_path}/Render_{project_id}_{work_id}_{version}_$F4.png")
            rop.parm("camera").set(cam.path())

            rop.parm("trange").set(1)
            rop.parm("f2").deleteAllKeyframes()
            rop.parm("f2").set(frame_count)
            # execute
            rop.parm('execute').pressButton()
            return True
        
        elif render_engine == "omniverse":
            
            stage = hou.node("/stage")
            sopimport = stage.createNode("sopimport")
            sopimport.parm("soppath").set(file.path())
            sopimport.moveToGoodPosition()

            # This is moved to omnirender instead of houdini
            
            # light = stage.createNode("domelight")
            # light.moveToGoodPosition()
            # light.parm("xn__inputsintensity_i0a").set(1000)
            
            stagecam = stage.createNode("sceneimport")
            stagecam.parm("objects").set(cam.path())
            stagecam.moveToGoodPosition()
            
            # merge
            merge = stage.createNode("merge") 
            merge.moveToGoodPosition()
            merge.setInput(0, sopimport)
            # merge.setInput(1, light)
            merge.setInput(1, stagecam)

            # This is where we save the staged usd file
            usd_out = f"{save_path}/Render_{project_id}_{work_id}_{version}.usd"
            omni_render_out = f"{save_path}/Render_{project_id}_{work_id}_{version}/"


            # create a usd rop node
            rop = stage.createNode("usd_rop")
            rop.setInput(0, merge)
            rop.parm("lopoutput").set(usd_out)
            rop.parm("trange").set(1)
            rop.parm("f2").deleteAllKeyframes()
            rop.parm("f2").set(frame_count)
            rop.parm("savestyle").set("flattenstage")
            rop.parm("execute").pressButton()
            hou.hipFile.save(f"{save_path}/Render_{project_id}_{work_id}_{version}.hip")
            import os
            # TODO check if all machines have isaac installed
            
            res = os.system(f'C:/Users/capoom/AppData/Local/ov/pkg/isaac_sim-2022.1.1/python.bat P:/pipeline/standalone_dev/libs/omni_render.py {str(frame_count)} {usd_out} {omni_render_out}')

            return True if res == 0 else False
        
        elif render_engine == "karma":
            ###### Karma on obj level ######
            # create environment light
            light = obj.createNode("envlight")
            light.moveToGoodPosition()

            # create a rop node
            rop = out.createNode("karma")

            # set the output path
            rop.parm("picture").set(f"{save_path}/Render_{project_id}_{work_id}_{version}_$F4.png")
            rop.parm("camera").set(cam.path())

            rop.parm("trange").set(1)
            rop.parm("f2").deleteAllKeyframes()
            rop.parm("f2").set(frame_count)
            rop.parm("engine").set("XPU")
            # execute
            rop.parm('render').pressButton()
            return True
            # stage = hou.node("/stage")
            # sopimport = stage.createNode("sopimport")
            # sopimport.parm("soppath").set(file.path())
            # sopimport.moveToGoodPosition()

            # light = stage.createNode("domelight")
            # light.moveToGoodPosition()

            
            # stagecam = stage.createNode("sceneimport")
            # stagecam.parm("objects").set(cam.path())
            # stagecam.moveToGoodPosition()
            
            # # merge
            # merge = stage.createNode("merge") 
            # merge.moveToGoodPosition()
            # merge.setInput(0, sopimport)
            # merge.setInput(1, light)
            # merge.setInput(2, stagecam)

            # # karma rop
            # ropset = stage.createNode("karmarenderproperties")
            # ropset.setInput(0, merge)


            # camname = cam.path().replace("/obj", "")

            # print(f"Cam Name: {camname}")
            # ropset.parm("camera").set(camname)
            # ropset.parm("picture").set(f"{save_path}/render_{projectid}_{workid}_$F4.png")

            # rop = stage.createNode("usdrender_rop")
            # rop.setInput(0, ropset)

            # rop.parm("trange").set(1)
            # rop.parm("f2").deleteAllKeyframes()
            # rop.parm("f2").set(frame_count)
            # rop.parm("rendersettings").set("/render/")
            # rop.parm('execute').pressButton()
    except Exception as e:
        sys.stderr.write(str(e))
        return False
"""