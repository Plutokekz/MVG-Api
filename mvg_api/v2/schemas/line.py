from __future__ import annotations

from typing import List

from pydantic import BaseModel, RootModel


class Line(BaseModel):
    label: str
    transportType: str
    network: str
    divaId: str
    sev: bool


class Lines(RootModel):
    root: List[Line]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
