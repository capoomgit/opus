
import sys, json

def render_with_omni(frame_count, out_config, usd_path, out_path):
    # DEFAULT CONFIG
    checks = ["rgb", "bb2t", "bb2l", "ss", "is", "distcam", "distplane", "bb3", "occ", "normal", "motvec"]
    for key in checks:
        if key not in out_config:
            out_config[key] = False

    if "resw" not in out_config or "resh" not in out_config:
        out_config["resw"] = 1920
        out_config["resh"] = 1080
    
    if "rendertype" not in out_config:
        out_config["rendertype"] = "RayTracedLighting"

    
    RES = (out_config["resw"], out_config["resh"])
    # Get from args
    GEN_CONFIG = {
        "renderer": out_config["rendertype"],
        # "renderer": "PathTracing",
        "headless": False,
    }
    from omni.isaac.kit import SimulationApp
    simulation_app = SimulationApp(GEN_CONFIG)

    # ext_manager = simulation_app._app.get_extension_manager()
    # ext_manager.set_extension_enabled_immediate("omni.kit.window.environment", True)
    
    import omni.replicator.core as rep
    import omni.usd
    from semantics.schema.editor import PrimSemanticData
    import omni.kit.commands
    import os
    from pxr import Sdf
    def assign_materials():
        stage = omni.usd.get_context().get_stage()
        for prim in stage.Traverse():
            if prim.GetTypeName() == "Mesh":

                prim_name = prim.GetName()
                if len(prim_name.split('_')) < 2:
                    print(f"prim_name: {prim_name} is not a valid material name")
                    continue

                material_name =prim_name.split('_')[0]
                material_type = prim_name.split('_')[1]
                # print(f"material_name: {material_name} material_type: {material_type}")

                #Create material reference
                if not stage.GetPrimAtPath(f"/materials/{material_name}_{material_type}"):
                    # print(f"Creating material reference: {material_name}_{material_type}")
                    omni.kit.commands.execute('CreateReference',
                        path_to=Sdf.Path(f"/materials/{material_name}_{material_type}"),
                        asset_path=f"{self.materials_path}/{material_name}.sbsar",
                        usd_context=omni.usd.get_context())

                #Assign material
                selected_material=stage.GetPrimAtPath(f"/materials/{material_name}_{material_type}")

                while selected_material.GetTypeName() != "Material":
                    selected_material = selected_material.GetChildren()[0]
                print(f"selected_material: {selected_material}")


                print(f"Assigning material: {selected_material.GetName()}")
                omni.kit.commands.execute('BindMaterialCommand',
                    prim_path=f"{prim.GetPath()}",
                    material_path=f"{selected_material.GetPath()}",
                    strength='weakerThanDescendants')

    def run_orchestrator():
        rep.orchestrator.run()
        # Wait until started
        while not rep.orchestrator.get_is_started():
            simulation_app.update()

        # Wait until stopped
        while rep.orchestrator.get_is_started():
            simulation_app.update()
        rep.BackendDispatch.wait_until_done()

    # TODO change the file names so they don't overwrite each other
    # Couldn't get the writer to work with the file name

    while simulation_app.is_running():
        omni.usd.get_context().open_stage(usd_path)
        with rep.new_layer():
            render_product = rep.create.render_product("/null/cam", RES)
            stage = omni.usd.get_context().get_stage()
            # omni.kit.commands.execute('CreateDynamicSkyCommand',
            #     sky_url='https://omniverse-content-production.s3.us-west-2.amazonaws.com/Assets/Skies/2022_1/Skies/Dynamic/CumulusLight.usd',
            #     sky_path='/Environment/sky')

            for prim in stage.Traverse():
                if prim.GetTypeName() == "Mesh":
                    prim_sd = PrimSemanticData(prim)
                    prim_sd.add_entry("class", "house")


            # TODO replace this with a writer of your own
            writer = rep.WriterRegistry.get("BasicWriter")
            writer.initialize(
                output_dir=out_path,
                rgb=out_config["rgb"],
                bounding_box_2d_tight=out_config["bb2t"],
                bounding_box_2d_loose=out_config["bb2l"],
                semantic_segmentation=out_config["ss"],
                instance_segmentation=out_config["is"],
                distance_to_camera=out_config["distcam"],
                distance_to_image_plane=out_config["distplane"],
                bounding_box_3d=out_config["bb3"],
                occlusion=out_config["occ"],
                normals=out_config["normal"],
                motion_vectors=out_config["motvec"]
            )
            writer.attach([render_product])

            with rep.trigger.on_frame(num_frames=int(frame_count)+1):
                # rep.orchestrator.step()
                run_orchestrator()

        return True

if __name__ == "__main__":
    # TODO switch to this after testing
    # import argparse

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--projectid", type=int, required=True)
    # parser.add_argument("--workid", type=int, required=True)
    # parser.add_argument("--frame_count", type=int, required=True)
    # parser.add_argument("--sim_config", type=str, required=True)
    # parser.add_argument("--out_config", type=str, required=True)

    # args = parser.parse_args()

    # render_with_omni(args.projectid, args.workid, args.frame_count, args.sim_config, args.out_config)
    

    # Open the config file
    with open("P:/pipeline/standalone/shared_settings.json") as f:
        try:
            sttngs = json.load(f)
            render_with_omni(sys.argv[1], sttngs, sys.argv[2], sys.argv[3])
        except Exception as e:
            print("Error: Omniverse raised an exception", e)
            # FIXME This does not work whatsoever, os.system does not catch the exit code
            sys.exit(1)
