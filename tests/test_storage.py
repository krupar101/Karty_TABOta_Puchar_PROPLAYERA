import json
from pathlib import Path
import tempfile
import unittest
from tabota.storage import Storage, new_profile, make_reading, validate_reading, validate_match
from tabota.engine import Match


class PersistenceTests(unittest.TestCase):
    def test_reading_exact_question_no_duplicates(self):
        for count in [1,3,5]:
            for _ in range(50):
                r=make_reading("  Pytanie\nbez zmian?  ",count)
                self.assertEqual(r["question"],"  Pytanie\nbez zmian?  ")
                self.assertEqual(len(set(r["cards"])),count)
                validate_reading(r)

    def test_invalid_readings_rejected(self):
        with self.assertRaises(ValueError):make_reading("x"*501,3)
        with self.assertRaises(ValueError):make_reading("",2)
        r=make_reading("",3);r["cards"][0]="E01"
        with self.assertRaises(ValueError):validate_reading(r)
        r=make_reading("",3);r["cards"][1]=r["cards"][0]
        with self.assertRaises(ValueError):validate_reading(r)

    def test_roundtrip_and_separate_stores(self):
        with tempfile.TemporaryDirectory() as d:
            s=Storage(d);s.data["slots"][0]=new_profile();s.profile["match"]=Match().s;s.campaign()
            r=make_reading("Prywatne pytanie",5);r["revealed"]=[0,2];r["note"]="Notatka"
            s.tarot["readings"].append(r);s.readings()
            reload=Storage(d)
            self.assertEqual(reload.data,s.data);self.assertEqual(reload.tarot,s.tarot)
            reload.data["slots"][0]=new_profile();reload.campaign()
            self.assertEqual(Storage(d).tarot["readings"][0],r)

    def test_backup_recovers_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            s=Storage(d);s.data["slots"][0]=new_profile("Pierwsza");s.campaign()
            s.profile["name"]="Druga";s.campaign()
            Path(d,"campaign.json").write_text("invalid",encoding="utf-8")
            recovered=Storage(d)
            self.assertEqual(recovered.profile["name"],"Pierwsza");self.assertTrue(recovered.warnings)

    def test_import_validates_before_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            s=Storage(d);path=Path(d,"import.json")
            r=make_reading("test",3)
            path.write_text(json.dumps(dict(schema=1,readings=[r])),encoding="utf-8")
            s.import_file(path,"readings");s.import_file(path,"readings")
            self.assertEqual(len(s.tarot["readings"]),1)
            path.write_text('{"schema":99,"readings":[]}',encoding="utf-8")
            with self.assertRaises(ValueError):s.import_file(path,"readings")
            self.assertEqual(len(s.tarot["readings"]),1)

    def test_match_validated(self):
        m=Match();validate_match(m.s)
        m.s["hand"][0][0]["buff"]=999
        with self.assertRaises(ValueError):validate_match(m.s)


if __name__ == "__main__":unittest.main()
