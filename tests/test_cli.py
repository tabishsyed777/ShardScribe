import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from model import analyze

ROOT = Path(__file__).resolve().parents[1]

class InterfaceTests(unittest.TestCase):
    def test_example_pipeline(self):
        sample = json.loads((ROOT/"example.json").read_text())
        result = analyze(sample)
        if "fragments" in sample:
            for f,i in zip(sample["fragments"],result["locations"],strict=True):
                self.assertEqual(result["text"][i:i+len(f)],f)
        else:
            probe = result["next_probe"]
            sample["observations"][probe] = True
            self.assertGreater(analyze(sample)["posterior"]["cable"],0.5)

    def test_cli_from_other_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            r = subprocess.run([sys.executable,ROOT/"app.py",ROOT/"example.json"],cwd=folder,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual(json.loads(r.stdout),analyze(json.loads((ROOT/"example.json").read_text())))

    def test_cli_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"input.json"
            for content in [None,"{","null","{}"]:
                if content is not None: path.write_text(content)
                r = subprocess.run([sys.executable,ROOT/"app.py",path],capture_output=True,text=True)
                self.assertEqual(r.returncode,2)
                self.assertIn("Input error",r.stderr)
                self.assertEqual(r.stdout,"")
