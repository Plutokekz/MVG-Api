from __future__ import annotations

from typing import List

from pydantic import BaseModel, RootModel


class Aushang(BaseModel):
    uri: str
    scheduleKind: str
    scheduleName: str
    direction: str


class Aushaenge(RootModel):
    root: List[Aushang]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
