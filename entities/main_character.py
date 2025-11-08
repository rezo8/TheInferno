from dataclasses import dataclass, field
from typing import Dict


@dataclass
class MainCharacter:
    gold: int = 0
    items: Dict[str, int] = field(default_factory=dict)

    def add_gold(self, amount: int) -> None:
        self.gold += amount

    def add_item(self, name: str, qty: int = 1) -> None:
        self.items[name] = self.items.get(name, 0) + qty

    def inventory(self) -> str:
        parts = [f"gold: {self.gold}"]
        for k, v in self.items.items():
            parts.append(f"{k}: {v}")
        return ", ".join(parts)

    def has_item(self, name: str) -> bool:
        return self.items.get(name, 0) > 0

    def remove_item(self, name: str, qty: int = 1) -> bool:
        cur = self.items.get(name, 0)
        if cur < qty:
            return False
        if cur == qty:
            del self.items[name]
        else:
            self.items[name] = cur - qty
        return True
