import logging
import tkinter as tk

from coretk.images import Images

# from coretk.tooltip import CreateToolTip


class CoreToolbar(object):
    """
    Core toolbar class
    """

    def __init__(self, master, edit_frame, menubar):
        """
        Create a CoreToolbar instance

        :param tkinter.Frame edit_frame: edit frame
        """
        self.master = master
        self.edit_frame = edit_frame
        self.menubar = menubar
        self.radio_value = tk.IntVar()
        self.exec_radio_value = tk.IntVar()

        # button dimension
        self.width = 32
        self.height = 32

        # Used for drawing the horizontally displayed menu items for network-layer nodes and link-layer node
        self.selection_tool_button = None

        # Reference to the option menus
        self.link_layer_option_menu = None
        self.marker_option_menu = None
        self.network_layer_option_menu = None

    def load_toolbar_images(self):
        """
        Load the images that appear in core toolbar

        :return: nothing
        """
        Images.load("core", "core-icon.png")
        Images.load("start", "start.gif")
        Images.load("switch", "lanswitch.gif")
        Images.load("marker", "marker.gif")
        Images.load("router", "router.gif")
        Images.load("select", "select.gif")
        Images.load("link", "link.gif")
        Images.load("hub", "hub.gif")
        Images.load("wlan", "wlan.gif")
        Images.load("rj45", "rj45.gif")
        Images.load("tunnel", "tunnel.gif")
        Images.load("oval", "oval.gif")
        Images.load("rectangle", "rectangle.gif")
        Images.load("text", "text.gif")
        Images.load("host", "host.gif")
        Images.load("pc", "pc.gif")
        Images.load("mdr", "mdr.gif")
        Images.load("prouter", "router_green.gif")
        Images.load("ovs", "OVS.gif")
        Images.load("editnode", "document-properties.gif")
        Images.load("run", "run.gif")
        Images.load("plot", "plot.gif")
        Images.load("twonode", "twonode.gif")
        Images.load("stop", "stop.gif")
        Images.load("observe", "observe.gif")

    def destroy_previous_frame(self):
        """
        Destroy any extra frame from previous before drawing a new one

        :return: nothing
        """
        if (
            self.network_layer_option_menu
            and self.network_layer_option_menu.winfo_exists()
        ):
            self.network_layer_option_menu.destroy()
        if self.link_layer_option_menu and self.link_layer_option_menu.winfo_exists():
            self.link_layer_option_menu.destroy()
        if self.marker_option_menu and self.marker_option_menu.winfo_exists():
            self.marker_option_menu.destroy()

    def destroy_children_widgets(self, parent):
        """
        Destroy all children of a parent widget

        :param tkinter.Frame parent: parent frame
        :return: nothing
        """

        for i in parent.winfo_children():
            if i.winfo_name() != "!frame":
                i.destroy()

    def create_button(self, img, func, frame, main_button):
        """
        Create button and put it on the frame

        :param PIL.Image img: button image
        :param func: the command that is executed when button is clicked
        :param tkinter.Frame frame: frame that contains the button
        :param tkinter.Radiobutton main_button: main button
        :return: nothing
        """
        button = tk.Button(frame, width=self.width, height=self.height, image=img)
        button.pack(side=tk.LEFT, pady=1)
        button.bind("<Button-1>", lambda mb: func(main_button))

    def create_radio_button(self, frame, image, func, variable, value):
        button = tk.Radiobutton(
            frame,
            indicatoron=False,
            width=self.width,
            height=self.height,
            image=image,
            value=value,
            variable=variable,
            command=func,
        )
        button.pack(side=tk.TOP, pady=1)

    def create_regular_button(self, frame, image, func):
        button = tk.Button(
            frame, width=self.width, height=self.height, image=image, command=func
        )
        button.pack(side=tk.TOP, pady=1)

    def draw_button_menu_frame(self, edit_frame, option_frame, main_button):
        """
        Draw option menu frame right next to the main button

        :param tkinter.Frame edit_frame: parent frame of the main button
        :param tkinter.Frame option_frame: option frame to draw
        :param tkinter.Radiobutton main_button: the main button
        :return: nothing
        """

        first_button = edit_frame.winfo_children()[0]
        _x = main_button.winfo_rootx() - first_button.winfo_rootx() + 40
        _y = main_button.winfo_rooty() - first_button.winfo_rooty() - 1
        option_frame.place(x=_x, y=_y)

    def bind_widgets_before_frame_hide(self, frame):
        """
        Bind the widgets to a left click, when any of the widgets is clicked, the menu option frame is destroyed before
        any further action is performed

        :param tkinter.Frame frame: the frame to be destroyed
        :return: nothing
        """
        self.menubar.bind("<Button-1>", lambda e: frame.destroy())
        self.master.bind("<Button-1>", lambda e: frame.destroy())

    def unbind_widgets_after_frame_hide(self):
        """
        Unbind the widgets to make sure everything works normally again after the menu option frame is destroyed

        :return: nothing
        """
        self.master.unbind("<Button-1>")
        self.menubar.unbind("Button-1>")

    def click_selection_tool(self):
        logging.debug("Click SELECTION TOOL")

    def click_start_stop_session_tool(self):
        logging.debug("Click START STOP SESSION button")
        self.destroy_children_widgets(self.edit_frame)
        self.create_runtime_toolbar()

    def click_link_tool(self):
        logging.debug("Click LINK button")

    def pick_router(self, main_button):
        self.network_layer_option_menu.destroy()
        main_button.configure(image=Images.get("router"))
        logging.debug("Pick router option")

    def pick_host(self, main_button):
        self.network_layer_option_menu.destroy()
        main_button.configure(image=Images.get("host"))
        logging.debug("Pick host option")

    def pick_pc(self, main_button):
        self.network_layer_option_menu.destroy()
        main_button.configure(image=Images.get("pc"))
        logging.debug("Pick PC option")

    def pick_mdr(self, main_button):
        self.network_layer_option_menu.destroy()
        main_button.configure(image=Images.get("mdr"))
        logging.debug("Pick MDR option")

    def pick_prouter(self, main_button):
        self.network_layer_option_menu.destroy()
        main_button.configure(image=Images.get("prouter"))
        logging.debug("Pick prouter option")

    def pick_ovs(self, main_button):
        self.network_layer_option_menu.destroy()
        main_button.configure(image=Images.get("ovs"))
        logging.debug("Pick OVS option")

    def pick_editnode(self, main_button):
        self.network_layer_option_menu.destroy()
        main_button.configure(image=Images.get("editnode"))
        logging.debug("Pick editnode option")

    def draw_network_layer_options(self, network_layer_button):
        """
        Draw the options for network-layer button

        :param tkinter.Radiobutton network_layer_button: network-layer button
        :return: nothing
        """
        # create a frame and add buttons to it
        self.destroy_previous_frame()
        option_frame = tk.Frame(self.master, padx=1, pady=1)
        img_list = [
            Images.get("router"),
            Images.get("host"),
            Images.get("pc"),
            Images.get("mdr"),
            Images.get("prouter"),
            Images.get("ovs"),
            Images.get("editnode"),
        ]
        func_list = [
            self.pick_router,
            self.pick_host,
            self.pick_pc,
            self.pick_mdr,
            self.pick_prouter,
            self.pick_ovs,
            self.pick_editnode,
        ]
        for i in range(len(img_list)):
            self.create_button(
                img_list[i], func_list[i], option_frame, network_layer_button
            )

        # place frame at a calculated position as well as keep a reference of that frame
        self.draw_button_menu_frame(self.edit_frame, option_frame, network_layer_button)
        self.network_layer_option_menu = option_frame

        # destroy the frame before any further actions on other widgets
        self.bind_widgets_before_frame_hide(option_frame)
        option_frame.wait_window(option_frame)
        self.unbind_widgets_after_frame_hide()

    def create_network_layer_button(self):
        """
        Create network layer button

        :return: nothing
        """
        router_image = Images.get("router")
        network_layer_button = tk.Radiobutton(
            self.edit_frame,
            indicatoron=False,
            variable=self.radio_value,
            value=3,
            width=self.width,
            height=self.height,
            image=router_image,
            command=lambda: self.draw_network_layer_options(network_layer_button),
        )
        network_layer_button.pack(side=tk.TOP, pady=1)
        # network_layer_btt = CreateToolTip(network_layer_button, "Network-layer virtual nodes")

    def pick_hub(self, main_button):
        self.link_layer_option_menu.destroy()
        main_button.configure(image=Images.get("hub"))
        logging.debug("Pick link-layer node HUB")

    def pick_switch(self, main_button):
        self.link_layer_option_menu.destroy()
        main_button.configure(image=Images.get("switch"))
        logging.debug("Pick link-layer node SWITCH")

    def pick_wlan(self, main_button):
        self.link_layer_option_menu.destroy()
        main_button.configure(image=Images.get("wlan"))
        logging.debug("Pick link-layer node WLAN")

    def pick_rj45(self, main_button):
        self.link_layer_option_menu.destroy()
        main_button.configure(image=Images.get("rj45"))
        logging.debug("Pick link-layer node RJ45")

    def pick_tunnel(self, main_button):
        self.link_layer_option_menu.destroy()
        main_button.configure(image=Images.get("tunnel"))
        logging.debug("Pick link-layer node TUNNEL")

    def draw_link_layer_options(self, link_layer_button):
        """
        Draw the options for link-layer button

        :param tkinter.RadioButton link_layer_button: link-layer button
        :return: nothing
        """
        # create a frame and add buttons to it
        self.destroy_previous_frame()
        option_frame = tk.Frame(self.master, padx=1, pady=1)
        img_list = [
            Images.get("hub"),
            Images.get("switch"),
            Images.get("wlan"),
            Images.get("rj45"),
            Images.get("tunnel"),
        ]
        func_list = [
            self.pick_hub,
            self.pick_switch,
            self.pick_wlan,
            self.pick_rj45,
            self.pick_tunnel,
        ]
        for i in range(len(img_list)):
            self.create_button(
                img_list[i], func_list[i], option_frame, link_layer_button
            )

        # place frame at a calculated position as well as keep a reference of the frame
        self.draw_button_menu_frame(self.edit_frame, option_frame, link_layer_button)
        self.link_layer_option_menu = option_frame

        # destroy the frame before any further actions on other widgets
        self.bind_widgets_before_frame_hide(option_frame)
        option_frame.wait_window(option_frame)
        self.unbind_widgets_after_frame_hide()

    def create_link_layer_button(self):
        """
        Create link-layer node button and the options that represent different link-layer node types

        :return: nothing
        """
        hub_image = Images.get("hub")
        link_layer_button = tk.Radiobutton(
            self.edit_frame,
            indicatoron=False,
            variable=self.radio_value,
            value=4,
            width=self.width,
            height=self.height,
            image=hub_image,
            command=lambda: self.draw_link_layer_options(link_layer_button),
        )
        link_layer_button.pack(side=tk.TOP, pady=1)

    def pick_marker(self, main_button):
        self.marker_option_menu.destroy()
        main_button.configure(image=Images.get("marker"))
        logging.debug("Pick MARKER")
        return "break"

    def pick_oval(self, main_button):
        self.marker_option_menu.destroy()
        main_button.configure(image=Images.get("oval"))
        logging.debug("Pick OVAL")

    def pick_rectangle(self, main_button):
        self.marker_option_menu.destroy()
        main_button.configure(image=Images.get("rectangle"))
        logging.debug("Pick RECTANGLE")

    def pick_text(self, main_button):
        self.marker_option_menu.destroy()
        main_button.configure(image=Images.get("text"))
        logging.debug("Pick TEXT")

    def draw_marker_options(self, main_button):
        """
        Draw the options for marker button

        :param tkinter.Radiobutton main_button: the main button
        :return: nothing
        """
        # create a frame and add buttons to it
        self.destroy_previous_frame()
        option_frame = tk.Frame(self.master, padx=1, pady=1)
        img_list = [
            Images.get("marker"),
            Images.get("oval"),
            Images.get("rectangle"),
            Images.get("text"),
        ]
        func_list = [
            self.pick_marker,
            self.pick_oval,
            self.pick_rectangle,
            self.pick_text,
        ]
        for i in range(len(img_list)):
            self.create_button(img_list[i], func_list[i], option_frame, main_button)

        # place the frame at a calculated position as well as keep a reference of that frame
        self.draw_button_menu_frame(self.edit_frame, option_frame, main_button)
        self.marker_option_menu = option_frame

        # destroy the frame before any further actions on other widgets
        self.bind_widgets_before_frame_hide(option_frame)
        option_frame.wait_window(option_frame)
        self.unbind_widgets_after_frame_hide()

    def create_marker_button(self):
        """
        Create marker button and options that represent different marker types

        :return: nothing
        """
        marker_image = Images.get("marker")
        marker_main_button = tk.Radiobutton(
            self.edit_frame,
            indicatoron=False,
            variable=self.radio_value,
            value=5,
            width=self.width,
            height=self.height,
            image=marker_image,
            command=lambda: self.draw_marker_options(marker_main_button),
        )
        marker_main_button.pack(side=tk.TOP, pady=1)

    def create_toolbar(self):
        self.load_toolbar_images()
        self.create_regular_button(
            self.edit_frame, Images.get("start"), self.click_start_stop_session_tool
        )
        self.create_radio_button(
            self.edit_frame,
            Images.get("select"),
            self.click_selection_tool,
            self.radio_value,
            1,
        )
        self.create_radio_button(
            self.edit_frame,
            Images.get("link"),
            self.click_link_tool,
            self.radio_value,
            2,
        )
        self.create_network_layer_button()
        self.create_link_layer_button()
        self.create_marker_button()

    def create_observe_button(self):
        menu_button = tk.Menubutton(
            self.edit_frame,
            image=Images.get("observe"),
            width=self.width,
            height=self.height,
            direction=tk.RIGHT,
            relief=tk.RAISED,
        )
        menu_button.menu = tk.Menu(menu_button, tearoff=0)
        menu_button["menu"] = menu_button.menu
        menu_button.pack(side=tk.TOP, pady=1)

        menu_button.menu.add_command(label="None")
        menu_button.menu.add_command(label="processes")
        menu_button.menu.add_command(label="ifconfig")
        menu_button.menu.add_command(label="IPv4 routes")
        menu_button.menu.add_command(label="IPv6 routes")
        menu_button.menu.add_command(label="OSPFv2 neighbors")
        menu_button.menu.add_command(label="OSPFv3 neighbors")
        menu_button.menu.add_command(label="Listening sockets")
        menu_button.menu.add_command(label="IPv4 MFC entries")
        menu_button.menu.add_command(label="IPv6 MFC entries")
        menu_button.menu.add_command(label="firewall rules")
        menu_button.menu.add_command(label="IPSec policies")
        menu_button.menu.add_command(label="docker logs")
        menu_button.menu.add_command(label="OSPFv3 MDR level")
        menu_button.menu.add_command(label="PIM neighbors")
        menu_button.menu.add_command(label="Edit...")

    def click_stop_button(self):
        logging.debug("Click on STOP button ")
        self.destroy_children_widgets(self.edit_frame)
        self.create_toolbar()

    def click_run_button(self):
        logging.debug("Click on RUN button")

    def click_plot_button(self):
        logging.debug("Click on plot button")

    def click_marker_button(self):
        logging.debug("Click on marker button")

    def click_two_node_button(self):
        logging.debug("Click TWONODE button")

    def create_runtime_toolbar(self):
        self.create_regular_button(
            self.edit_frame, Images.get("stop"), self.click_stop_button
        )
        self.create_radio_button(
            self.edit_frame,
            Images.get("select"),
            self.click_selection_tool,
            self.exec_radio_value,
            1,
        )
        self.create_observe_button()
        self.create_radio_button(
            self.edit_frame,
            Images.get("plot"),
            self.click_plot_button,
            self.exec_radio_value,
            2,
        )
        self.create_radio_button(
            self.edit_frame,
            Images.get("marker"),
            self.click_marker_button,
            self.exec_radio_value,
            3,
        )
        self.create_radio_button(
            self.edit_frame,
            Images.get("twonode"),
            self.click_two_node_button,
            self.exec_radio_value,
            4,
        )
        self.create_regular_button(
            self.edit_frame, Images.get("run"), self.click_run_button
        )
