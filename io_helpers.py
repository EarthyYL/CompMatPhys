import re
from pathlib import Path


def change_param(file: Path | str, param: str, new_val: str | float | int) -> None:
    """Replace the value of a `param = value` line in a QE input file in place."""
    path = Path(file)
    text = path.read_text()
    pattern = re.compile(rf"^(\s*{re.escape(param)}\s*=\s*).*?(,?\s*)$", re.MULTILINE)
    new_text, n = pattern.subn(rf"\g<1>{new_val}\g<2>", text, count=1)
    if n == 0:
        raise ValueError(f"parameter {param!r} not found in {path}")
    path.write_text(new_text)


def _demo() -> None:
    import tempfile

    sample = "&SYSTEM\n ibrav = 0,\n A = 4.17970,\n nat = 6,\n/\n"
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "qe.in"

        # loop over A values, as needed for e.g. an equation-of-state scan
        for a in (4.0, 4.1, 4.2):
            f.write_text(sample)
            change_param(f, "A", a)
            assert f" A = {a},\n" in f.read_text()

        f.write_text(sample)
        change_param(f, "nat", 8)
        assert " nat = 8,\n" in f.read_text()
        assert " ibrav = 0,\n" in f.read_text()  # untouched neighbor line

        try:
            change_param(f, "not_a_param", 1)
            raise AssertionError("expected ValueError")
        except ValueError:
            pass

    print("io.py self-check passed")


if __name__ == "__main__":
    _demo()
