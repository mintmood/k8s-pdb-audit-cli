import unittest
import pdb_audit


class TestPdbAudit(unittest.TestCase):
    def test_labels_match(self):
        self.assertTrue(pdb_audit.labels_match({"app": "api"}, {"app": "api", "env": "prod"}))
        self.assertFalse(pdb_audit.labels_match({}, {"app": "api"}))

    def test_blocking_pdb(self):
        self.assertTrue(pdb_audit.is_blocking_pdb(3, None, 3))
        self.assertTrue(pdb_audit.is_blocking_pdb("100%", None, 2))
        self.assertTrue(pdb_audit.is_blocking_pdb(None, 0, 2))
        self.assertFalse(pdb_audit.is_blocking_pdb(2, None, 3))
