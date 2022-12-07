import hou
import os
import capoom_utils as utils
import json
def merge_caches(projectid, workid, db, make_usd):
    try:
        # clear
        hou.hipFile.clear(suppress_save_prompt=1)

        obj = hou.node("/obj")
        geo = obj.createNode("geo", f"merge_{projectid}_{workid}")

        # TODO get this path from the database
        cache_path = f"P:/pipeline/standalone_dev/saved/{projectid}"


        last_saved = None
        # Get keep info from the database
        for i in range(len(db)):
            
            if db[i]["keep"] == True:
                hda_name = db[i]["name"]

                filecache = geo.createNode('filecache')
                # rename the name of the node
                filecache.setName(f"{hda_name}")

                filecache.moveToGoodPosition(move_inputs=False)
                filecache.parm('loadfromdisk').set(1)
                filecache.parm('filemethod').set(1)
                filecache.parm('trange').set(0)


                # TODO support usd
                filecache.parm('file').set(f"{cache_path}/{hda_name}_{projectid}/Out_0/{hda_name}_{projectid}_{workid}.bgeo.sc")
                last_saved = filecache
            else:
                # account for the fact that we are skipping a node
                i-=1
        
        # merge all nodes
        merge = geo.createNode("merge")
        merge.moveToGoodPosition(move_inputs=False)

        # loop over all nodes
        for i in range(len(db)):
            merge.setInput(i, geo.node(f"{db[i]['name']}"))

        # add normal node
        normal = geo.createNode("normal")
        normal.moveToGoodPosition(move_inputs=False)
        normal.setInput(0, merge)

        normal.setDisplayFlag(True)
        normal.setRenderFlag(True)

        # save the cache
        utils.filecache(geo, normal, f"{cache_path}/end/", f"merge_{projectid}_{workid}")

        
        if make_usd:
            stage = hou.node("/stage")
            sopimport = stage.createNode("sopimport")
            sopimport.parm("soppath").set(normal.path())
            sopimport.moveToGoodPosition()


            # # merge
            # merge = stage.createNode("merge")
            # merge.moveToGoodPosition()
            # merge.setInput(0, sopimport)

            # create a usd rop node
            rop = stage.createNode("usd_rop")
            rop.setInput(0, sopimport)
            rop.parm("lopoutput").set(f"{cache_path}/end/merge_{projectid}_{workid}.usd")
            rop.parm("trange").set(0)
            rop.parm("savestyle").set("flattenstage")
            rop.parm("execute").pressButton()
        
        all_params = []
        for i in range(len(db)):
            # Merge json files
            
            with open(f"{cache_path}/{db[i]['name']}_{projectid}/parms_{db[i]['name']}_{projectid}_{workid}.json", "r") as f:
                data = json.load(f)
                all_params.append(data)
        
        with open(f"{cache_path}/end/merged_{projectid}_{workid}.json", "w") as f:
            json.dump(all_params, f, indent=4)

        return True

    except Exception as e:
        utils.save_hip(hou, f"{cache_path}/errors/", workid)
        return e