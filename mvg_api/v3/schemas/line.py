from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, RootModel

from mvg_api.v3.network import NetworkLine


class Line(BaseModel):
    label: str
    """The line label, e.g. U4"""
    transportType: str
    """The transport type"""
    trainType: Optional[str] = None
    """unknown"""
    network: str
    """provider; encountered 'DDB' for Deutsche Bahn, 'SWM' for ubahn, 'MVV' for buses, 'MUENCHNER_LINIEN' and 'LUFTHANSA' """
    divaId: str
    """unknown"""
    sev: bool
    """unknown"""

    def to_network_line(self):
        """Converts this line descriptor to the standardized network line"""
        return NetworkLine.of_any(self)


class Lines(RootModel):
    """A list of service lines at a station or globally as returned by the API."""
    root: List[Line]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)

    def sorted(self, *, key=lambda l: l.label.rjust(5, "0"), reverse: bool = False) -> Lines:
        """
        Sorts the lines to present them in a more sensible ordering.
        :param key: key to sort with, default to sorting by label.
        """
        return Lines(sorted(self.root, key=key, reverse=reverse))
