import tkinter as tk
from typing import Optional

from behave import *
from conscience.lobes.lobe import Lobe
from conscience.lib.mocking import VacantLog, copy_function
from conscience.parsers import register_parsers


class MockMenu(Lobe):
    def on_start(self, context, suite):
        old_config = copy_function(tk.Tk.config)
        context.menus = []

        def inject_config(self, **kwargs):
            old_config(self, **kwargs)
            if "menu" in kwargs:
                context.menus.append(kwargs["menu"])

        setattr(tk.Tk, "config", inject_config)

        load_file_menu_tests()


class FilemenuManager:
    def __init__(self, gui):
        self._gui = gui

    def list_menu_children(self, menu, options=["label"]):
        # Brae: holy damn they did not want this traversed
        index = 0
        results = []
        last_real_index = -1

        while True:
            real_index = menu.index(index)
            if last_real_index == real_index:
                break
            last_real_index = real_index

            result: list[Optional[int]] = [index]
            for option in options:
                try:
                    result.append(menu.entrycget(index, option))
                except tk.TclError as e:
                    result.append(None)
            results.append(result)
            index += 1

        return results

    def menu_tree(self, root_menu):
        children = []
        for menu in self.list_menu_children(root_menu, options=["label", "menu"]):
            if menu[2] is not None:
                widget = self._gui.nametowidget(menu[2])
                children.append((menu[0], menu[1], root_menu, self.menu_tree(widget)))
            elif menu[1] is not None:
                children.append((menu[0], menu[1], root_menu, []))
        return children

    def has_name(self, tree, name):
        for element in tree:
            if name in element[1].lower():
                return True
            if self.has_name(element[-1], name):
                return True
        return False

    def get_by_name(self, tree, name):
        for element in tree:
            if name in element[1].lower():
                return element
            child = self.get_by_name(element[-1], name)
            if child is not None:
                return child
        return None

    def find_filemenu(self, menus):
        for menu in menus:
            tree = self.menu_tree(menu)
            if self.has_name(tree, "file"):
                return tree


def get_filemenu(context):
    manager = FilemenuManager(context.suite.window)
    menu = manager.find_filemenu(context.menus)

    if menu is None:
        assert False, f"unable to find a file menu, menus: {context.menus}"

    return manager, menu


def get_menu_option(context, menu_item):
    manager, menu = get_filemenu(context)
    selected_menu = manager.get_by_name(menu, menu_item)
    if selected_menu is None:
        print(f"menu structure: {menu}")
        assert False, f"unable to find the {menu_item} menu option"

    return selected_menu


def load_file_menu_tests():
    register_parsers()

    @then("the file menu is displayed")
    def filemenu_displayed(context):
        get_filemenu(context)

    @then("I can see a {menu_item:Text} menu option")
    def sees_menu_option(context, menu_item):
        get_menu_option(context, menu_item)

    @when("I select the {menu_item:Text} menu option")
    def menu_selected(context, menu_item):
        selected_menu = get_menu_option(context, menu_item)

        selected_menu[2].invoke(selected_menu[0])
