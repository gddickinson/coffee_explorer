"""
Coffee Explorer tab modules.

Each module provides a mixin class that contributes one notebook tab
and all its event handlers to the main CoffeeExplorerApp.
"""

from tabs.database_tab import DatabaseTabMixin
from tabs.varieties_tab import VarietiesTabMixin
from tabs.roasters_tab import RoastersTabMixin
from tabs.brewing_tab import BrewingTabMixin
from tabs.journal_tab import JournalTabMixin
from tabs.guide_tab import GuideTabMixin
from tabs.map_tab import MapTabMixin

__all__ = [
    "DatabaseTabMixin",
    "VarietiesTabMixin",
    "RoastersTabMixin",
    "BrewingTabMixin",
    "JournalTabMixin",
    "GuideTabMixin",
    "MapTabMixin",
]
