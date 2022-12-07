import os
import time
def render_with_omni(house_of_interest):
    # Get from args

    RES = (600, 600)

    
    import omni.replicator.core as rep
    from omni.replicator.core import Writer, AnnotatorRegistry
    import omni.kit
    from pxr import Usd
    import omni.usd
    import carb
    from semantics.schema.editor import PrimSemanticData

   
    # TODO change the file names so they don't overwrite each other
    # Couldn't get the writer to work with the file name
    # output_directory = r'C:/Users/capoom/Documents/Arda/omniverse_test/out/'
    
    def run_orchestrator():
        rep.orchestrator.run()
        # Wait until started
        while not rep.orchestrator.get_is_started():
            simulation_app.update()

        # Wait until stopped
        while rep.orchestrator.get_is_started():
            simulation_app.update()
        rep.BackendDispatch.wait_until_done()
    # Get all the file names from given path
    
    output_directory = r'P:/Projects/CES_FILM/scenes/output/usds_data/v09/'


    usdpath = f"P:/Projects/CES_FILM/scenes/output/usds/v05/{house_of_interest}/"
    usd_files = [f for f in os.listdir(usdpath) if os.path.isfile(os.path.join(usdpath, f))]
    usd_files = [f for f in usd_files.copy() if f.endswith(".usd")]

    # for x in usd_files:
    #     file_name = x.split("\\")[-1].split(".")[0]
    #     # Check if it is in output directory as folder
    #     if not os.path.exists(output_directory + file_name):
    #         usd_files.remove(x)
    
    for usdfile in usd_files:
        workid = usdfile.replace(".usd", "").split("_")[1]
        
        omni.usd.get_context().open_stage(f"{usdpath}{usdfile}")
        with rep.new_layer():
            render_product = rep.create.render_product("/AI_DRONE_STREET_RENDER", RES)

            stage = omni.usd.get_context().get_stage()
            for prim in stage.Traverse():
                if prim.GetTypeName() == "Mesh":
                    
                    prim_sd = PrimSemanticData(prim)
                    data = f"House{prim.GetName()}"
                    prim_sd.add_entry("class", data)

            writer = rep.WriterRegistry.get("BasicWriter")
            writer.initialize(
                output_dir=f"{output_directory}{house_of_interest}_{workid}/",
                instance_id_segmentation=True,
                bounding_box_2d_tight=True
            )

            writer.attach([render_product]) 

            with rep.trigger.on_frame(num_frames=1):
                rep.orchestrator.step()




    # Rename all the png file names
    # TODO support all the output types
    # simulation_app.close()

if __name__ == "__main__":
    GEN_CONFIG = {
        "renderer": "RayTracedLighting",
        # "renderer": "PathTracing",
        # "renderer": "Iray",

        "headless": True,
        # "open_usd": usd
    }

    
    

    folder_path = r"P:/Projects/CES_FILM/scenes/output/usds/v05/"
    house_of_interests = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

    from omni.isaac.kit import SimulationApp
    simulation_app = SimulationApp(GEN_CONFIG)

    for house_of_interest in house_of_interests:

        
        render_with_omni(house_of_interest)