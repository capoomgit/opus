import hou

# TODO material support
def stage_usd(cache_path, save_path, project_id, work_id, version, frame_count):
    try:
        obj = hou.node("/obj")

        # TODO get the cams from db?
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

        # TODO fix the path issue
        null = obj.createNode("null", "null")
        null.parm("ry").setExpression(f"$F/{frame_count} * 360")

        cam.setInput(0, null)

        # Create the geo node
        geo = obj.createNode("geo")
        geo.moveToGoodPosition()

        # Create the filecache node
        file = geo.createNode("file")
        file.moveToGoodPosition()
        file.parm("file").set(f"{cache_path}")

        matchsize = geo.createNode("matchsize")
        matchsize.moveToGoodPosition()
        matchsize.setInput(0, file)
        matchsize.parm("justify_y").set(1)

        matchsize.setDisplayFlag(True)
        matchsize.setRenderFlag(True)

        stage = hou.node("/stage")
        sopimport = stage.createNode("sopimport")
        sopimport.parm("soppath").set(file.path())
        sopimport.moveToGoodPosition()

        # This is moved to omniverse instead of houdini

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
        usd_out = f"{save_path}/Staged_{project_id}_{work_id}_{version}.usd"

        # create a usd rop node
        rop = stage.createNode("usd_rop")
        rop.setInput(0, merge)
        rop.parm("lopoutput").set(usd_out)
        rop.parm("trange").set(1)
        rop.parm("f2").deleteAllKeyframes()
        rop.parm("f2").set(frame_count)
        rop.parm("savestyle").set("flattenstage")
        rop.parm("execute").pressButton()
        hou.hipFile.save(f"{save_path}/Staged_{project_id}_{work_id}_{version}.hip")
        return True
    except Exception as e:
        return e