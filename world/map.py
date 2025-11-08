# ...existing code...
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import yaml

@dataclass
class MapNode:
    description: str = ""
    encounter: Optional[str] = None
    children: Dict[str, "MapNode"] = field(default_factory=dict)
    items: Dict[str, int] = field(default_factory=dict)
    end: bool = False

    def add_child(self, direction: str, node: "MapNode") -> None:
        self.children[direction] = node

    def __repr__(self) -> str:
        return f"MapNode(desc={self.description!r}, encounter={self.encounter!r}, children={list(self.children.keys())}, end={self.end})"


def _build_node_from_spec(spec: Any, _cache: Optional[Dict[int, MapNode]] = None) -> MapNode:
    """
    Recursively construct MapNode from a YAML spec while handling aliases/cycles.

    Uses object identity (id(spec)) as the cache key so YAML anchors/aliases
    which produce shared Python objects won't cause infinite recursion.
    """
    if _cache is None:
        _cache = {}

    # shorthand: plain string -> description-only node
    if not isinstance(spec, dict):
        return MapNode(description=str(spec))

    key = id(spec)
    if key in _cache:
        return _cache[key]

    desc = spec.get("description", "")
    enc = spec.get("encounter")
    end_flag = bool(spec.get("end", False))
    items = spec.get("items", {}) or {}
    if not isinstance(items, dict):
        raise ValueError("items must be a mapping of item-name -> qty")
    node = MapNode(description=desc, encounter=enc, items=dict(items), end=end_flag)

    # store in cache before recursing to handle cycles/aliases
    _cache[key] = node

    exits = spec.get("exits", {}) or {}
    if not isinstance(exits, dict):
        raise ValueError("exits must be a mapping of direction -> node-spec")
    for direction, child_spec in exits.items():
        child = _build_node_from_spec(child_spec, _cache)
        node.add_child(direction, child)
    return node


def load_tree_from_yaml(path: str) -> MapNode:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        raise ValueError("Empty YAML map")
    if isinstance(data, dict) and len(data) == 1:
        root_spec = next(iter(data.values()))
    else:
        root_spec = data
    return _build_node_from_spec(root_spec)
# ...existing code...
