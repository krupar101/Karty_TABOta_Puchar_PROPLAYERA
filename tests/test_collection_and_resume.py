"""Regression coverage for isolated previews and cup/duel navigation."""
import tempfile
import unittest
from unittest.mock import patch

try:
    from PySide6.QtCore import QCoreApplication
    from tabota.bridge import Bridge
except ImportError:
    Bridge = None


@unittest.skipIf(Bridge is None, "Requires PySide6")
class CollectionAndResumeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QCoreApplication.instance() or QCoreApplication([])

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.api = Bridge(self.directory.name)
        self.api.newGame(0, "Test")

    def tearDown(self):
        self.api.save_timer.stop()
        self.api.play_timer.stop()
        self.api.settings_save_timer.stop()
        self.directory.cleanup()

    def test_inspection_does_not_reset_collection_or_global_state(self):
        self.api.navigate("collection")
        global_updates, detail_updates = [], []
        self.api.changed.connect(lambda: global_updates.append(True))
        self.api.detailChanged.connect(lambda: detail_updates.append(True))
        catalog = self.api.state["catalog"]
        cid = next(c["id"] for c in catalog if c["unlocked"])
        self.api.inspect(cid)
        self.assertEqual(self.api.detailState["detail"]["id"], cid)
        self.api.closeDetail()
        self.assertEqual(self.api.detailState["detail"], {})
        self.assertIs(self.api.state["catalog"], catalog)
        self.assertEqual(global_updates, [])
        self.assertEqual(len(detail_updates), 2)

    def test_free_match_survives_return_to_story_and_resume(self):
        self.api.campaignMode(False, True)
        self.api.begin_match()
        saved = self.api.match.s.copy()
        self.api.navigate("menu")
        self.api.continueCup()
        self.assertEqual(self.api.screen, "map")
        self.assertFalse(self.api.free)
        self.assertFalse(self.api.hard)
        self.assertTrue(self.api.state["resumableFree"])
        self.assertEqual(self.api.match.s, saved)
        self.api.navigate("settings")
        self.api.resumeMatch()
        self.assertEqual(self.api.screen, "battle")
        self.assertTrue(self.api.free)
        self.assertEqual(self.api.match.s, saved)

    def test_cup_resumes_story_match_even_after_browsing_free_mode(self):
        self.api.begin_match()
        self.api.campaignMode(False, True)
        self.assertFalse(self.api.state["resumableFree"])
        self.api.continueCup()
        self.assertEqual(self.api.screen, "battle")
        self.assertFalse(self.api.free)

    def test_reloaded_free_match_opens_story_map_from_continue_cup(self):
        self.api.campaignMode(False, True)
        self.api.begin_match()
        other = Bridge(self.directory.name)
        other.continueCup()
        self.assertEqual(other.screen, "map")
        self.assertFalse(other.free)
        self.assertTrue(other.state["resumableFree"])
        other.resumeMatch()
        self.assertEqual(other.screen, "battle")
        self.assertTrue(other.free)

    def test_volume_drag_updates_live_without_refresh_or_disk_writes(self):
        notifications = []
        self.api.volumeChanged.connect(lambda: notifications.append(self.api.volumes))
        with patch.object(self.api, "refresh") as refresh, patch.object(self.api.store, "write") as write:
            for value in (.1, .2, .3, .8):
                self.api.setting("musicVolume", value)
                self.api.setting("volume", value)
            refresh.assert_not_called()
            write.assert_not_called()
            self.assertEqual(len(notifications), 8)
            self.assertEqual(self.api.volumes, {"volume": .8, "musicVolume": .8})
            self.assertTrue(self.api.settings_save_timer.isActive())
            self.api.flush_settings()
            write.assert_called_once_with("settings.json", self.api.store.settings)
            self.assertFalse(self.api.settings_save_timer.isActive())

    def test_quit_preserves_pending_volume_changes(self):
        self.api.setting("musicVolume", .17)
        self.api.setting("volume", .73)
        self.api.quit()
        other = Bridge(self.directory.name)
        self.assertEqual(other.volumes, {"volume": .73, "musicVolume": .17})
