"""Tests for Native_in_* and Scaffold_in_* parsers."""

import sys
import unittest
from pathlib import Path

# Ensure project root is on path when running this file directly (e.g. python test_parser.py)
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.input_parser import (
    _clean_tokens,
    TokenReader,
    parse_immune_file,
    parse_native_file,
    parse_scaffold_file,
)
from src.input_types import ImmuneParams, NativeParams, ScaffoldParams


class TestCleanTokens(unittest.TestCase):
    def test_skips_comments(self) -> None:
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("# comment line\n1.0 2.0\n# another\n3.0\n")
            path = f.name
        try:
            self.assertEqual(_clean_tokens(path), ["1.0", "2.0", "3.0"])
        finally:
            Path(path).unlink()

    def test_skips_empty_lines(self) -> None:
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("a\n\n\nb\n")
            path = f.name
        try:
            self.assertEqual(_clean_tokens(path), ["a", "b"])
        finally:
            Path(path).unlink()


class TestTokenReader(unittest.TestCase):
    def test_reads_in_order(self) -> None:
        t = TokenReader(["foo", "1.5", "2.0"])
        self.assertEqual(t.read_str(), "foo")
        self.assertEqual(t.read_float(), 1.5)
        self.assertEqual(t.read_float(), 2.0)
        self.assertTrue(t.done())

    def test_raises_on_eof(self) -> None:
        t = TokenReader(["x"])
        t.read_str()
        with self.assertRaises(ValueError):
            t.read_float()

    def test_raises_on_bad_float(self) -> None:
        t = TokenReader(["not_a_number"])
        with self.assertRaises(ValueError):
            t.read_float()


class TestParseScaffoldFile(unittest.TestCase):
    def test_parse_scaffold_file(self) -> None:
        """Parse actual Scaffold_in_ file from G&R_TEVG."""
        scaffold_path = Path(__file__).resolve().parent.parent / "G&R_TEVG" / "Scaffold_in_"
        if not scaffold_path.exists():
            self.skipTest(f"Scaffold file not found: {scaffold_path}")

        params = parse_scaffold_file(scaffold_path)
        self.assertIsInstance(params, ScaffoldParams)
        self.assertEqual(params.vessel_name, "Lamb_TEVG")
        self.assertEqual(params.radius, 8.0)
        self.assertEqual(params.thickness, 0.7)
        self.assertEqual(params.c1_p1, 2000000000.0)
        self.assertEqual(params.c2_p1, 0.0)
        self.assertEqual(params.fd_p1, 8.0)
        self.assertEqual(params.fd_p2, 16.0)


class TestParseNativeFile(unittest.TestCase):
    def test_parse_native_file(self) -> None:
        """Parse actual Native_in_ file from G&R_TEVG."""
        native_path = Path(__file__).resolve().parent.parent / "G&R_TEVG" / "Native_in_"
        if not native_path.exists():
            self.skipTest(f"Native file not found: {native_path}")

        params = parse_native_file(native_path)
        self.assertIsInstance(params, NativeParams)
        self.assertEqual(params.vessel_name, "Lamb_Thoracic_IVC")
        self.assertEqual(params.radius, 8.573)
        self.assertEqual(params.thickness, 0.743)
        self.assertEqual(params.lambda_z_h, 1.0)
        self.assertEqual(params.P_h, 615.0)
        self.assertEqual(params.Q_h, 20.0)


class TestParseImmuneFile(unittest.TestCase):
    def test_parse_immune_file(self) -> None:
        """Parse actual Immune_in_ file from G&R_TEVG."""
        immune_path = Path(__file__).resolve().parent.parent / "G&R_TEVG" / "Immune_in_"
        if not immune_path.exists():
            self.skipTest(f"Immune file not found: {immune_path}")

        params = parse_immune_file(immune_path)
        self.assertIsInstance(params, ImmuneParams)
        self.assertEqual(params.gamma_i_1, 5.0)
        self.assertEqual(params.gamma_i_2, 1.0)
        self.assertEqual(params.gamma_p_d1, 1.5)
        self.assertEqual(params.window_end, 120.0)
        self.assertEqual(params.rat_smc2col_p, 30.0)
        self.assertEqual(params.rat_smc2col_d, 1.8)


class TestLoadCase(unittest.TestCase):
    def test_load_case(self) -> None:
        """Load case with native, scaffold, and immune files."""
        from src.load_case import load_case

        base = Path(__file__).resolve().parent.parent / "G&R_TEVG"
        if not (base / "Native_in_").exists():
            self.skipTest("Input files not found")

        native, scaffold, immune = load_case(
            base / "Native_in_",
            base / "Scaffold_in_",
            base / "Immune_in_",
        )
        self.assertEqual(native.vessel_name, "Lamb_Thoracic_IVC")
        self.assertEqual(scaffold.vessel_name, "Lamb_TEVG")
        self.assertIsNotNone(immune)
        if immune:
            self.assertEqual(immune.gamma_i_1, 5.0)


class TestAsdictExport(unittest.TestCase):
    def test_asdict_export(self) -> None:
        """Verify dataclasses can be converted to dict for logging/JSON."""
        from dataclasses import asdict

        scaffold_path = Path(__file__).resolve().parent.parent / "G&R_TEVG" / "Scaffold_in_"
        if not scaffold_path.exists():
            self.skipTest("Scaffold file not found")

        params = parse_scaffold_file(scaffold_path)
        d = asdict(params)
        self.assertIsInstance(d, dict)
        self.assertEqual(d["vessel_name"], params.vessel_name)
        self.assertEqual(d["radius"], params.radius)


if __name__ == "__main__":
    unittest.main()
