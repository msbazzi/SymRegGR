"""Tests for Native_in_* and Scaffold_in_* parsers."""

import unittest
from pathlib import Path

from .input_parser import (
    _clean_tokens,
    TokenReader,
    parse_native_file,
    parse_scaffold_file,
)
from .input_types import NativeParams, ScaffoldParams


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
