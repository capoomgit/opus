# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#

from __future__ import annotations  # This allows us to hint types that do not yet exist like omni.usd etc

import os
import sys
import argparse
import re
import carb
import omni.kit.app
import builtins
import warnings


class SimulationApp:
    """Helper class to launch Omniverse Toolkit.

    Omniverse loads various plugins at runtime which cannot be imported unless
    the Toolkit is already running. Thus, it is necessary to launch the Toolkit first from
    your python application and then import everything else.

    Usage:

    .. code-block:: python

        # At top of your application
        from omni.isaac.kit import SimulationApp
        config = {
             width: "1280",
             height: "720",
             headless: False,
        }
        simulation_app = SimulationApp(config)

        # Rest of the code follows
        ...
        simulation_app.close()

    Note:
            The settings in :obj:`DEFAULT_LAUNCHER_CONFIG` are overwritten by those in :obj:`config`.

    Arguments:
        config (dict): A dictionary containing the configuration for the app. (default: None)
        experience (str): Path to the application config loaded by the launcher (default: "", will load app/omni.isaac.sim.python.kit if left blank)
    """

    DEFAULT_LAUNCHER_CONFIG = {
        "headless": True,
        "active_gpu": None,
        "physics_gpu": 0,
        "multi_gpu": True,
        "sync_loads": True,
        "width": 1280,
        "height": 720,
        "window_width": 1440,
        "window_height": 900,
        "display_options": 3094,
        "subdiv_refinement_level": 0,
        "renderer": "RayTracedLighting",  # Can also be PathTracing
        "anti_aliasing": 3,
        "samples_per_pixel_per_frame": 64,
        "denoiser": True,
        "max_bounces": 4,
        "max_specular_transmission_bounces": 6,
        "max_volume_bounces": 4,
        "open_usd": None,
        "livesync_usd": None,
        "memory_report": False,
    }
    """
    The config variable is a dictionary containing the following entries

    Args:
        headless (bool): Disable UI when running. Defaults to True
        active_gpu (int): Specify the GPU to use when running, set to None to use default value which is usually the first gpu, default is None
        physics_gpu (int): Specify the GPU to use when running physics simulation. Defaults to 0 (first GPU).
        multi_gpu (bool): Set to true to enable Multi GPU support, Defaults to true
        sync_loads (bool): When enabled, will pause rendering until all assets are loaded. Defaults to True
        width (int): Width of the viewport and generated images. Defaults to 1280
        height (int): Height of the viewport and generated images. Defaults to 720
        window_width (int): Width of the application window, independent of viewport, defaults to 1440,
        window_height (int): Height of the application window, independent of viewport, defaults to 900,
        display_options (int): used to specify whats visible in the stage by default. Defaults to 3094 so extra objects do not appear in synthetic data. 3286 is another good default, used for the regular isaac-sim editor experience
        subdiv_refinement_level (int): Number of subdivisons to perform on supported geometry. Defaults to 0
        renderer (str): Rendering mode, can be  `RayTracedLighting` or `PathTracing`. Defaults to `PathTracing`
        anti_aliasing (int): Antialiasing mode, 0: Disabled, 1: TAA, 2: FXAA, 3: DLSS, 4:RTXAA
        samples_per_pixel_per_frame (int): The number of samples to render per frame, increase for improved quality, used for `PathTracing` only. Defaults to 64
        denoiser (bool):  Enable this to use AI denoising to improve image quality, used for `PathTracing` only. Defaults to True
        max_bounces (int): Maximum number of bounces, used for `PathTracing` only. Defaults to 4
        max_specular_transmission_bounces (int): Maximum number of bounces for specular or transmission, used for `PathTracing` only. Defaults to 6
        max_volume_bounces (int): Maximum number of bounces for volumetric materials, used for `PathTracing` only. Defaults to 4
        open_usd (str): This is the name of the usd to open when the app starts. It will not be saved over. Default is None and an empty stage is created on startup.
        livesync_usd (str): This is the location of the usd that you want to do your interactive work in.  The existing file is overwritten. Default is None
        memory_report (bool): Deprecated, enable the omni.isaac.statistics_logging extension to log directly to disk
    """

    def __init__(self, launch_config: dict = None, experience: str = "") -> None:
        # Sanity check to see if any extra omniverse modules are loaded
        # Warn users if so because this will usually cause issues.
        # Base list of modules that can be loaded before kit app starts, might need to be updated in the future
        ok_list = [
            "omni",
            "omni.isaac",
            "omni.isaac.kit",
            "omni.isaac.kit.simulation_app",
            "omni.kit",
            "omni.kit.app",
            "omni.kit.app.impl",
            "omni.kit.app.impl.app_iface",
            "omni.kit.app.impl.telemetry_helpers",
            "omni.ext",
            "omni.ext.impl",
            "omni.ext._extensions",
            "omni.ext.impl._internal",
            "omni.ext.impl.leak_detection",
            "omni.ext.impl.stat_cache",
            "omni.ext.impl.ext_settings",
            "omni.ext.impl.custom_importer",
            "omni.kit.app._app",
        ]
        r = re.compile("omni.*|pxr.*")
        found_modules = list(filter(r.match, list(sys.modules.keys())))
        result = []
        for item in found_modules:
            if item not in ok_list:
                result.append(item)
        # Made this a warning instead of an error as the above list might be incomplete
        if len(result):
            carb.log_warn(
                f"Modules: {result} were loaded before SimulationApp was started and might not be loaded correctly."
            )
            carb.log_warn(
                "Please check to make sure no extra omniverse or pxr modules are imported before the call to SimulationApp(...)"
            )

        # Initialize variables
        builtins.ISAAC_LAUNCHED_FROM_TERMINAL = False
        self._exiting = False

        # Override settings from input config
        self.config = self.DEFAULT_LAUNCHER_CONFIG
        if experience == "":
            experience = f'{os.environ["EXP_PATH"]}/omni.isaac.sim.python.kit'
        self.config.update({"experience": experience})
        if launch_config is not None:
            self.config.update(launch_config)
        if builtins.ISAAC_LAUNCHED_FROM_JUPYTER:
            if self.config["headless"] is False:
                carb.log_warn("Non-headless mode not supported with jupyter notebooks")
                # self.config.update({"headless": True}) # Disable this, in case the user really wants to run non-headless

        # Load omniverse application plugins
        self._framework = carb.get_framework()
        self._framework.load_plugins(
            loaded_file_wildcards=["omni.kit.app.plugin"],
            search_paths=[os.path.abspath(f'{os.environ["CARB_APP_PATH"]}/plugins')],
        )
        # Get Omniverse application
        self._app = omni.kit.app.get_app()
        self._start_app()

        # vp_interface = omni.kit.viewport_legacy.acquire_viewport_interface()
        # vp_window = vp_interface.get_viewport_window()
        # drawable = vp_window.get_drawable()

        # if drawable is None:
        #     self._app.update()

        # once app starts, we can set settings
        from .utils import set_carb_setting, open_stage, create_new_stage, set_livesync_stage

        self._carb_settings = carb.settings.get_settings()
        # apply render settings specified in config
        self.reset_render_settings()

        self._app.print_and_log("Simulation App Starting")

        self._app.update()

        self.open_usd = self.config.get("open_usd")
        if self.open_usd is not None:
            print("Opening usd file at ", self.open_usd, " ...", end="")
            if open_stage(self.open_usd) is False:
                print("Could not open", self.open_usd, "creating a new empty stage")
                create_new_stage()
            else:
                print("Done.")
        else:
            create_new_stage()

        self.livesync_usd = self.config.get("livesync_usd")
        if self.livesync_usd != None:
            print("Saving a temp livesync stage at ", self.livesync_usd, " ...", end="")
            if set_livesync_stage(self.livesync_usd, True):
                print("Done.")
            else:
                print("Could not save usd file to ", self.livesync_usd)

        # Update the app
        self._app.update()
        # self._prepare_ui()  # Dock floating UIs this might not be needed anymore as extensions dock themselves

        # Increase hang detection timeout
        omni.client.set_hang_detection_time_ms(10000)

        # Set the window title to something simpler
        from omni.isaac.version import get_version
        from omni.kit.window.title import get_main_window_title

        window_title = get_main_window_title()
        app_version_core, app_version_prerel, _, _, _, _, _, _ = get_version()
        window_title.set_app_version(app_version_core)

        self._wait_for_viewport()

        if self.config.get("memory_report"):
            warnings.warn(
                "memory_report option is deprecated, please enable the omni.isaac.statistics_logging extension to log directly to disk",
                DeprecationWarning,
            )
        # Notify toolkit is running
        self._app.print_and_log("Simulation App Startup Complete")

    def __del__(self):
        """Destructor for the class."""
        if self._exiting is False and sys.meta_path is None:
            print(
                "\033[91m"
                + "ERROR: Python exiting while SimulationApp was still running, Please call close() on the SimulationApp object to exit cleanly"
                + "\033[0m"
            )
        pass

    """
    Private methods
    """

    def _start_app(self) -> None:
        """Launch the Omniverse application."""
        exe_path = os.path.abspath(f'{os.environ["CARB_APP_PATH"]}')
        # input arguments to the application
        args = [
            os.path.abspath(__file__),
            f'"C:/Users/capoom/Documents/Arda/CapoomOV/apps/my_name.my_app.viewport.kit"',
            f"--/app/tokens/exe-path={exe_path}",  # this is needed so dlss lib is found
            f'--/persistent/app/viewport/displayOptions={self.config["display_options"]}',  # hide extra stuff in viewport
            # Forces kit to not render until all USD files are loaded
            f'--/rtx/materialDb/syncLoads={self.config["sync_loads"]}',
            f'--/rtx/hydra/materialSyncLoads={self.config["sync_loads"]}'
            f'--/omni.kit.plugin/syncUsdLoads={self.config["sync_loads"]}',
            f'--/app/renderer/resolution/width={self.config["width"]}',
            f'--/app/renderer/resolution/height={self.config["height"]}',
            f'--/app/window/width={self.config["window_width"]}',
            f'--/app/window/height={self.config["window_height"]}',
            f'--/renderer/multiGpu/enabled={self.config["multi_gpu"]}',
            "--ext-folder",
            f'{"C:/Users/capoom/Documents/Arda/CapoomOV/apps/my_name.my_app.viewport.kit"}/exts',  # adding to json doesn't work
            "--ext-folder",
            f'{"C:/Users/capoom/Documents/Arda/CapoomOV/apps/my_name.my_app.viewport.kit"}/apps',  # so we can reference other kit files
        ]
        if self.config.get("active_gpu") is not None:
            args.append(f'--/renderer/activeGpu={self.config["active_gpu"]}')
        if self.config.get("physics_gpu") is not None:
            args.append(f'--/physics/cudaDevice={self.config["physics_gpu"]}')
        # parse any extra command line args here
        # user script should provide its own help, otherwise we default to printing the kit app help output
        parser = argparse.ArgumentParser(add_help=False)
        parsed_args, unknown_args = parser.parse_known_args()
        # is user did not request portable root,
        # we still run apps as portable to prevent them writing extra files to user directory
        if "--portable-root" not in unknown_args:
            args.append("--portable")
        if self.config.get("headless") and "--no-window" not in unknown_args:
            args.append("--no-window")

        # get the effective uid of this process, if its root, then we automatically add the allow root flag
        # if the flag is already in unknown_args, we don't need to add it again.
        if sys.platform.startswith("linux"):
            if os.geteuid() == 0 and "--allow-root" not in unknown_args:
                args.append("--allow-root")

        # pass all extra arguments onto the main kit app
        print("Starting kit application with the fillowing args: ", args)
        print("Passing the following args to the base kit application: ", unknown_args)
        args.extend(unknown_args)
        self.app.startup("kit", os.environ["CARB_APP_PATH"], args)
        # if user called with -h kit auto exits so we force exit the script here as well
        if "-h" in unknown_args or "--help" in unknown_args:
            sys.exit()

    def _set_render_settings(self, default: bool = False) -> None:
        """Set render settings to those in config.

        Note:
            This should be used in case a new stage is opened and the desired config needs
            to be re-applied.

        Args:
            default (bool, optional): Whether to setup RTX default or non-default settings. Defaults to False.
        """
        from .utils import set_carb_setting

        # Define mode to configure settings into.
        if default:
            rtx_mode = "/rtx-defaults"
        else:
            rtx_mode = "/rtx"

        # Set renderer mode.
        set_carb_setting(self._carb_settings, rtx_mode + "/rendermode", self.config["renderer"])
        # Raytrace mode settings
        set_carb_setting(self._carb_settings, rtx_mode + "/post/aa/op", self.config["anti_aliasing"])
        # Pathtrace mode settings
        set_carb_setting(self._carb_settings, rtx_mode + "/pathtracing/spp", self.config["samples_per_pixel_per_frame"])
        set_carb_setting(
            self._carb_settings, rtx_mode + "/pathtracing/totalSpp", self.config["samples_per_pixel_per_frame"]
        )
        set_carb_setting(
            self._carb_settings, rtx_mode + "/pathtracing/clampSpp", self.config["samples_per_pixel_per_frame"]
        )
        set_carb_setting(self._carb_settings, rtx_mode + "/pathtracing/maxBounces", self.config["max_bounces"])
        set_carb_setting(
            self._carb_settings,
            rtx_mode + "/pathtracing/maxSpecularAndTransmissionBounces",
            self.config["max_specular_transmission_bounces"],
        )
        set_carb_setting(
            self._carb_settings, rtx_mode + "/pathtracing/maxVolumeBounces", self.config["max_volume_bounces"]
        )
        set_carb_setting(self._carb_settings, rtx_mode + "/pathtracing/optixDenoiser/enabled", self.config["denoiser"])
        set_carb_setting(
            self._carb_settings, rtx_mode + "/hydra/subdivision/refinementLevel", self.config["subdiv_refinement_level"]
        )

        # Experimental, forces kit to not render until all USD files are loaded
        set_carb_setting(self._carb_settings, rtx_mode + "/materialDb/syncLoads", self.config["sync_loads"])
        set_carb_setting(self._carb_settings, rtx_mode + "/hydra/materialSyncLoads", self.config["sync_loads"])
        set_carb_setting(self._carb_settings, "/omni.kit.plugin/syncUsdLoads", self.config["sync_loads"])

    def _prepare_ui(self) -> None:
        """Dock the windows in the UI if they exist."""
        import omni.ui

        # Method for docking a particular window to a location
        def dock_window(space, name, location, ratio=0.5):
            window = omni.ui.Workspace.get_window(name)
            if window and space:
                window.dock_in(space, location, ratio=ratio)
            return window

        # Acquire the main docking station
        main_dockspace = omni.ui.Workspace.get_window("DockSpace")
        # Acquire the docking space for viewport
        view = dock_window(main_dockspace, "Viewport", omni.ui.DockPosition.TOP)
        self._app.update()
        console = dock_window(view, "Console", omni.ui.DockPosition.BOTTOM, 0.3)
        dock_window(view, "Main ToolBar", omni.ui.DockPosition.LEFT)
        self._app.update()
        # Acquire the docking window where `Stage` tab is present and add tabs
        render = dock_window(main_dockspace, "Render Settings", omni.ui.DockPosition.RIGHT, 0.3)
        dock_window(render, "Stage", omni.ui.DockPosition.SAME)
        dock_window(render, "Layer", omni.ui.DockPosition.SAME)
        dock_window(console, "Content", omni.ui.DockPosition.SAME)
        self._app.update()
        dock_window(render, "Property", omni.ui.DockPosition.BOTTOM)

    def _wait_for_viewport(self) -> None:
        vp_interface = omni.kit.viewport_legacy.acquire_viewport_interface()
        vp_window = vp_interface.get_viewport_window()
        frame = 0
        if (
            vp_window.get_drawable_ldr_resource() is None
            and vp_window.get_drawable_hdr_resource() is None
            and frame < 100
        ):
            self._app.update()
            frame += 1
        # once we load, we need a few frames so everything docks itself
        for _ in range(10):
            self._app.update()

    """
    Public methods
    """

    def update(self) -> None:
        """
        Convenience function to step the application forward one frame
        """
        self._app.update()
        return

    def set_setting(self, setting: str, value) -> None:
        """
        Set a carbonite setting

        Args:
            setting (str): carb setting path
            value: value to set the setting to, type is used to properly set the setting.
        """
        from .utils import set_carb_setting

        set_carb_setting(self._carb_settings, setting, value)

    def reset_render_settings(self):
        """Reset render settings to those in config.

        Note:
            This should be used in case a new stage is opened and the desired config needs
            to be re-applied.
        """
        # Set rtx-default renderder settings
        self._set_render_settings(default=True)
        # Set rtx settings renderer settings
        self._set_render_settings(default=False)

    def close(self) -> None:
        """Close the running Omniverse Toolkit."""
        # workaround for exit issues, clean the stage first:
        omni.usd.get_context().close_stage()
        omni.kit.app.get_app().update()
        # check if exited already
        if not self._exiting:
            self._exiting = True
            self._app.print_and_log("Simulation App Shutting Down")

            # We are exisitng but something is still loading, wait for it to load to avoid a deadlock
            from .utils import is_stage_loading

            if is_stage_loading():
                print("   Waiting for USD resource operations to complete (this may take a few seconds)")
            while is_stage_loading():
                self._app.update()
            self._app.shutdown()
            # disabled on linux to workaround issues where unloading plugins causes carb to fail
            if sys.platform == "win32":
                self._framework.unload_all_plugins()
            # Force all omni module to unload on close
            # This prevents crash on exit
            for m in list(sys.modules.keys()):
                if "omni" in m and m != "omni.kit.app":
                    del sys.modules[m]
            print("Simulation App Shutdown Complete")

    def is_running(self) -> bool:
        """
        bool: convenience function to see if app is running. True if running, False otherwise
        """
        # If there is no stage, we can assume that the app is about to close
        return self._app.is_running() and not self.is_exiting() and self.context.get_stage() is not None

    def is_exiting(self) -> bool:
        """
        bool: True if close() was called previously, False otherwise
        """
        return self._exiting

    @property
    def app(self) -> omni.kit.app.IApp:
        """
        omni.kit.app.IApp: omniverse kit application object
        """
        return self._app

    @property
    def context(self) -> omni.usd.UsdContext:
        """
        omni.usd.UsdContext: the current USD context
        """
        return omni.usd.get_context()

if __name__ == "__main__":
    print("AAAAAAAAAAAAAAAAAAAAAAA")
    app = SimulationApp()

    while app.is_running():
        app.update()