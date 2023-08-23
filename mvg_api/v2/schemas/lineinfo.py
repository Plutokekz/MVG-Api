from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, RootModel


class Key(BaseModel):
    transportType: str
    label: Optional[str] = None


class Info(BaseModel):
    key: Key
    value: str


class Infos(RootModel):
    root: List[Info]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)
