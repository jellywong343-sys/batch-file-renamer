import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from batch_file_renamer.cli import apply_plan,build_plan,undo
class Tests(unittest.TestCase):
 def test_apply_and_undo(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); (root/"b.txt").write_text("b"); (root/"a.txt").write_text("a")
   plan=build_plan(root,prefix="item-"); manifest=root/"rename-manifest.json"; apply_plan(plan,manifest)
   self.assertTrue((root/"item-001.txt").exists()); undo(manifest); self.assertTrue((root/"a.txt").exists())
if __name__ == "__main__": unittest.main()
