import datetime
import os, sys

import carb
import omni.kit.app
import omni.kit.viewport_legacy
import omni.kit.viewport.utility
import omni.client

USD_PATH = "P:/pipeline/standalone_dev/saved/Test/Project_4_v0001/Render/Render_4_0_0001.usd"

class CapoomOV:
    def __init__(self):
        framework = carb.get_framework()
        framework.load_plugins(loaded_file_wildcards=["omni.kit.app.plugin"], search_paths=["${CARB_APP_PATH}/kernel/plugins"])
        self.app = omni.kit.app.get_app()
        self._startup()
        self.app.update()
        omni.client.set_hang_detection_time_ms(10000)

        self._wait_for_viewport()
        # self.app.update()
    def _startup(self):

        # Path to where kit was built to
        app_root = os.environ["CARB_APP_PATH"]

        sys.argv.insert(1, f"C:/Users/capoom/Documents/Arda/CapoomOV/apps/my_name.my_app.viewport.kit")
        # args.append("--no-window")
        # Start the default Kit Experience App
        self.app.startup("kit", app_root, sys.argv)

    def _wait_for_viewport(self) -> None:
        vp_window = omni.kit.viewport.utility.get_active_viewport_window()
        frame = 0
        if (
            vp_window is None
            and frame < 100
        ):
            self.app.update()
            frame += 1
            print(f"Waiting for viewport to load... {frame}")
        # once we load, we need a few frames so everything docks itself
        for _ in range(30):
            self.app.update()
        print("Viewport loaded")

    def is_running(self) -> bool:
        """
        bool: convenience function to see if app is running. True if running, False otherwise
        """
        # If there is no stage, we can assume that the app is about to close
        # self.app.update()
        return self._app.is_running() and not self.is_exiting() and self.context.get_stage() is not None
    # def run_orchestrator(self):
    #     rep.orchestrator.run()
    #     # Wait until started
    #     while not rep.orchestrator.get_is_started():
    #         self.app.update()

    #     # Wait until stopped
    #     while rep.orchestrator.get_is_started():
    #         self.app.update()
    #     rep.BackendDispatch.wait_until_done()


import logging
if __name__ == "__main__":
    capoomov = CapoomOV()
    app = capoomov.app
    app.print_and_log("App loaded fully")

    # Log to a log file
    # stream = app.get_log_event_stream()
    # logging.basicConfig(filename="C:/Users/capoom/Documents/Arda/CapoomOV/log.txt", level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream))

    import omni.usd
    import omni.kit.commands
    import omni.replicator.core as rep
    import omni.replicator

    while app.is_running():
        # app.print_and_log("App is running")
        cur_ctx = omni.usd.get_context()
        open_stage = cur_ctx.open_stage(USD_PATH)

        # Make sure usd is loaded
        for i in range (10):
            # try:
            #     print("Current status", cur_ctx.get_stage_state())
            # except Exception as e:
            #     print("Cur except ", e)
            app.update()

        with rep.new_layer():
            new_ctx = omni.usd.get_context()
            stage = new_ctx.get_stage()

            try:
                rep.create.cone(count=100, position=rep.distribution.uniform((-100,-100,-100),(100,100,100)))
                # render_product = rep.create.render_product("/null/cam", (1920, 1080))
            except Exception as e:
                print("New layer except", e)

            # print(render_product)
        # omni.kit.commands.execute('CreateDynamicSkyCommand',
        #     sky_url='https://omniverse-content-production.s3.us-west-2.amazonaws.com/Assets/Skies/2022_1/Skies/Dynamic/CumulusLight.usd',
        #     sky_path='/Environment/sky')

        # app.update()

            # render_product = rep.create.render_product("/null/cam", (1920, 1080))

# while capoomov.is_running():


