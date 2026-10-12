import json
from pathlib import Path

import numpy as np

from io_utils import save_csv, save_json


def test_serializers_write_numpy_values(tmp_path: Path):
    csv_path = tmp_path / "table.csv"
    json_path = tmp_path / "data.json"
    save_csv(csv_path, [{"x": np.int64(2), "y": np.float64(3.5)}])
    save_json(json_path, {"array": np.array([1.0, 2.0]), "complex": 1.0 + 2.0j})
    assert "2,3.5" in csv_path.read_text(encoding="utf-8")
    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded == {"array": [1.0, 2.0], "complex": {"real": 1.0, "imag": 2.0}}
